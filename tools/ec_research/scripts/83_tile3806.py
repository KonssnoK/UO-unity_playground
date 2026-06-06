"""Extract tile 3806 (the gravestone the user pointed at) in all forms:
  - CC art (from artLegacyMUL.uop)
  - EC legacy DDS
  - EC HD DDS
With overlay rectangles showing EcImage, LegacyImage, alpha bboxes.
Goal: understand visually WHAT the EcImage rect points to in the HD canvas
for THIS specific tile."""
import struct, sys, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image, ImageDraw

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
OUT = Path(__file__).resolve().parent.parent / "out" / "tile3806"
OUT.mkdir(parents=True, exist_ok=True)

TILE = 3806
ART  = 0x4000 + TILE   # 20190

def decode_cc(buf):
    if len(buf) < 12: return None
    w = struct.unpack_from('<H', buf, 4)[0]
    h = struct.unpack_from('<H', buf, 6)[0]
    line_offs = struct.unpack_from(f'<{h}H', buf, 8)
    ds = 8 + h*2
    px = bytearray(w*h*4)
    for y in range(h):
        if line_offs[y] == 0 and y != 0: continue
        ptr = ds + line_offs[y]*2; x = 0
        while True:
            if ptr+4 > len(buf): break
            xo = struct.unpack_from('<H', buf, ptr)[0]; ptr+=2
            rn = struct.unpack_from('<H', buf, ptr)[0]; ptr+=2
            if xo+rn >= 2048 or xo+rn == 0: break
            x += xo
            for _ in range(rn):
                if ptr+2 > len(buf): break
                v = struct.unpack_from('<H', buf, ptr)[0]; ptr+=2
                if v:
                    r=((v>>10)&0x1F)<<3; g=((v>>5)&0x1F)<<3; b=(v&0x1F)<<3
                    p=(y*w+x)*4; px[p]=r; px[p+1]=g; px[p+2]=b; px[p+3]=0xFF
                x += 1
    return Image.frombytes('RGBA', (w,h), bytes(px))


# Dump tileart record
tileart = UopArchive(EC / 'tileart.uop')
e = tileart.by_hash[hash_name(f'build/tileart/{ART:08}.bin')]
p = tileart.read(e)
tileart.close()
ec_lay = struct.unpack_from('<6i', p, 0x4D)
lg_lay = struct.unpack_from('<6i', p, 0x65)
print(f"tile {TILE} (art_id {ART}):")
print(f"  EcImage     = {ec_lay}")
print(f"  LegacyImage = {lg_lay}")

# CC art
cc = UopArchive(CC / 'artLegacyMUL.uop')
buf = cc.get_by_name(f'build/artlegacymul/{ART:08}.tga')
cc.close()
if buf:
    cci = decode_cc(buf)
    bbox = cci.getbbox() or (0,0,cci.width,cci.height)
    cci_up = cci.resize((cci.width*4, cci.height*4), Image.NEAREST)
    d = ImageDraw.Draw(cci_up)
    d.rectangle([bbox[0]*4, bbox[1]*4, bbox[2]*4-1, bbox[3]*4-1], outline=(0,255,255), width=2)
    d.text((2,2), f"CC {cci.width}x{cci.height} bbox={bbox}", fill=(255,255,0))
    cci_up.save(OUT / 'cc.png')
    print(f"  CC: {cci.width}x{cci.height}, alpha bbox={bbox}")

# HD DDS
hd = UopArchive(EC / 'Texture.uop')
he = hd.by_hash.get(hash_name(f'build/worldart/{TILE:08}.dds'))
if he:
    dds = hd.read(he)
    img = Image.open(io.BytesIO(dds)).convert('RGBA')
    bbox = img.getbbox() or (0,0,img.width,img.height)
    img2 = img.copy()
    d = ImageDraw.Draw(img2)
    # cyan = alpha bbox
    d.rectangle([bbox[0], bbox[1], bbox[2]-1, bbox[3]-1], outline=(0,255,255), width=1)
    # red = EcImage rect as-is (top-down interpretation)
    if ec_lay[2] > ec_lay[0] and ec_lay[3] > ec_lay[1]:
        d.rectangle([ec_lay[0], ec_lay[1], ec_lay[2], ec_lay[3]], outline=(255,0,0), width=1)
    img2 = img2.resize((img2.width*2, img2.height*2), Image.NEAREST)
    d = ImageDraw.Draw(img2)
    d.text((2,2),  f"HD {img.width}x{img.height}  alpha={bbox}", fill=(255,255,0))
    d.text((2,16), f"red=EcImage rect {ec_lay[0]},{ec_lay[1]},{ec_lay[2]},{ec_lay[3]}", fill=(255,0,0))
    img2.save(OUT / 'hd.png')
    print(f"  HD: {img.width}x{img.height}, alpha bbox={bbox}")
hd.close()

# Legacy DDS
lg = UopArchive(EC / 'LegacyTexture.uop')
le = lg.by_hash.get(hash_name(f'build/tileartlegacy/{TILE:08}.dds'))
if le:
    dds = lg.read(le)
    img = Image.open(io.BytesIO(dds)).convert('RGBA')
    bbox = img.getbbox() or (0,0,img.width,img.height)
    img2 = img.copy()
    d = ImageDraw.Draw(img2)
    d.rectangle([bbox[0], bbox[1], bbox[2]-1, bbox[3]-1], outline=(0,255,255), width=1)
    if lg_lay[2] > lg_lay[0] and lg_lay[3] > lg_lay[1]:
        d.rectangle([lg_lay[0], lg_lay[1], lg_lay[2], lg_lay[3]], outline=(255,0,255), width=1)
    img2 = img2.resize((img2.width*4, img2.height*4), Image.NEAREST)
    d = ImageDraw.Draw(img2)
    d.text((2,2),  f"Legacy {img.width}x{img.height}  alpha={bbox}", fill=(255,255,0))
    d.text((2,14), f"magenta=LegacyImage rect {lg_lay[0]},{lg_lay[1]},{lg_lay[2]},{lg_lay[3]}", fill=(255,0,255))
    img2.save(OUT / 'legacy.png')
    print(f"  Legacy: {img.width}x{img.height}, alpha bbox={bbox}")
lg.close()
print(f"\nOutput: {OUT.resolve()}")
