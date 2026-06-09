"""Inspect tile 5649 — the 'left banner' user says isn't tinting under HD."""
import sys, io, struct
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")

TILE = 5649
ART = 0x4000 + TILE  # 21649

# CC TileFlag bit 17 = PartialHue
PARTIAL_HUE_BIT = 1 << 17

# CC tiledata.mul
TD = (CC / "tiledata.mul").read_bytes()
land_block = 512 * (4 + 32 * 30)
static_offset_in_block = (TILE // 32) * (4 + 32 * 41) + 4 + (TILE % 32) * 41
abs_offset = land_block + static_offset_in_block
flags = struct.unpack_from('<Q', TD, abs_offset)[0]
weight = TD[abs_offset + 8]
print(f"CC tiledata for tile {TILE} (art_id {ART}):")
print(f"  flags = 0x{flags:016X}")
print(f"  IsPartialHue (bit 17) = {bool(flags & PARTIAL_HUE_BIT)}")
print(f"  weight = {weight}")

# EC tileart record
ta = UopArchive(EC / 'tileart.uop')
e = ta.by_hash.get(hash_name(f'build/tileart/{ART:08}.bin'))
if e:
    p = ta.read(e)
    flags_ec = struct.unpack_from('<Q', p, 0x39)[0]
    flags_leg = struct.unpack_from('<Q', p, 0x41)[0]
    ec_lay = struct.unpack_from('<6i', p, 0x4D)
    lg_lay = struct.unpack_from('<6i', p, 0x65)
    print()
    print(f"EC tileart record:")
    print(f"  FlagsEC = 0x{flags_ec:016X}  (bit 17 = {bool(flags_ec & PARTIAL_HUE_BIT)})")
    print(f"  FlagsLeg = 0x{flags_leg:016X}  (bit 17 = {bool(flags_leg & PARTIAL_HUE_BIT)})")
    print(f"  EcImage     = {ec_lay}")
    print(f"  LegacyImage = {lg_lay}")
ta.close()

# Texture/mask presence
hd = UopArchive(EC / 'Texture.uop')
lg = UopArchive(EC / 'LegacyTexture.uop')
print()
print("Texture/mask availability:")
for label, arc, prefix in [("HD color", hd, "build/worldart/"), ("HD mask", hd, "build/worldart/"),
                            ("Legacy color", lg, "build/tileartlegacy/"), ("Legacy mask", lg, "build/tileartlegacy/")]:
    if "mask" in label:
        n = 1_000_000 + TILE
    else:
        n = TILE
    key = f"{prefix}{n:08}.dds"
    ent = arc.by_hash.get(hash_name(key))
    if ent:
        dds = arc.read(ent)
        try:
            img = Image.open(io.BytesIO(dds)).convert('RGBA')
            print(f"  {label}: {key}  -  {img.width}x{img.height}")
        except Exception as ex:
            print(f"  {label}: {key}  -  decode failed: {ex}")
    else:
        print(f"  {label}: {key}  -  MISS")
hd.close(); lg.close()
