"""Compare tile 5649 (banner — misplaced) with a normal correctly-rendered
tile to find what's special about the banner record."""
import struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

NORMAL_TILES = [3806, 100, 200]  # confirmed working tiles
WEIRD_TILES = [5649, 5650]       # banner

ta = UopArchive(EC / 'tileart.uop')


def dump_record(tile_id):
    art_id = 0x4000 + tile_id
    e = ta.by_hash.get(hash_name(f'build/tileart/{art_id:08}.bin'))
    if e is None:
        print(f"  tile {tile_id}: no record"); return None
    p = ta.read(e)
    fields = {
        'Version':        struct.unpack_from('<H', p, 0x00)[0],
        'StringDictOff':  struct.unpack_from('<I', p, 0x02)[0],
        'TileID':         struct.unpack_from('<I', p, 0x06)[0],
        'UnkBool@0x0A':   p[0x0A],
        'UnkByte@0x0B':   p[0x0B],
        'HeaderFloatA':   struct.unpack_from('<f', p, 0x0C)[0],
        'HeaderFloatB':   struct.unpack_from('<f', p, 0x10)[0],
        'OldId':          struct.unpack_from('<I', p, 0x18)[0],
        'Unk@0x1C':       struct.unpack_from('<I', p, 0x1C)[0],
        'Unk@0x20':       struct.unpack_from('<I', p, 0x20)[0],
        'Unk@0x24':       p[0x24],
        'Float@0x25':     struct.unpack_from('<f', p, 0x25)[0],
        'Unk@0x29':       struct.unpack_from('<I', p, 0x29)[0],
        'LightFloatA':    struct.unpack_from('<f', p, 0x2D)[0],
        'LightFloatB':    struct.unpack_from('<f', p, 0x31)[0],
        'Unk@0x35':       struct.unpack_from('<I', p, 0x35)[0],
        'FlagsEC':        struct.unpack_from('<Q', p, 0x39)[0],
        'FlagsLegacy':    struct.unpack_from('<Q', p, 0x41)[0],
        'Unk@0x49':       struct.unpack_from('<I', p, 0x49)[0],
        'EcImage':        struct.unpack_from('<6i', p, 0x4D),
        'LegacyImage':    struct.unpack_from('<6i', p, 0x65),
        'RecordLength':   len(p),
        'PropertyECCount': p[0x7D] if len(p) > 0x7D else 0,
    }
    return fields, p


print("="*90)
all_records = {}
for tile in NORMAL_TILES + WEIRD_TILES:
    print(f"\n--- tile {tile} ---")
    res = dump_record(tile)
    if res:
        fields, raw = res
        all_records[tile] = fields
        for k, v in fields.items():
            if k == 'FlagsEC' or k == 'FlagsLegacy' or k == 'OldId':
                print(f"  {k:>17}: 0x{v:016X}" if 'Flags' in k else f"  {k:>17}: 0x{v:08X}")
            elif k in ('EcImage', 'LegacyImage'):
                print(f"  {k:>17}: {v}")
            else:
                print(f"  {k:>17}: {v}")

# Now diff banner vs normal tiles per field
print()
print("="*90)
print("FIELD-BY-FIELD DIFFERENCES (banner 5649 vs others):")
banner = all_records.get(5649)
if banner:
    for tile, fields in all_records.items():
        if tile == 5649: continue
        print(f"\n  vs tile {tile}:")
        for key in banner:
            if banner[key] != fields[key]:
                print(f"    {key:>20}: banner={banner[key]}  other={fields[key]}")
ta.close()
