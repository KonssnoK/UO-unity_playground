"""Dump EcImage / LegacyImage 6-int fields for representative tiles to see
if our parsing matches DDS sprite positions."""
import struct, sys, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

samples = [
    (16384, 'tile 0 / Rattan_Wall sprite 461'),
    (16385, 'tile 1 / Rattan_Wall sprite 461'),
    (16584, 'tile 200 / Stone wall (Mage_Stone_Walls)'),
    (16640, 'tile 256 / Jungle_Walls'),
    (22137, 'tile 5753 / Marble wall'),
    (8251,  'land tile 8251 (no art_id offset)'),
    (16432, 'tile 48 / roof or floor (small id)'),
    (16444, 'tile 60'),
    (16500, 'tile 116'),
]

tileart = UopArchive(EC / 'tileart.uop')
lg      = UopArchive(EC / 'LegacyTexture.uop')
hd      = UopArchive(EC / 'Texture.uop')

print(f"{'art_id':<8}{'EcImage':<28}{'LegacyImage':<28}{'lg_dds':<12}{'lg_visible':<14}desc")
for art_id, desc in samples:
    h = hash_name(f'build/tileart/{art_id:08}.bin')
    e = tileart.by_hash.get(h)
    ec_str = lg_str = '(no record)'
    lg_sz = lg_vis = '-'
    if e:
        p = tileart.read(e)
        ec_str = str(struct.unpack_from('<6i', p, 0x4D))
        lg_str = str(struct.unpack_from('<6i', p, 0x65))
    item_id = art_id - 0x4000 if art_id >= 0x4000 else art_id
    lk = f'build/tileartlegacy/{item_id:08}.dds'
    le = lg.by_hash.get(hash_name(lk))
    if le:
        try:
            img = Image.open(io.BytesIO(lg.read(le))).convert('RGBA')
            lg_sz = f'{img.width}x{img.height}'
            bbox = img.getbbox()
            if bbox:
                lg_vis = f'{bbox[2]-bbox[0]}x{bbox[3]-bbox[1]}@{bbox[0]},{bbox[1]}'
        except Exception as ex:
            lg_sz = f'err:{ex}'
    print(f'{art_id:<8}{ec_str:<28}{lg_str:<28}{lg_sz:<12}{lg_vis:<14}{desc}')

tileart.close(); lg.close(); hd.close()
