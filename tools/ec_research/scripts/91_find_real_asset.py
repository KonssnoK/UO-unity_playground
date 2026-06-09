"""Reverse-lookup: from the EC's string_dictionary, find ALL strings that
contain '1414' (or 1410-1414) and resolve where each one is physically
stored in the UOP archives. This tells us where EC's roof for tile 1414
actually lives — independent of our `build/worldart/{tile_id}.dds`
assumption."""
import sys, struct, io
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
hd = UopArchive(EC / 'Texture.uop')
lt = UopArchive(EC / 'LegacyTexture.uop')
sd_arc = UopArchive(EC / 'string_dictionary.uop')
sd = sd_arc.read(list(sd_arc.by_hash.values())[0])

# Decode all length-prefixed strings
strings = []
pos = 0
while pos + 2 < len(sd):
    n = struct.unpack_from('<H', sd, pos)[0]
    if n == 0 or n > 1024:
        pos += 1; continue
    if pos + 2 + n > len(sd):
        break
    tb = sd[pos+2:pos+2+n]
    if all(0x20 <= b < 0x80 or b in (0x09, 0x0a) for b in tb):
        strings.append(tb.decode('utf-8'))
        pos += 2 + n; continue
    pos += 1

print(f"strings in dictionary: {len(strings)}")

# Find every string containing 1408..1414 padded eight wide OR plain
SEP = chr(92)
def path_to_uop_key(tga_path: str) -> str:
    """Convert 'Data\\WorldArt\\00001414_Castle_Roof.tga' to the UOP entry key.
    Empirically: lowercase, replace backslashes with /, replace .tga with .dds,
    drop leading 'data/'."""
    p = tga_path.replace(SEP, '/').lower()
    if p.startswith('data/'):
        p = 'build/' + p[5:]
    if p.endswith('.tga'):
        p = p[:-4] + '.dds'
    return p

# Build by tile_ids 1408..1414: scan dictionary for those numbers as substrings
for tile in range(1408, 1415):
    needle = f"{tile:08}"
    print(f"\n=== tile {tile} (needle '{needle}') ===")
    matches = [s for s in strings if needle in s and s.endswith('.tga')]
    if not matches:
        # Try unpadded
        matches = [s for s in strings if f"\\{tile}." in s or f"\\{tile}_" in s]
    if not matches:
        print(f"  no string match")
        continue
    for s in matches[:8]:
        key = path_to_uop_key(s)
        h = hash_name(key)
        hd_hit = hd.by_hash.get(h)
        lt_hit = lt.by_hash.get(h)
        loc = []
        if hd_hit: loc.append(f"HD size={hd_hit.decompressed_size}")
        if lt_hit: loc.append(f"legacy size={lt_hit.decompressed_size}")
        loc = ', '.join(loc) if loc else 'NOT FOUND'
        print(f"  string: {s}")
        print(f"    -> key: {key}")
        print(f"       hash 0x{h:x}: {loc}")

# Also: for each tile, locate ALL strings starting with 'Data\WorldArt\'+'{tile_id}'
# (helps if the actual roof is at e.g. 'Data\WorldArt\00001414_Castle_Roof.tga'
# which won't hash the same as 'build/worldart/00001414.dds').
print("\n\n=== full directory listing for tiles 1408..1418 ===")
for tile in range(1408, 1419):
    needle1 = f"\\{tile:08}_"
    needle2 = f"\\{tile:08}."
    matches = [s for s in strings if (needle1 in s or needle2 in s) and s.endswith('.tga')]
    if matches:
        print(f"\ntile {tile}:")
        for m in matches:
            print(f"  {m}")

hd.close(); lt.close(); sd_arc.close()
