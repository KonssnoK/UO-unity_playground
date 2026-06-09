"""Generate PNGs for tiles 2 and 3 showing CC, EC legacy (with rect), EC HD (with rect).
For HD we use EcImage; for legacy we use LegacyImage. Green rect = CC alpha bbox
(reference — CC has no explicit stored offset); Red rect = the tileart record's rect."""
import struct, sys, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image, ImageDraw

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
OUT = Path(__file__).resolve().parent.parent / "out" / "offsets_viz"
OUT.mkdir(parents=True, exist_ok=True)

TILES = [2, 3]


def decode_cc_art(buf):
    if len(buf) < 12: return None
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
    return Image.frombytes('RGBA', (w, h), bytes(pixels))


def render(img, rect, color, label, scale=4):
    out = img.copy()
    d = ImageDraw.Draw(out)
    if rect is not None and rect[2] > 0 and rect[3] > 0:
        x, y, w, h = rect
        d.rectangle([x, y, x + w - 1, y + h - 1], outline=color, width=1)
    if scale > 1:
        out = out.resize((out.width * scale, out.height * scale), Image.NEAREST)
        d = ImageDraw.Draw(out)
    d.text((2, 2), label, fill=color)
    return out


tileart = UopArchive(EC / 'tileart.uop')
lg      = UopArchive(EC / 'LegacyTexture.uop')
hd      = UopArchive(EC / 'Texture.uop')
ccart   = UopArchive(CC / 'artLegacyMUL.uop')

for tile in TILES:
    art = 0x4000 + tile
    rec = tileart.read(tileart.by_hash[hash_name(f'build/tileart/{art:08}.bin')])
    ec_layout = struct.unpack_from('<6i', rec, 0x4D)
    lg_layout = struct.unpack_from('<6i', rec, 0x65)
    print(f"\ntile {tile}: EcImage={ec_layout}  LegacyImage={lg_layout}")

    # CC art
    cc_buf = ccart.get_by_name(f'build/artlegacymul/{art:08}.tga')
    if cc_buf:
        cc_img = decode_cc_art(cc_buf)
        if cc_img:
            bbox = cc_img.getbbox() or (0, 0, cc_img.width, cc_img.height)
            r = (bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1])
            render(cc_img, r, (0, 255, 0), f"CC {cc_img.width}x{cc_img.height}  bbox={r}").save(
                OUT / f'tile{tile:02}_cc.png')

    # EC legacy DDS with LegacyImage rect
    le = lg.by_hash.get(hash_name(f'build/tileartlegacy/{tile:08}.dds'))
    if le:
        img = Image.open(io.BytesIO(lg.read(le))).convert('RGBA')
        x0, y0, x1, y1, ax, ay = lg_layout
        r = (x0, y0, max(0, x1 - x0), max(0, y1 - y0))
        bbox = img.getbbox() or (0, 0, img.width, img.height)
        cc_eq = (bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1])
        out = img.copy()
        d = ImageDraw.Draw(out)
        # Red = LegacyImage rect; Cyan = actual alpha bbox
        if cc_eq[2] > 0 and cc_eq[3] > 0:
            d.rectangle([cc_eq[0], cc_eq[1], cc_eq[0]+cc_eq[2]-1, cc_eq[1]+cc_eq[3]-1], outline=(0,255,255), width=1)
        if r[2] > 0 and r[3] > 0:
            d.rectangle([r[0], r[1], r[0]+r[2]-1, r[1]+r[3]-1], outline=(255,0,0), width=1)
        out = out.resize((out.width*4, out.height*4), Image.NEAREST)
        d = ImageDraw.Draw(out)
        d.text((2, 2),  f"EC Legacy {img.width}x{img.height}", fill=(255,255,0))
        d.text((2, 14), f"red=record {r}", fill=(255, 0, 0))
        d.text((2, 26), f"cyan=alpha bbox {cc_eq}", fill=(0, 255, 255))
        d.text((2, 38), f"anchor=({ax},{ay})", fill=(255, 0, 0))
        out.save(OUT / f'tile{tile:02}_ec_legacy.png')
        print(f"  EC legacy {img.width}x{img.height}  alpha={cc_eq}  rect={r}")

    # EC HD DDS with EcImage rect
    he = hd.by_hash.get(hash_name(f'build/worldart/{tile:08}.dds'))
    if he:
        try:
            img = Image.open(io.BytesIO(hd.read(he))).convert('RGBA')
            x0, y0, x1, y1, ax, ay = ec_layout
            r = (x0, y0, max(0, x1 - x0), max(0, y1 - y0))
            bbox = img.getbbox() or (0, 0, img.width, img.height)
            alpha_bbox = (bbox[0], bbox[1], bbox[2]-bbox[0], bbox[3]-bbox[1])
            out = img.copy()
            d = ImageDraw.Draw(out)
            if alpha_bbox[2] > 0 and alpha_bbox[3] > 0:
                d.rectangle([alpha_bbox[0], alpha_bbox[1], alpha_bbox[0]+alpha_bbox[2]-1, alpha_bbox[1]+alpha_bbox[3]-1], outline=(0,255,255), width=1)
            if r[2] > 0 and r[3] > 0:
                d.rectangle([r[0], r[1], r[0]+r[2]-1, r[1]+r[3]-1], outline=(255,0,0), width=1)
            out = out.resize((out.width*2, out.height*2), Image.NEAREST)
            d = ImageDraw.Draw(out)
            d.text((2, 2),  f"EC HD {img.width}x{img.height}", fill=(255,255,0))
            d.text((2, 14), f"red=record {r}", fill=(255, 0, 0))
            d.text((2, 26), f"cyan=alpha bbox {alpha_bbox}", fill=(0, 255, 255))
            d.text((2, 38), f"anchor=({ax},{ay})", fill=(255, 0, 0))
            out.save(OUT / f'tile{tile:02}_ec_hd.png')
            print(f"  EC HD {img.width}x{img.height}  alpha={alpha_bbox}  rect={r}")
        except Exception as ex:
            print(f"  EC HD decode failed: {ex}")
    else:
        print(f"  no EC HD")

tileart.close(); lg.close(); hd.close(); ccart.close()
print(f"\nOutput dir: {OUT.resolve()}")
