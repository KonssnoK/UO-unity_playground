"""Inspect the 24-byte image-offset blobs at record offsets 0x4D (EC) and 0x65 (2D).

Per the wiki, each tileart record contains two opaque 24-byte fields right
after the flag QWORDs. We want to know whether they carry the anchor offsets
the renderer needs.

Strategy: dump the two blobs for a large random sample of tiles, look for
columns whose bytes vary per-id (anchors should vary) and columns that are
constant (probably reserved/padding). Also try interpreting as 6 floats,
3×(int16,int16,int16), or other plausible layouts.
"""
from __future__ import annotations

import struct
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name


EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def parse_header(buf: bytes):
    """Pull just enough to land at 0x4D / 0x65 reliably."""
    if len(buf) < 0x7D:
        return None
    version  = struct.unpack_from("<H", buf, 0)[0]
    string_id = struct.unpack_from("<I", buf, 2)[0]
    tile_id  = struct.unpack_from("<I", buf, 6)[0]
    flags_ec     = struct.unpack_from("<Q", buf, 0x39)[0]
    flags_legacy = struct.unpack_from("<Q", buf, 0x41)[0]
    ec_image     = buf[0x4D:0x4D + 24]
    img2d        = buf[0x65:0x65 + 24]
    return {
        "version": version,
        "string_id": string_id,
        "tile_id": tile_id,
        "flags_ec": flags_ec,
        "flags_legacy": flags_legacy,
        "ec_image": ec_image,
        "img2d": img2d,
    }


def fmt_floats(blob: bytes) -> str:
    # interpret as 6 little-endian floats
    f = struct.unpack_from("<6f", blob)
    return "(" + ", ".join(f"{v:+8.3f}" if abs(v) < 1e6 else f"{v:.2e}" for v in f) + ")"


def fmt_i32(blob: bytes) -> str:
    a = struct.unpack_from("<6i", blob)
    return "(" + ", ".join(f"{v:>+8}" for v in a) + ")"


def main():
    arc = UopArchive(EC / "tileart.uop")
    print(f"tileart.uop: {len(arc.entries)} entries")

    # Sample ids: a slice from land range, several from static range, plus
    # known character-customization tiles.
    sample_ids = (
        list(range(0, 8))
        + list(range(0x1000, 0x1004))
        + list(range(0x4000, 0x4008))
        + [0x4100, 0x4180, 0x4200, 0x4500]
        + [0x8000, 0x9000, 0xA000, 0xB000, 0xC000]
        + [22137, 22138, 22139, 8251, 8252, 8253, 5903, 5905, 5433, 5422, 7933]
    )

    print(f"\nSampling {len(sample_ids)} tiles\n")
    print(f"{'id':>8} {'sz':>4} {'flags_ec':>16} {'flags_lg':>16}  ec_blob (hex)                                          2d_blob (hex)")
    print("-" * 170)
    rows = []
    for tid in sample_ids:
        h = hash_name(f"build/tileart/{tid:08}.bin")
        e = arc.by_hash.get(h)
        if e is None:
            continue
        payload = arc.read(e)
        rec = parse_header(payload)
        if not rec:
            continue
        rows.append(rec)
        print(f"{tid:>8} {len(payload):>4} {rec['flags_ec']:>016X} {rec['flags_legacy']:>016X}  "
              f"{rec['ec_image'].hex(' ')}  {rec['img2d'].hex(' ')}")

    # Column-by-column variability across the 24-byte blobs
    def report_variability(label, key):
        print(f"\n--- {label}: per-byte variability across {len(rows)} samples ---")
        cols = [Counter() for _ in range(24)]
        for r in rows:
            blob = r[key]
            for i in range(24):
                cols[i][blob[i]] += 1
        for i in range(24):
            unique = len(cols[i])
            most_common = cols[i].most_common(1)[0]
            tag = "VARIES" if unique > 3 else ("STABLE" if unique == 1 else "low")
            print(f"  byte[{i:2d}]: unique={unique:2d}  most={most_common[0]:#04x}({most_common[1]:>2})  {tag}")

    report_variability("ec_image @ 0x4D", "ec_image")
    report_variability("img2d   @ 0x65", "img2d")

    # Show a handful interpreted as 6 floats
    print("\n--- ec_image as 6 floats (LE) ---")
    for r in rows[:10]:
        print(f"  id={r['tile_id']:>5}  {fmt_floats(r['ec_image'])}")
    print("\n--- img2d as 6 floats (LE) ---")
    for r in rows[:10]:
        print(f"  id={r['tile_id']:>5}  {fmt_floats(r['img2d'])}")

    # Same interpreted as 6 int32
    print("\n--- ec_image as 6 int32 ---")
    for r in rows[:10]:
        print(f"  id={r['tile_id']:>5}  {fmt_i32(r['ec_image'])}")
    print("\n--- img2d as 6 int32 ---")
    for r in rows[:10]:
        print(f"  id={r['tile_id']:>5}  {fmt_i32(r['img2d'])}")

    arc.close()


if __name__ == "__main__":
    main()
