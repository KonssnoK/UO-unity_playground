"""Dump full tileart record for tile 2 and render ALL three sources (CC, EC legacy,
EC HD) at native pixel scale. Then walk the record looking for any 6-int triplet
that has a 'tall narrow rect' matching CC's visible content (24x73)."""
import struct, sys, io
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
OUT = HERE.parent / "out" / "offsets_viz"

TILE = 2
ART  = 0x4000 + TILE

tileart = UopArchive(EC / 'tileart.uop')
e = tileart.by_hash.get(hash_name(f'build/tileart/{ART:08}.bin'))
payload = tileart.read(e)
tileart.close()

print(f"tile {TILE} (art_id {ART}) record length = {len(payload)} bytes\n")
print("--- hex dump ---")
for i in range(0, len(payload), 16):
    chunk = payload[i:i+16]
    hexs = ' '.join(f'{b:02x}' for b in chunk)
    asci = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
    print(f"  {i:04x}: {hexs:<48}  {asci}")

# Scan every 4-byte-aligned position for plausible (X0,Y0,X1,Y1) bounds
# matching CC's visible bbox (20,1,44,73) or the EC legacy visible bbox.
print("\n--- candidate 6-int triplets in record ---")
print("  Looking for small reasonable bounds matching CC tile shapes.")
for off in range(0, len(payload) - 24, 4):
    vals = struct.unpack_from('<6i', payload, off)
    x0, y0, x1, y1, ax, ay = vals
    # Heuristic: rect with sensible small dims
    if 0 <= x0 < 256 and 0 <= y0 < 256 and 0 < x1 < 256 and 0 < y1 < 256 \
       and x0 < x1 and y0 < y1 and -300 < ax < 300 and -300 < ay < 300:
        w = x1 - x0; h = y1 - y0
        # filter trivial header-size combos
        if (w, h) in {(0, 0)}: continue
        print(f"  off=0x{off:02X} ({off:>3}): {vals}  → {w}x{h}")

# Also: scan for 4-int rectangles (no anchor)
print("\n--- candidate 4-int rectangles (X0,Y0,X1,Y1) ---")
for off in range(0, len(payload) - 16, 4):
    x0, y0, x1, y1 = struct.unpack_from('<4i', payload, off)
    if 0 <= x0 < 100 and 0 <= y0 < 100 and 10 <= x1 < 256 and 10 <= y1 < 256 \
       and x0 < x1 and y0 < y1:
        w = x1 - x0; h = y1 - y0
        if w >= 20 and h >= 20 and w <= 80 and h <= 200:
            print(f"  off=0x{off:02X} ({off:>3}): ({x0},{y0},{x1},{y1})  → {w}x{h}")

# Render HD (no rect) so we can see it.
hd = UopArchive(EC / 'Texture.uop')
ent = hd.by_hash.get(hash_name(f'build/worldart/{TILE:08}.dds'))
if ent:
    dds = hd.read(ent)
    try:
        img = Image.open(io.BytesIO(dds)).convert('RGBA')
        bbox = img.getbbox()
        print(f"\nEC HD: {img.width}x{img.height}, visible bbox: {bbox} → {bbox[2]-bbox[0]}x{bbox[3]-bbox[1]}")
        # Upscale 2x and save
        up = img.resize((img.width*2, img.height*2), Image.NEAREST)
        d = ImageDraw.Draw(up)
        if bbox:
            d.rectangle([bbox[0]*2, bbox[1]*2, bbox[2]*2-1, bbox[3]*2-1], outline=(0,255,0,255), width=1)
        up.save(OUT / f'tile{TILE:02}_ec_hd.png')
        print(f"  saved → tile{TILE:02}_ec_hd.png")
    except Exception as ex:
        print(f"  HD decode failed: {ex}")
hd.close()
