"""For a set of known tiles, render the CC art and the candidate EC sprite,
then compare them (dimensions + color histogram) to find which BYTE LAYOUT
in the SUB_9_7 entry gives the correct sprite_id.

Outputs a per-byte-interpretation success rate over the test set, so we
can pick the layout that ACTUALLY produces matching sprites.
"""
from __future__ import annotations

import io
import struct
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")


# ---------- Read a single CC static art tile from artLegacyMUL.uop ----------

def load_cc_art(art_uop: UopArchive, art_id: int) -> bytes | None:
    """Return raw (W, H, RGBA pixel bytes) for a CC static at art_id."""
    h = hash_name(f"build/artlegacymul/{art_id:08}.tga")
    e = art_uop.by_hash.get(h)
    if e is None:
        return None
    return art_uop.read(e)


def decode_cc_static(buf: bytes) -> tuple[int, int, bytes] | None:
    """Decode CC's run-length-encoded ARGB1555 static art into (W,H, raw RGBA)."""
    if len(buf) < 8:
        return None
    flags, w, h = struct.unpack_from("<IHH", buf, 0)
    if w == 0 or h == 0 or w > 1024 or h > 1024:
        return None
    line_offsets = struct.unpack_from(f"<{h}H", buf, 8)
    data_start = 8 + h * 2
    pixels = bytearray(w * h * 4)  # RGBA, transparent by default
    for y in range(h):
        if line_offsets[y] == 0 and y != 0:
            continue
        ptr = data_start + line_offsets[y] * 2
        x = 0
        while True:
            if ptr + 4 > len(buf):
                break
            xoffs = struct.unpack_from("<H", buf, ptr)[0]; ptr += 2
            run   = struct.unpack_from("<H", buf, ptr)[0]; ptr += 2
            if xoffs + run >= 2048:
                break
            if xoffs + run == 0:
                break
            x += xoffs
            for _ in range(run):
                if ptr + 2 > len(buf): break
                val = struct.unpack_from("<H", buf, ptr)[0]; ptr += 2
                if val:
                    a = 0xFF
                    r = ((val >> 10) & 0x1F) << 3
                    g = ((val >> 5)  & 0x1F) << 3
                    b = (val         & 0x1F) << 3
                    px = (y * w + x) * 4
                    pixels[px]     = r
                    pixels[px + 1] = g
                    pixels[px + 2] = b
                    pixels[px + 3] = a
                x += 1
    return (w, h, bytes(pixels))


def color_histogram(rgba: bytes) -> Counter:
    """4-bit-per-channel color histogram of non-transparent pixels."""
    c: Counter = Counter()
    for i in range(0, len(rgba), 4):
        if rgba[i+3] < 128: continue
        key = ((rgba[i] >> 4) << 8) | ((rgba[i+1] >> 4) << 4) | (rgba[i+2] >> 4)
        c[key] += 1
    return c


def histogram_distance(a: Counter, b: Counter) -> float:
    if not a or not b: return 1.0
    total_a = sum(a.values()); total_b = sum(b.values())
    keys = set(a) | set(b)
    diff = 0.0
    for k in keys:
        pa = a.get(k, 0) / total_a
        pb = b.get(k, 0) / total_b
        diff += abs(pa - pb)
    return diff / 2.0


# ---------- Pull all 8 bytes of the first SUB_9_7 entry for a tile ----------

def sub_9_7_offset(payload: bytes) -> int | None:
    try:
        p = 0x7D
        cnt = payload[p]; p += 1 + cnt * 5
        cnt = payload[p]; p += 1 + cnt * 5
        cnt = struct.unpack_from("<I", payload, p)[0]; p += 4 + cnt * 8
        cnt = struct.unpack_from("<I", payload, p)[0]; p += 4
        for _ in range(cnt):
            val = payload[p]; p += 1
            if val == 0:
                sub = struct.unpack_from("<I", payload, p)[0]; p += 4 + sub * 8
            elif val == 1:
                p += 5
            else: return None
        sitting = payload[p]; p += 1
        if sitting != 0: p += 16
        p += 4
        return p
    except Exception:
        return None


def first_entry_bytes(tileart_payload: bytes) -> bytes | None:
    off = sub_9_7_offset(tileart_payload)
    if off is None: return None
    # Walk groups, find first non-empty, return its first 8 bytes
    p = off
    for _ in range(4):
        try:
            cnt = tileart_payload[p]; p += 1
            if cnt > 0:
                return tileart_payload[p: p + 8]
            # Otherwise skip nothing
        except Exception:
            return None
    return None


def main():
    art_uop = UopArchive(CC / "artLegacyMUL.uop")
    tileart = UopArchive(EC / "tileart.uop")
    legacy = UopArchive(EC / "LegacyTexture.uop")
    hd = UopArchive(EC / "Texture.uop")

    # Tiles we want to validate.
    test_tile_ids = [
        16384,    # first static
        16385,
        16386,
        16640,
        16768,
        17664,
        22137,    # face1
    ]

    layouts = {
        "b >> 16 (LE u16 @6)":  lambda e: struct.unpack_from("<H", e, 6)[0],
        "BE u16 @6":            lambda e: struct.unpack_from(">H", e, 6)[0],
        "LE u16 @4":            lambda e: struct.unpack_from("<H", e, 4)[0],
        "BE u16 @4":            lambda e: struct.unpack_from(">H", e, 4)[0],
        "LE u32 @4 & 0xFFFFFF": lambda e: struct.unpack_from("<I", e, 4)[0] & 0xFFFFFF,
        "LE u32 @0":            lambda e: struct.unpack_from("<I", e, 0)[0],
        "LE u32 @4":            lambda e: struct.unpack_from("<I", e, 4)[0],
        "u8 @6 | (u8 @7 << 8)": lambda e: e[6] | (e[7] << 8),
        "u8 @7 | (u8 @6 << 8)": lambda e: e[7] | (e[6] << 8),
        "u8 @5 | (u8 @6 << 8)": lambda e: e[5] | (e[6] << 8),
    }

    for tile_id in test_tile_ids:
        h = hash_name(f"build/tileart/{tile_id:08}.bin")
        e = tileart.by_hash.get(h)
        if e is None:
            print(f"\n--- tile {tile_id}: MISS in tileart")
            continue
        record = tileart.read(e)
        entry = first_entry_bytes(record)
        if entry is None:
            print(f"\n--- tile {tile_id}: no SUB_9_7 entry")
            continue

        # Load CC reference: tile_id is in art-space so use as-is
        cc_buf = load_cc_art(art_uop, tile_id)
        cc = decode_cc_static(cc_buf) if cc_buf else None
        if cc is None:
            print(f"\n--- tile {tile_id}: no CC art to compare against")
            continue
        cc_w, cc_h, cc_rgba = cc
        cc_hist = color_histogram(cc_rgba)

        print(f"\n--- tile {tile_id}: CC art {cc_w}x{cc_h}  entry=[{entry.hex(' ')}] ---")

        for label, fn in layouts.items():
            sid = fn(entry)
            # try legacy archive
            ec_buf = None
            arc = None
            for arc_name, arc_obj, prefix in (("Legacy", legacy, "build/tileartlegacy/"),
                                              ("HD",     hd,      "build/worldart/")):
                ent = arc_obj.by_hash.get(hash_name(f"{prefix}{sid:08}.dds"))
                if ent is not None:
                    ec_buf = arc_obj.read(ent)
                    arc = arc_name
                    break
            if ec_buf is None:
                continue
            # Decode DDS via PIL
            try:
                img = Image.open(io.BytesIO(ec_buf)).convert("RGBA")
            except Exception as ex:
                continue
            ec_hist = color_histogram(img.tobytes())
            dist = histogram_distance(cc_hist, ec_hist)
            size_diff = abs(img.width - cc_w) + abs(img.height - cc_h)
            print(f"  {label:30s} sid={sid:>6d} arc={arc:6s} ec={img.width}x{img.height} "
                  f"hist_diff={dist:.3f} size_diff={size_diff}")

    art_uop.close(); tileart.close(); legacy.close(); hd.close()


if __name__ == "__main__":
    main()
