"""Cross-correlate every byte/int/float offset in the EC tileart record
against every field in CC's tiledata.mul (StaticTilesNew format).
For each (ec_offset, cc_field, dtype) triple, count the % of tiles where
the values match. Print the strongest correlations as Markdown.
"""
from __future__ import annotations
import struct, sys
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
TILEDATA = CC / "tiledata.mul"


def load_cc_static_tiledata():
    """Returns dict[item_id] -> {field_name: value} using StaticTilesNew layout.

    File layout (modern, u64 flags):
      Land:    512 groups × (4 hdr + 32 × 30 bytes land entry)  = 493568 bytes
      Static:  ~512 groups × (4 hdr + 32 × 41 bytes static entry)
    """
    data = TILEDATA.read_bytes()
    land_block = 512 * (4 + 32 * 30)
    print(f"tiledata.mul {len(data)} bytes; static block starts @{land_block}")

    statics: dict[int, dict] = {}
    p = land_block
    group_size = 4 + 32 * 41
    group_idx = 0
    while p + group_size <= len(data):
        # 4-byte group header (skip)
        entry_p = p + 4
        for i in range(32):
            item_id = group_idx * 32 + i
            flags    = struct.unpack_from('<Q',  data, entry_p)[0]
            weight   = struct.unpack_from('<B',  data, entry_p + 8)[0]
            layer    = struct.unpack_from('<B',  data, entry_p + 9)[0]
            count    = struct.unpack_from('<i',  data, entry_p + 10)[0]
            animid   = struct.unpack_from('<H',  data, entry_p + 14)[0]
            hue      = struct.unpack_from('<H',  data, entry_p + 16)[0]
            light    = struct.unpack_from('<H',  data, entry_p + 18)[0]
            height   = struct.unpack_from('<B',  data, entry_p + 20)[0]
            name_raw = bytes(data[entry_p + 21: entry_p + 41])
            name = name_raw.rstrip(b'\x00').decode('ascii', errors='replace')
            statics[item_id] = dict(
                flags=flags, weight=weight, layer=layer, count=count,
                animid=animid, hue=hue, light=light, height=height, name=name
            )
            entry_p += 41
        p += group_size
        group_idx += 1
    print(f"loaded {len(statics)} static tile entries")
    return statics


def load_ec_tileart_offsets(max_offsets=0x80):
    """Returns dict[art_id] -> bytes(payload[:max_offsets])"""
    arc = UopArchive(EC / 'tileart.uop')
    out: dict[int, bytes] = {}
    for e in arc.entries:
        try:
            p = arc.read(e)
        except Exception:
            continue
        if len(p) < max_offsets: continue
        try:
            tid = struct.unpack_from('<I', p, 6)[0]
        except struct.error:
            continue
        out[tid] = p[:max_offsets]
    arc.close()
    print(f"loaded {len(out)} EC tileart records")
    return out


def main():
    cc = load_cc_static_tiledata()
    ec = load_ec_tileart_offsets()
    # cc is keyed by item_id (0..N). EC's record is keyed by art_id (= item_id + 0x4000 for statics).
    # Build merged pairs.
    pairs = []
    for art_id, ec_bytes in ec.items():
        if art_id < 0x4000: continue        # only statics
        item_id = art_id - 0x4000
        if item_id not in cc: continue
        pairs.append((item_id, ec_bytes, cc[item_id]))
    print(f"{len(pairs)} tile pairs matched")

    # For each EC offset, build u8/u16/u32/i32/u64 candidate values
    ec_offsets = list(range(0x00, 0x80))

    # CC numeric fields to test
    cc_field_extractors = {
        "flags": lambda c: c['flags'],
        "weight": lambda c: c['weight'],
        "layer": lambda c: c['layer'],
        "count": lambda c: c['count'],
        "animid": lambda c: c['animid'],
        "hue": lambda c: c['hue'],
        "light": lambda c: c['light'],
        "height": lambda c: c['height'],
    }

    formats = [
        ("u8",  'B', 1),
        ("u16", 'H', 2),
        ("u32", 'I', 4),
        ("i32", 'i', 4),
        ("u64", 'Q', 8),
        ("f32", 'f', 4),
    ]

    # For each EC offset × dtype, build per-tile value list once
    ec_vals = {}
    for o in ec_offsets:
        for fname, fcode, fsize in formats:
            if o + fsize > 0x80: continue
            key = (o, fname)
            vals = []
            for item_id, eb, cc in pairs:
                vals.append(struct.unpack_from('<' + fcode, eb, o)[0])
            ec_vals[key] = vals

    cc_vals = {}
    for cname, ext in cc_field_extractors.items():
        cc_vals[cname] = [ext(p[2]) for p in pairs]

    print()
    print("# Strong correlations on NON-DEFAULT CC values (filters out hue=0 noise)")
    print()
    rows = []
    for (o, fname), evals in ec_vals.items():
        if len(set(evals)) <= 2: continue
        for cname, cvals in cc_vals.items():
            if len(set(cvals)) <= 1: continue
            # only pairs where CC value is non-zero
            nz_pairs = [(a, b) for a, b in zip(evals, cvals) if b != 0]
            if len(nz_pairs) < 100: continue
            matches = sum(1 for a, b in nz_pairs if a == b)
            pct = matches / len(nz_pairs) * 100
            if pct >= 50:
                rows.append((pct, o, fname, cname, matches, len(nz_pairs)))
    rows.sort(reverse=True)
    print("  EC offset | dtype | CC field   | match % | matches/non-zero pairs")
    print("  ----------+-------+------------+---------+----------------------")
    for pct, o, fname, cname, m, t in rows[:60]:
        print(f"  0x{o:02X}      | {fname:5} | {cname:10} | {pct:6.2f}% | {m}/{t}")

    # Also: known good baseline check (StringDictionary @0x02 should vary, TileID @0x06 should equal item_id+0x4000)
    print()
    print("## Sanity: TileID at 0x06 == art_id?")
    matches = sum(1 for (item_id, eb, _) in pairs
                  if struct.unpack_from('<I', eb, 0x06)[0] == item_id + 0x4000)
    print(f"  {matches}/{len(pairs)} (expected 100%)")

    # Pairs filtered to where CC field != 0 — 30-70% range (subtype matches)
    print()
    print("# Partial correlations 30-70% on non-zero CC values (subtype/conditional fields)")
    print()
    rows = []
    for (o, fname), evals in ec_vals.items():
        if len(set(evals)) <= 2: continue
        for cname, cvals in cc_vals.items():
            if len(set(cvals)) <= 1: continue
            nz_pairs = [(a, b) for a, b in zip(evals, cvals) if b != 0]
            if len(nz_pairs) < 100: continue
            matches = sum(1 for a, b in nz_pairs if a == b)
            pct = matches / len(nz_pairs) * 100
            if 30 <= pct < 50:
                rows.append((pct, o, fname, cname, matches, len(nz_pairs)))
    rows.sort(reverse=True)
    for pct, o, fname, cname, m, t in rows[:20]:
        print(f"  0x{o:02X}      | {fname:5} | {cname:10} | {pct:6.2f}% | {m}/{t}")

    # FLAG BITS — compare each EC u64 offset's set bits with CC flags' set bits
    print()
    print("# Flag bit overlap — EC u64 offsets vs CC flags (Jaccard over bit-sets)")
    print()
    flag_rows = []
    cc_flags = [p[2]['flags'] for p in pairs]
    for o in ec_offsets:
        if o + 8 > 0x80: continue
        ev = [struct.unpack_from('<Q', eb, o)[0] for _, eb, _ in pairs]
        # only interesting if multi-value
        if len(set(ev)) < 5: continue
        # bit-wise: count tiles where ec_val & cc_flag != 0 (any bit overlap)
        any_overlap = sum(1 for a, b in zip(ev, cc_flags) if a != 0 and b != 0 and (a & b) != 0)
        exact = sum(1 for a, b in zip(ev, cc_flags) if a == b and a != 0)
        # AND across all tiles -> common bits
        and_mask = 0xFFFFFFFFFFFFFFFF
        or_mask = 0
        for a, b in zip(ev, cc_flags):
            if a == 0 or b == 0: continue
            and_mask &= (a & b)
            or_mask  |= (a & b)
        if any_overlap < 100: continue
        flag_rows.append((any_overlap, exact, o, and_mask, or_mask))
    flag_rows.sort(reverse=True)
    for any_overlap, exact, o, and_m, or_m in flag_rows[:15]:
        print(f"  0x{o:02X}  exact={exact:>5}  any_bit_overlap={any_overlap:>5}  "
              f"AND-mask=0x{and_m:016X}  OR-mask=0x{or_m:016X}")

    # Specific deep-dive: 0x18 vs weight (currently labeled "Old id")
    print()
    print("# 0x18 deep-dive: u8 byte vs CC.weight, per-tile histogram")
    print()
    o = 0x18
    pairs_view = [(struct.unpack_from('<B', eb, o)[0], p[2]['weight']) for _, eb, p in
                  [(item_id, eb, (item_id, eb, cc)) for item_id, eb, cc in pairs]]
    # fix: re-build correctly
    pairs_view = []
    for item_id, eb, cc in pairs:
        ev = struct.unpack_from('<B', eb, o)[0]
        pairs_view.append((ev, cc['weight']))
    # cases where they differ
    diff = [(a, b) for a, b in pairs_view if a != b]
    print(f"  matched: {len(pairs_view) - len(diff)} / {len(pairs_view)}")
    print(f"  examples of differences:")
    diff_counter = Counter(diff)
    for (ev, cv), c in diff_counter.most_common(10):
        print(f"    EC[0x18]={ev}  vs  CC.weight={cv}   ({c} tiles)")


if __name__ == "__main__":
    main()
