"""Scan tileart for consecutive tiles that share the same StringDictionary
offset (= same name = likely a CC multi-piece grouped into one HD asset).
If 5649/5650 banner theory holds, we'll see lots of pairs/triplets where
the first has an HD entry and subsequent ones don't."""
import struct, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
ta = UopArchive(EC / 'tileart.uop')
hd = UopArchive(EC / 'Texture.uop')

# Build: tile_id -> (string_dict_off, has_hd)
tile_info = {}
for art_id in range(0x4000, 0x4000 + 16384):
    item_id = art_id - 0x4000
    rec = ta.by_hash.get(hash_name(f'build/tileart/{art_id:08}.bin'))
    if rec is None: continue
    p = ta.read(rec)
    if len(p) < 0x80: continue
    sd_off = struct.unpack_from('<I', p, 0x02)[0]
    has_hd = hash_name(f'build/worldart/{item_id:08}.dds') in hd.by_hash
    tile_info[item_id] = (sd_off, has_hd)

print(f"loaded {len(tile_info)} statics with tileart records")

# Group consecutive tile_ids that share the same string_dict_off
groups = []
sorted_ids = sorted(tile_info)
i = 0
while i < len(sorted_ids):
    start = sorted_ids[i]
    sd, hd_flag = tile_info[start]
    j = i + 1
    while (j < len(sorted_ids)
           and sorted_ids[j] == sorted_ids[j-1] + 1
           and tile_info[sorted_ids[j]][0] == sd):
        j += 1
    if j > i + 1:  # group of >= 2
        groups.append([(tid, tile_info[tid][1]) for tid in sorted_ids[i:j]])
    i = j

print(f"\nConsecutive same-name groups: {len(groups)}")
print(f"Total tiles in groups: {sum(len(g) for g in groups)}")

# Distribution: how many of each size?
from collections import Counter
size_dist = Counter(len(g) for g in groups)
print(f"\nGroup size distribution: {sorted(size_dist.items())[:15]}")

# Of the groups, how many follow the "only first has HD" pattern?
first_only_hd = 0
all_have_hd = 0
none_have_hd = 0
mixed = 0
for g in groups:
    hd_flags = [hd_flag for _, hd_flag in g]
    if hd_flags[0] and not any(hd_flags[1:]):
        first_only_hd += 1
    elif all(hd_flags):
        all_have_hd += 1
    elif not any(hd_flags):
        none_have_hd += 1
    else:
        mixed += 1

print(f"\nWithin same-name groups:")
print(f"  ONLY FIRST has HD: {first_only_hd}  (banner pattern)")
print(f"  ALL have HD: {all_have_hd}")
print(f"  NONE have HD: {none_have_hd}")
print(f"  MIXED (other): {mixed}")

# Print some examples of the "first only HD" pattern
print(f"\nFirst-only-HD examples (first 15):")
n = 0
for g in groups:
    hd_flags = [hd_flag for _, hd_flag in g]
    if hd_flags[0] and not any(hd_flags[1:]):
        ids = [tid for tid, _ in g]
        sd = tile_info[ids[0]][0]
        print(f"  tile_ids {ids}  (sd_off={sd})")
        n += 1
        if n >= 15: break

ta.close(); hd.close()
