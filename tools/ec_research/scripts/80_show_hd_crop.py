"""For tiles 2 and 3: show the HD DDS WITH a red rect at the LegacyImage
coords, AND extract just the cropped piece and save it separately, so we
can see what the rect actually picks out of the HD image.
"""
import struct, sys, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image, ImageDraw

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = Path(__file__).resolve().parent.parent / "out" / "hd_crop"; OUT.mkdir(parents=True, exist_ok=True)

TILES = [2, 3, 6, 7, 8, 16, 26]   # range with HD entries

tileart = UopArchive(EC / 'tileart.uop')
hd      = UopArchive(EC / 'Texture.uop')
lg      = UopArchive(EC / 'LegacyTexture.uop')

for tile in TILES:
    art = 0x4000 + tile
    he = hd.by_hash.get(hash_name(f'build/worldart/{tile:08}.dds'))
    if he is None:
        print(f"tile {tile}: no HD entry, skip"); continue
    rec_ent = tileart.by_hash.get(hash_name(f'build/tileart/{art:08}.bin'))
    if rec_ent is None:
        print(f"tile {tile}: no tileart record"); continue
    rec = tileart.read(rec_ent)
    ec_layout = struct.unpack_from('<6i', rec, 0x4D)
    lg_layout = struct.unpack_from('<6i', rec, 0x65)
    print(f"\n=== tile {tile} ===")
    print(f"  EcImage     = {ec_layout}")
    print(f"  LegacyImage = {lg_layout}")

    img = Image.open(io.BytesIO(hd.read(he))).convert('RGBA')
    print(f"  HD canvas: {img.width}x{img.height}")

    # Save the HD image with overlay rects
    overlay = img.copy()
    d = ImageDraw.Draw(overlay)
    # red = EcImage rect
    ex0, ey0, ex1, ey1, _, _ = ec_layout
    if ex1 > ex0 and ey1 > ey0:
        d.rectangle([ex0, ey0, ex1-1, ey1-1], outline=(255,0,0,255), width=1)
    # magenta = LegacyImage rect
    lx0, ly0, lx1, ly1, _, _ = lg_layout
    if lx1 > lx0 and ly1 > ly0:
        d.rectangle([lx0, ly0, lx1-1, ly1-1], outline=(255,0,255,255), width=1)
    overlay = overlay.resize((overlay.width*2, overlay.height*2), Image.NEAREST)
    d = ImageDraw.Draw(overlay)
    d.text((2, 2),  f"tile {tile} HD ({img.width}x{img.height})", fill=(255,255,0))
    d.text((2, 14), f"red=EcImage  magenta=LegacyImage", fill=(255,255,0))
    overlay.save(OUT / f"tile{tile:02}_hd_overlay.png")

    # Save just the CROPPED LegacyImage piece
    if lx1 > lx0 and ly1 > ly0:
        crop = img.crop((lx0, ly0, lx1, ly1))
        crop_up = crop.resize((crop.width*4, crop.height*4), Image.NEAREST)
        crop_up.save(OUT / f"tile{tile:02}_hd_crop_LegacyImage_{crop.width}x{crop.height}.png")
        print(f"  Cropped HD via LegacyImage: {crop.width}x{crop.height}")

    # Also save the EC LEGACY DDS for direct visual compare
    le = lg.by_hash.get(hash_name(f'build/tileartlegacy/{tile:08}.dds'))
    if le:
        leg = Image.open(io.BytesIO(lg.read(le))).convert('RGBA')
        leg.resize((leg.width*4, leg.height*4), Image.NEAREST).save(OUT / f"tile{tile:02}_legacy_for_compare.png")
        print(f"  Legacy DDS for compare: {leg.width}x{leg.height}")

tileart.close(); hd.close(); lg.close()
print(f"\nOutput dir: {OUT.resolve()}")
