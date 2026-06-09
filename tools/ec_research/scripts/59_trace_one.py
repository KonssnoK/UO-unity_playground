"""Trace one specific tile through the full resolution chain so we can spot
exactly where it goes wrong."""
from __future__ import annotations

import io
import re
import struct
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")

# user said "tile 200 is a stone wall in classic"
ITEM_ID = 200
ART_ID  = ITEM_ID + 0x4000

print(f"Investigating CC item id {ITEM_ID}  (art_id {ART_ID} = 0x{ART_ID:04X})")
print()


# 1. Pull the CC art to confirm dimensions
art_uop = UopArchive(CC / "artLegacyMUL.uop")
cc_buf = art_uop.get_by_name(f"build/artlegacymul/{ART_ID:08}.tga")
if cc_buf:
    flags = struct.unpack_from("<I", cc_buf, 0)[0]
    w = struct.unpack_from("<H", cc_buf, 4)[0]
    h = struct.unpack_from("<H", cc_buf, 6)[0]
    print(f"CC art: width={w}, height={h}, flags=0x{flags:X}")
art_uop.close()


# 2. Read tileart record for art_id
tileart = UopArchive(EC / "tileart.uop")
h = hash_name(f"build/tileart/{ART_ID:08}.bin")
e = tileart.by_hash.get(h)
if e is None:
    print(f"No tileart record for art_id {ART_ID}!")
    sys.exit(1)
payload = tileart.read(e)
print(f"tileart record bytes = {len(payload)}")

# Header fields
print(f"  Version: {struct.unpack_from('<H', payload, 0)[0]}")
print(f"  StringId: {struct.unpack_from('<I', payload, 2)[0]}")
print(f"  TileId (from record): {struct.unpack_from('<I', payload, 6)[0]}")
print(f"  Flags EC: 0x{struct.unpack_from('<Q', payload, 0x39)[0]:016X}")
print(f"  Flags Legacy: 0x{struct.unpack_from('<Q', payload, 0x41)[0]:016X}")

# EC sprite layout (0x4D)
ec_layout = struct.unpack_from("<6i", payload, 0x4D)
print(f"  EC sprite layout: {ec_layout}")
# Legacy (0x65)
lg_layout = struct.unpack_from("<6i", payload, 0x65)
print(f"  Legacy sprite layout: {lg_layout}")


# Re-parse SUB_9_7 per the wiki and resolve through string dict
def sub_9_7_offset(payload):
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


def load_sd_index():
    arc = UopArchive(EC / "string_dictionary.uop")
    sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
    arc.close()
    out = []
    p = 16
    while p + 2 <= len(sd):
        length = struct.unpack_from("<H", sd, p)[0]
        if length == 0 or length > 500: break
        content_start = p + 2
        content_end = content_start + length
        if content_end > len(sd): break
        out.append((content_start, content_end, sd[content_start: content_end].decode("ascii", errors="replace")))
        p = content_end
    return out


def find_containing(index, offset):
    lo, hi = 0, len(index)
    while lo < hi:
        mid = (lo + hi) // 2
        s, e, _ = index[mid]
        if offset < s: hi = mid
        elif offset >= e: lo = mid + 1
        else: return index[mid]
    return None


RX_WORLD = re.compile(r'Data\\WorldArt\\(\d+)(?:_[^.]*)?\.tga', re.I)
RX_LEGACY = re.compile(r'Data\\TileArtLegacy\\(\d+)\.tga', re.I)
RX_ENHANCED = re.compile(r'Data\\TileArtEnhanced\\(\d+)\.tga', re.I)

off = sub_9_7_offset(payload)
print(f"\nSUB_9_7 starts at offset 0x{off:X}")

sd_index = load_sd_index()
print(f"Loaded {len(sd_index)} dictionary entries")

p = off
for gname in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
    val = payload[p]; p += 1
    print(f"\n[{gname}] Val={val}")
    if val == 0: continue
    print(f"  unknown byte: 0x{payload[p]:02X}"); p += 1
    shader = struct.unpack_from("<I", payload, p)[0]; p += 4
    print(f"  shader: 0x{shader:08X}")
    count = payload[p]; p += 1
    print(f"  texture count: {count}")
    for i in range(count):
        sd_off = struct.unpack_from("<I", payload, p)[0]; p += 4
        _b = payload[p]; p += 1
        rep = struct.unpack_from("<f", payload, p)[0]; p += 4
        d1 = struct.unpack_from("<I", payload, p)[0]; p += 4
        d2 = struct.unpack_from("<I", payload, p)[0]; p += 4
        ent = find_containing(sd_index, sd_off)
        s = ent[2] if ent else None
        print(f"  #{i}: sd_off={sd_off}  rep={rep}  d1={d1} d2={d2}")
        print(f"      -> string: {s!r}")
        if s:
            for label, rx, prefix, archive_name in (
                ("WorldArt", RX_WORLD, "build/worldart/", "Texture.uop"),
                ("Legacy",   RX_LEGACY, "build/tileartlegacy/", "LegacyTexture.uop"),
                ("Enhanced", RX_ENHANCED, "build/tileartenhanced/", "EnhancedTexture.uop"),
            ):
                m = rx.match(s)
                if m:
                    sid = int(m.group(1))
                    arc = UopArchive(EC / archive_name) if (EC / archive_name).exists() else None
                    if arc:
                        key = f"{prefix}{sid:08}.dds"
                        ent = arc.by_hash.get(hash_name(key))
                        if ent:
                            dds = arc.read(ent)
                            try:
                                img = Image.open(io.BytesIO(dds)).convert("RGBA")
                                print(f"      => {label} sid={sid} → {archive_name}[{key}]  dims={img.width}x{img.height}")
                                # Save it for visual comparison
                                out_dir = HERE.parent / "out" / "trace_one"
                                out_dir.mkdir(parents=True, exist_ok=True)
                                img.save(out_dir / f"tile{ART_ID:05}_{label}_{sid}.png")
                                print(f"         saved → {out_dir / f'tile{ART_ID:05}_{label}_{sid}.png'}")
                            except Exception as ex:
                                print(f"      => DDS decode failed: {ex}")
                        else:
                            print(f"      => MISS in {archive_name} ({key})")
                        arc.close()
                    else:
                        print(f"      => {archive_name} NOT SHIPPED")
                    break
            else:
                print(f"      => no namespace match")
    c2 = struct.unpack_from("<I", payload, p)[0]; p += 4
    for _ in range(c2):
        p += 4
    c3 = struct.unpack_from("<I", payload, p)[0]; p += 4
    for _ in range(c3):
        p += 4

# Also dump the CC art for comparison
art_uop = UopArchive(CC / "artLegacyMUL.uop")
cc_buf = art_uop.get_by_name(f"build/artlegacymul/{ART_ID:08}.tga")
if cc_buf:
    # Decode CC art and save
    flags = struct.unpack_from("<I", cc_buf, 0)[0]
    w = struct.unpack_from("<H", cc_buf, 4)[0]
    h = struct.unpack_from("<H", cc_buf, 6)[0]
    line_offsets = struct.unpack_from(f"<{h}H", cc_buf, 8)
    data_start = 8 + h * 2
    pixels = bytearray(w * h * 4)
    for y in range(h):
        if line_offsets[y] == 0 and y != 0:
            continue
        ptr = data_start + line_offsets[y] * 2
        x = 0
        while True:
            if ptr + 4 > len(cc_buf): break
            xoffs = struct.unpack_from("<H", cc_buf, ptr)[0]; ptr += 2
            run   = struct.unpack_from("<H", cc_buf, ptr)[0]; ptr += 2
            if xoffs + run >= 2048: break
            if xoffs + run == 0: break
            x += xoffs
            for _ in range(run):
                if ptr + 2 > len(cc_buf): break
                val = struct.unpack_from("<H", cc_buf, ptr)[0]; ptr += 2
                if val:
                    r = ((val >> 10) & 0x1F) << 3
                    g = ((val >>  5) & 0x1F) << 3
                    b = ( val        & 0x1F) << 3
                    px = (y * w + x) * 4
                    pixels[px]   = r; pixels[px+1] = g; pixels[px+2] = b; pixels[px+3] = 0xFF
                x += 1
    out_dir = HERE.parent / "out" / "trace_one"
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.frombytes("RGBA", (w, h), bytes(pixels))
    img.save(out_dir / f"tile{ART_ID:05}_CC_art.png")
    print(f"\nSaved CC reference → {out_dir / f'tile{ART_ID:05}_CC_art.png'}")
art_uop.close()
tileart.close()
