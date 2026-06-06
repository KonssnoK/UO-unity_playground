"""Verified: the absorbed-tile relationship is encoded by SHARED FILE-PATH STRINGS
in string_dictionary.uop. Tiles whose tileart record's sd_off resolves to the
same string entry are members of the same logical sprite. If any tile in such a
group has an HD asset (Texture.uop build/worldart/{id}.dds) and this tile does
not, this tile is absorbed by the HD-bearing sibling.

This script re-derives the absorbed map purely from string_dictionary lookups
(no 'consecutive tile_id' heuristic) and reports how it covers the 5649/5650
banner case plus other groups."""
import struct, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

ta = UopArchive(EC / 'tileart.uop')
hd = UopArchive(EC / 'Texture.uop')
sd_arc = UopArchive(EC / 'string_dictionary.uop')
sd = sd_arc.read(list(sd_arc.by_hash.values())[0])

# Pre-decode all length-prefixed strings in string_dictionary.
# Format: (u16 length, utf8 bytes)*, packed back-to-back, with some 1-byte
# pad slots in between (entries always start on the next position past the
# previous string's end).
entries_by_start = {}    # byte_offset_of_length -> text
pos = 0
while pos + 2 < len(sd):
    n = struct.unpack_from('<H', sd, pos)[0]
    if n == 0 or n > 1024:
        pos += 1; continue
    text_start = pos + 2
    if text_start + n > len(sd):
        break
    try:
        text_bytes = sd[text_start:text_start + n]
        if all(0x20 <= b < 0x80 or b in (0x09, 0x0a) for b in text_bytes):
            text = text_bytes.decode('utf-8')
            entries_by_start[pos] = text
            pos = text_start + n
            continue
    except UnicodeDecodeError:
        pass
    pos += 1

# Sort entries to enable nearest-start lookup for any sd_off (sd_off may point
# into the middle of the entry's bytes — observed offsets land a few bytes
# past the length prefix).
sorted_starts = sorted(entries_by_start)
def lookup(off):
    import bisect
    i = bisect.bisect_right(sorted_starts, off) - 1
    if i < 0: return None
    start = sorted_starts[i]
    text = entries_by_start[start]
    # offset must fall within [start, start + 2 + len(text)]
    if off > start + 2 + len(text):
        return None
    return text

# Walk every static tile (art_id 0x4000..0x7FFF), bucket by source string.
groups_by_name = defaultdict(list)   # name -> list of tile_ids
hd_owners = set()
for art_id in range(0x4000, 0x4000 + 16384):
    item_id = art_id - 0x4000
    e = ta.by_hash.get(hash_name(f'build/tileart/{art_id:08}.bin'))
    if e is None: continue
    p = ta.read(e)
    if len(p) < 0x08: continue
    sd_off = struct.unpack_from('<I', p, 0x02)[0]
    name = lookup(sd_off)
    if name is None: continue
    groups_by_name[name].append(item_id)
    if hash_name(f'build/worldart/{item_id:08}.dds') in hd.by_hash:
        hd_owners.add(item_id)

# Find groups with at least one HD owner and >=2 members.
multi_groups = {n: ids for n, ids in groups_by_name.items() if len(ids) > 1}
hd_groups   = {n: ids for n, ids in multi_groups.items() if any(t in hd_owners for t in ids)}

print(f"total distinct source-string groups: {len(groups_by_name)}")
print(f"multi-member groups (>=2 tiles share string): {len(multi_groups)}")
print(f"...of which at least one member has HD: {len(hd_groups)}")

# Absorbed tile = group member that lacks HD while at least one sibling has HD.
absorbed = set()
for ids in hd_groups.values():
    owners = [t for t in ids if t in hd_owners]
    if not owners: continue
    for t in ids:
        if t not in hd_owners:
            absorbed.add(t)
print(f"\nABSORBED tile count (authoritative, via string_dictionary): {len(absorbed)}")

# Sanity: 5650 should be absorbed by 5649.
print(f"\n5649 has HD? {5649 in hd_owners}")
print(f"5650 has HD? {5650 in hd_owners}")
print(f"5650 absorbed? {5650 in absorbed}")
print(f"5648 absorbed? {5648 in absorbed}")
print(f"5651 absorbed? {5651 in absorbed}")

# Show the banner group in full
for name, ids in hd_groups.items():
    if 5649 in ids:
        print(f"\nGroup containing 5649:")
        print(f"  name: {name}")
        print(f"  members: {sorted(ids)}")
        print(f"  HD owners: {sorted([t for t in ids if t in hd_owners])}")
        print(f"  absorbed:  {sorted([t for t in ids if t not in hd_owners])}")
        break

# Compare against script 86's heuristic (consecutive-id pairs).
# Build the script-86 set:
tile_info = {}
for art_id in range(0x4000, 0x4000 + 16384):
    item_id = art_id - 0x4000
    e = ta.by_hash.get(hash_name(f'build/tileart/{art_id:08}.bin'))
    if e is None: continue
    p = ta.read(e)
    if len(p) < 0x80: continue
    sd_off = struct.unpack_from('<I', p, 0x02)[0]
    has_hd = item_id in hd_owners
    tile_info[item_id] = (sd_off, has_hd)
heur_absorbed = set()
sorted_ids = sorted(tile_info)
i = 0
while i < len(sorted_ids):
    sd, _ = tile_info[sorted_ids[i]]
    j = i + 1
    while (j < len(sorted_ids) and sorted_ids[j] == sorted_ids[j-1] + 1
           and tile_info[sorted_ids[j]][0] == sd):
        j += 1
    grp = sorted_ids[i:j]
    if j > i + 1:
        flags = [tile_info[t][1] for t in grp]
        if flags[0] and not any(flags[1:]):
            for t in grp[1:]:
                heur_absorbed.add(t)
    i = j

print(f"\nheuristic (script 86) absorbed: {len(heur_absorbed)}")
print(f"authoritative (string-dict) absorbed: {len(absorbed)}")
print(f"  authoritative ⊇ heuristic? {heur_absorbed.issubset(absorbed)}")
print(f"  extra in authoritative: {len(absorbed - heur_absorbed)}")
print(f"  missing from authoritative: {len(heur_absorbed - absorbed)}")

ta.close(); hd.close(); sd_arc.close()
