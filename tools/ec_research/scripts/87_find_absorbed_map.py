"""Hunt for an explicit absorbed-tile / replacement map in EC archives.

Strategy: tile 5649 'absorbs' 5650 (and same pattern for 18 other first-only-HD
groups script 86 found). If EC stores this somewhere, we should see ONE of:

  (a) A field in the absorbed tileart record (5650) that distinguishes it from
      a regular tile — zero-size EcImage/LegacyImage rectangle, a flag bit,
      a pointer back to 5649, a 'hidden' marker.
  (b) A field on the absorber (5649) that lists 5650 as a child — extended
      record length, an array of child tile_ids, a sibling pointer.
  (c) A separate UOP entry (a table file in tileart.uop / Texture.uop /
      Stringtable*.uop) keyed by tile_id or by sd_off.
  (d) An entry inside the StringDictionary referenced by sd_off — keys like
      'replaces', 'absorbs', 'spritegroup', etc.

We test all four against the 19 first-only-HD groups script 86 identified."""
import struct, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
ta = UopArchive(EC / 'tileart.uop')
hd = UopArchive(EC / 'Texture.uop')


def get_tileart(art_id):
    e = ta.by_hash.get(hash_name(f'build/tileart/{art_id:08}.bin'))
    if e is None:
        return None
    return ta.read(e)


def has_hd(item_id):
    return hash_name(f'build/worldart/{item_id:08}.dds') in hd.by_hash


# Rebuild the first-only-HD pair list (script 86 output, re-derived locally)
tile_info = {}
for art_id in range(0x4000, 0x4000 + 16384):
    item_id = art_id - 0x4000
    p = get_tileart(art_id)
    if p is None or len(p) < 0x80:
        continue
    sd_off = struct.unpack_from('<I', p, 0x02)[0]
    tile_info[item_id] = (sd_off, has_hd(item_id))

groups = []
sorted_ids = sorted(tile_info)
i = 0
while i < len(sorted_ids):
    sd = tile_info[sorted_ids[i]][0]
    j = i + 1
    while (j < len(sorted_ids)
           and sorted_ids[j] == sorted_ids[j-1] + 1
           and tile_info[sorted_ids[j]][0] == sd):
        j += 1
    if j > i + 1:
        groups.append(sorted_ids[i:j])
    i = j

absorber_absorbed = []
for g in groups:
    flags = [tile_info[t][1] for t in g]
    if flags[0] and not any(flags[1:]):
        absorber_absorbed.append((g[0], g[1:]))

print(f"first-only-HD groups: {len(absorber_absorbed)}")
print(f"first few: {absorber_absorbed[:5]}")

# ----------------------------------------------------------------------------
# (a) Field-by-field diff of absorber vs absorbed across all 19 pairs.
#     Look for fields that consistently differ in the same direction.
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(a) Per-byte diff: are there bytes that DIFFER in every absorber/absorbed pair?")
diffs_count = Counter()       # byte_offset -> how often it differs
diffs_sample = defaultdict(list)
sizes_pair = []
for absorber, absorbed_list in absorber_absorbed:
    pa = get_tileart(0x4000 + absorber)
    if pa is None:
        continue
    for absorbed in absorbed_list:
        pb = get_tileart(0x4000 + absorbed)
        if pb is None:
            continue
        sizes_pair.append((len(pa), len(pb)))
        # Skip TileID (0x06..0x09) and StringDictOff (0x02..0x05 are equal anyway)
        # and OldId (0x18..0x1B) which is obviously tile-specific.
        skip = set(range(0x06, 0x0A)) | set(range(0x18, 0x1C))
        n = min(len(pa), len(pb))
        for off in range(n):
            if off in skip:
                continue
            if pa[off] != pb[off]:
                diffs_count[off] += 1
                if len(diffs_sample[off]) < 3:
                    diffs_sample[off].append((absorber, absorbed, pa[off], pb[off]))

total_pairs = sum(len(absorbed_list) for _, absorbed_list in absorber_absorbed)
print(f"total absorber/absorbed pairs analyzed: {total_pairs}")
print()
print("byte offsets that differ in >= 80% of pairs (excluding obvious tile-id/oldid):")
sig = [(off, cnt) for off, cnt in diffs_count.items() if cnt >= total_pairs * 0.8]
for off, cnt in sorted(sig):
    sample = diffs_sample[off][0]
    print(f"  0x{off:04X}  {cnt:3d}/{total_pairs}  e.g. tile{sample[0]}={sample[2]:#04x} tile{sample[1]}={sample[3]:#04x}")
if not sig:
    print("  (none — absorber/absorbed records are byte-identical outside TileID/OldId)")

print()
print("record-length pairs (absorber_len, absorbed_len):")
print(f"  unique: {Counter(sizes_pair).most_common(8)}")

# ----------------------------------------------------------------------------
# (b) Check EcImage / LegacyImage. Banner is the canonical case — is 5650's
#     EcImage / LegacyImage zero-area (X1==X0 or Y1==Y0)?
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(b) Are absorbed tiles flagged via EcImage / LegacyImage rectangles?")
def img_rect(p, off):
    if len(p) < off + 24:
        return None
    return struct.unpack_from('<6i', p, off)

zero_ec = zero_leg = nonzero = 0
for _, absorbed_list in absorber_absorbed:
    for absorbed in absorbed_list:
        p = get_tileart(0x4000 + absorbed)
        if p is None:
            continue
        ec_r = img_rect(p, 0x4D)
        lg_r = img_rect(p, 0x65)
        ec_zero = ec_r is not None and (ec_r[2] == ec_r[0] or ec_r[3] == ec_r[1])
        lg_zero = lg_r is not None and (lg_r[2] == lg_r[0] or lg_r[3] == lg_r[1])
        if ec_zero: zero_ec += 1
        if lg_zero: zero_leg += 1
        if not ec_zero and not lg_zero:
            nonzero += 1
print(f"  absorbed tiles with zero-area EcImage:    {zero_ec}/{total_pairs}")
print(f"  absorbed tiles with zero-area LegacyImage: {zero_leg}/{total_pairs}")
print(f"  absorbed tiles with both rectangles nonzero: {nonzero}/{total_pairs}")

# Print actual EcImage / LegacyImage for the 5649/5650 case to be concrete.
print()
print("  5649 vs 5650 image rectangles:")
for tid in (5649, 5650):
    p = get_tileart(0x4000 + tid)
    print(f"    tile {tid}: EcImage={img_rect(p, 0x4D)}  LegacyImage={img_rect(p, 0x65)}")

# ----------------------------------------------------------------------------
# (c) Is there an extra/unusual UOP entry that could encode a replacement map?
#     Enumerate non-tileart/non-dds entries in the EC UOP archives.
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(c) Non-asset entries in EC archives (potential index tables)")
# Try common candidate filenames against tileart.uop + Texture.uop hashes.
candidates = [
    "build/tileart/tileart.idx",
    "build/tileart/replacements.bin",
    "build/tileart/groups.bin",
    "build/tileart/sprite_groups.bin",
    "build/worldart/index.bin",
    "build/worldart/replacements.bin",
    "build/worldart/groups.bin",
    "build/tileart/links.bin",
    "build/tileart/absorbed.bin",
]
for c in candidates:
    h = hash_name(c)
    for label, arc in [("tileart.uop", ta), ("Texture.uop", hd)]:
        if h in arc.by_hash:
            print(f"  HIT  {label}: {c}")

# Also: examine the per-archive entry counts and sniff a few non-conforming
# filenames (UOP archives store name-hashes only, but file-format header
# sometimes carries the original).
ta_total = len(ta.by_hash)
hd_total = len(hd.by_hash)
# Count how many tileart.uop entries match the build/tileart/{art_id:08}.bin
# pattern — any that don't are interesting.
matched = 0
for art_id in range(0x4000, 0x4000 + 16384):
    if hash_name(f'build/tileart/{art_id:08}.bin') in ta.by_hash:
        matched += 1
print(f"  tileart.uop entries: total={ta_total} matching build/tileart/{{art_id:08}}.bin = {matched}")
print(f"  Texture.uop entries: total={hd_total}")
# Difference = leftover entries that are NOT plain per-tile records.
print(f"  tileart.uop UNACCOUNTED entries: {ta_total - matched}")

# ----------------------------------------------------------------------------
# (d) Look at the property/sub-section after 0x7D for absorbed vs absorber.
#     If absorbed has FEWER properties or is missing a key sub-block (such as
#     image data) that's a real distinguishing marker.
# ----------------------------------------------------------------------------
print()
print("=" * 78)
print("(d) Property-count byte @ 0x7D — does it differ between absorber/absorbed?")
mismatch = same = 0
examples = []
for absorber, absorbed_list in absorber_absorbed:
    pa = get_tileart(0x4000 + absorber)
    if pa is None or len(pa) <= 0x7D:
        continue
    cnt_a = pa[0x7D]
    for absorbed in absorbed_list:
        pb = get_tileart(0x4000 + absorbed)
        if pb is None or len(pb) <= 0x7D:
            continue
        cnt_b = pb[0x7D]
        if cnt_a != cnt_b:
            mismatch += 1
            if len(examples) < 5:
                examples.append((absorber, absorbed, cnt_a, cnt_b, len(pa), len(pb)))
        else:
            same += 1
print(f"  property-count differs: {mismatch}/{total_pairs}")
print(f"  property-count identical: {same}/{total_pairs}")
for ex in examples:
    print(f"    e.g. absorber {ex[0]} cnt={ex[2]} len={ex[4]}  vs absorbed {ex[1]} cnt={ex[3]} len={ex[5]}")

ta.close(); hd.close()
