"""Extract static 5650 from CC and EC for side-by-side comparison."""
import struct, sys, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
OUT = Path(__file__).resolve().parent.parent / "out" / "static_5650"
OUT.mkdir(parents=True, exist_ok=True)

ITEM_ID = 5650
ART_ID  = 0x4000 + ITEM_ID  # 22034


def decode_cc_art(buf):
    if len(buf) < 12: return None
    flags = struct.unpack_from('<I', buf, 0)[0]
    w = struct.unpack_from('<H', buf, 4)[0]
    h = struct.unpack_from('<H', buf, 6)[0]
    line_offsets = struct.unpack_from(f'<{h}H', buf, 8)
    data_start = 8 + h * 2
    pixels = bytearray(w * h * 4)
    for y in range(h):
        if line_offsets[y] == 0 and y != 0: continue
        ptr = data_start + line_offsets[y] * 2
        x = 0
        while True:
            if ptr + 4 > len(buf): break
            xoffs = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
            run   = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
            if xoffs + run >= 2048 or xoffs + run == 0: break
            x += xoffs
            for _ in range(run):
                if ptr + 2 > len(buf): break
                val = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
                if val:
                    r = ((val >> 10) & 0x1F) << 3
                    g = ((val >>  5) & 0x1F) << 3
                    b = ( val        & 0x1F) << 3
                    px = (y * w + x) * 4
                    pixels[px] = r; pixels[px+1] = g; pixels[px+2] = b; pixels[px+3] = 0xFF
                x += 1
    return Image.frombytes('RGBA', (w, h), bytes(pixels)), flags

# CC art
ccart = UopArchive(CC / 'artLegacyMUL.uop')
buf = ccart.get_by_name(f'build/artlegacymul/{ART_ID:08}.tga')
ccart.close()
if buf:
    img, flags = decode_cc_art(buf)
    bbox = img.getbbox()
    img.resize((img.width*4, img.height*4), Image.NEAREST).save(OUT / f'cc_{ITEM_ID}.png')
    print(f'CC tile {ITEM_ID}: {img.width}x{img.height}  alpha={bbox}  flags=0x{flags:X}')

# EC legacy DDS
lg = UopArchive(EC / 'LegacyTexture.uop')
ent = lg.by_hash.get(hash_name(f'build/tileartlegacy/{ITEM_ID:08}.dds'))
lg.close()
if ent:
    dds = lg.read(ent) if False else None
    lg = UopArchive(EC / 'LegacyTexture.uop')
    dds = lg.read(ent)
    lg.close()
    try:
        img = Image.open(io.BytesIO(dds)).convert('RGBA')
        bbox = img.getbbox()
        img.resize((img.width*4, img.height*4), Image.NEAREST).save(OUT / f'ec_legacy_{ITEM_ID}.png')
        print(f'EC legacy {ITEM_ID}: {img.width}x{img.height}  alpha={bbox}')
    except Exception as e:
        print(f'EC legacy decode failed: {e}')

# EC HD DDS
hd = UopArchive(EC / 'Texture.uop')
ent = hd.by_hash.get(hash_name(f'build/worldart/{ITEM_ID:08}.dds'))
if ent:
    try:
        img = Image.open(io.BytesIO(hd.read(ent))).convert('RGBA')
        bbox = img.getbbox()
        img.resize((img.width*2, img.height*2), Image.NEAREST).save(OUT / f'ec_hd_{ITEM_ID}.png')
        print(f'EC HD {ITEM_ID}: {img.width}x{img.height}  alpha={bbox}')
    except Exception as e:
        print(f'EC HD decode failed: {e}')
hd.close()

# tileart record header (look at IsPartialHue flag etc.)
ta = UopArchive(EC / 'tileart.uop')
ent = ta.by_hash.get(hash_name(f'build/tileart/{ART_ID:08}.bin'))
if ent:
    rec = ta.read(ent)
    flags_ec    = struct.unpack_from('<Q', rec, 0x39)[0]
    flags_leg   = struct.unpack_from('<Q', rec, 0x41)[0]
    ec_layout   = struct.unpack_from('<6i', rec, 0x4D)
    lg_layout   = struct.unpack_from('<6i', rec, 0x65)
    print(f'tileart record: flags_EC=0x{flags_ec:016X}  flags_legacy=0x{flags_leg:016X}')
    print(f'  EcImage     = {ec_layout}')
    print(f'  LegacyImage = {lg_layout}')
ta.close()

print(f'\nOutput dir: {OUT.resolve()}')
