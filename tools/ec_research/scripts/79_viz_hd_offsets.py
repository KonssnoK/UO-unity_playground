"""Visualize tiles 2 and 3 across CC, EC legacy, EC HD with overlays:
  - cyan = alpha bbox
  - red  = EcImage rect (X0,Y0,X1,Y1) from 0x4D
  - magenta = LegacyImage rect from 0x65
  - yellow text  = the 6-int values + scaling-relevant fields
"""
import struct, sys, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image, ImageDraw

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
OUT = Path(__file__).resolve().parent.parent / "out" / "hd_offsets"; OUT.mkdir(parents=True, exist_ok=True)

TILES = [2, 3]


def decode_cc(buf):
    if len(buf) < 12: return None
    w = struct.unpack_from('<H', buf, 4)[0]
    h = struct.unpack_from('<H', buf, 6)[0]
    line_offs = struct.unpack_from(f'<{h}H', buf, 8)
    data = 8 + h * 2
    px = bytearray(w * h * 4)
    for y in range(h):
        if line_offs[y] == 0 and y != 0: continue
        ptr = data + line_offs[y] * 2; x = 0
        while True:
            if ptr + 4 > len(buf): break
            xo = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
            rn = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
            if xo + rn >= 2048 or xo + rn == 0: break
            x += xo
            for _ in range(rn):
                if ptr + 2 > len(buf): break
                v = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
                if v:
                    r = ((v>>10)&0x1F)<<3; g = ((v>>5)&0x1F)<<3; b = (v&0x1F)<<3
                    p = (y*w + x)*4
                    px[p]=r; px[p+1]=g; px[p+2]=b; px[p+3]=0xFF
                x += 1
    return Image.frombytes('RGBA', (w, h), bytes(px))


def annotate(img, rects, labels, scale=4):
    out = img.copy()
    d = ImageDraw.Draw(out)
    for r, col in rects:
        if r is None or r[2] <= 0 or r[3] <= 0: continue
        d.rectangle([r[0], r[1], r[0]+r[2]-1, r[1]+r[3]-1], outline=col, width=1)
    out = out.resize((out.width*scale, out.height*scale), Image.NEAREST)
    d = ImageDraw.Draw(out)
    for i, (text, col) in enumerate(labels):
        d.text((2, 2 + i*12), text, fill=col)
    return out


tileart = UopArchive(EC / 'tileart.uop')
hd  = UopArchive(EC / 'Texture.uop')
lg  = UopArchive(EC / 'LegacyTexture.uop')
ccart = UopArchive(CC / 'artLegacyMUL.uop')

for tile in TILES:
    art = 0x4000 + tile
    rec = tileart.read(tileart.by_hash[hash_name(f'build/tileart/{art:08}.bin')])
    ec_layout = struct.unpack_from('<6i', rec, 0x4D)
    lg_layout = struct.unpack_from('<6i', rec, 0x65)
    f_0c = struct.unpack_from('<f', rec, 0x0C)[0]
    f_10 = struct.unpack_from('<f', rec, 0x10)[0]
    f_25 = struct.unpack_from('<f', rec, 0x25)[0]
    print(f"\n=== tile {tile} ===")
    print(f"  EcImage     = {ec_layout}    (X0,Y0,X1,Y1, anchorX, anchorY)")
    print(f"  LegacyImage = {lg_layout}")
    print(f"  0x0C={f_0c:.3f}   0x10={f_10:.3f}   0x25={f_25:.3f}")

    # CC
    cc_buf = ccart.get_by_name(f'build/artlegacymul/{art:08}.tga')
    if cc_buf:
        cc_img = decode_cc(cc_buf)
        if cc_img:
            bbox = cc_img.getbbox() or (0, 0, cc_img.width, cc_img.height)
            rects = [
                ((bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]), (0,255,255,255)),
            ]
            labels = [
                (f"CC {cc_img.width}x{cc_img.height}  bbox={bbox[0]},{bbox[1]},{bbox[2]-bbox[0]}x{bbox[3]-bbox[1]}", (255,255,0)),
            ]
            annotate(cc_img, rects, labels).save(OUT / f'tile{tile:02}_cc.png')
            print(f"  CC: bbox={bbox}")

    # EC legacy
    le = lg.by_hash.get(hash_name(f'build/tileartlegacy/{tile:08}.dds'))
    if le:
        img = Image.open(io.BytesIO(lg.read(le))).convert('RGBA')
        bbox = img.getbbox() or (0, 0, img.width, img.height)
        rects = [
            ((bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]), (0,255,255,255)),
            ((lg_layout[0], lg_layout[1], max(0, lg_layout[2]-lg_layout[0]), max(0, lg_layout[3]-lg_layout[1])), (255,0,255,255)),
        ]
        labels = [
            (f"EC Legacy {img.width}x{img.height}", (255,255,0)),
            (f"cyan=alpha bbox", (0,255,255)),
            (f"magenta=LegacyImage {lg_layout[0]},{lg_layout[1]},{lg_layout[2]-lg_layout[0]}x{lg_layout[3]-lg_layout[1]}  anchor=({lg_layout[4]},{lg_layout[5]})", (255,0,255)),
        ]
        annotate(img, rects, labels).save(OUT / f'tile{tile:02}_ec_legacy.png')
        print(f"  EC Legacy: bbox={bbox}")

    # EC HD
    he = hd.by_hash.get(hash_name(f'build/worldart/{tile:08}.dds'))
    if he:
        try:
            img = Image.open(io.BytesIO(hd.read(he))).convert('RGBA')
            bbox = img.getbbox() or (0, 0, img.width, img.height)
            rects = [
                ((bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1]), (0,255,255,255)),
                ((ec_layout[0], ec_layout[1], max(0, ec_layout[2]-ec_layout[0]), max(0, ec_layout[3]-ec_layout[1])), (255,0,0,255)),
            ]
            labels = [
                (f"EC HD {img.width}x{img.height}", (255,255,0)),
                (f"cyan=alpha bbox", (0,255,255)),
                (f"red=EcImage {ec_layout[0]},{ec_layout[1]},{ec_layout[2]-ec_layout[0]}x{ec_layout[3]-ec_layout[1]}  anchor=({ec_layout[4]},{ec_layout[5]})", (255,0,0)),
            ]
            annotate(img, rects, labels, scale=2).save(OUT / f'tile{tile:02}_ec_hd.png')
            print(f"  EC HD: bbox={bbox}")
        except Exception as e:
            print(f"  EC HD decode failed: {e}")

tileart.close(); hd.close(); lg.close(); ccart.close()
print(f"\nOutput dir: {OUT.resolve()}")
