"""For each header offset, print a value-histogram and a CC-flag-bit
correspondence map. Goals:
  1. See which offsets actually carry per-tile data (multi-value)
  2. For 0x39 (Flags EC) and 0x41 (Flags Legacy), map each EC bit to its
     best-correlated CC bit so we can build a translation table.
"""
from __future__ import annotations
import struct, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
TILEDATA = CC / "tiledata.mul"


def load_cc():
    data = TILEDATA.read_bytes()
    p = 512 * (4 + 32 * 30)
    out = {}
    gi = 0
    gsize = 4 + 32 * 41
    while p + gsize <= len(data):
        ep = p + 4
        for i in range(32):
            item_id = gi * 32 + i
            out[item_id] = dict(
                flags    = struct.unpack_from('<Q', data, ep)[0],
                weight   = struct.unpack_from('<B', data, ep + 8)[0],
                layer    = struct.unpack_from('<B', data, ep + 9)[0],
                count    = struct.unpack_from('<i', data, ep + 10)[0],
                animid   = struct.unpack_from('<H', data, ep + 14)[0],
                hue      = struct.unpack_from('<H', data, ep + 16)[0],
                light    = struct.unpack_from('<H', data, ep + 18)[0],
                height   = struct.unpack_from('<B', data, ep + 20)[0],
            )
            ep += 41
        p += gsize
        gi += 1
    return out


def load_ec():
    arc = UopArchive(EC / 'tileart.uop')
    out = {}
    for e in arc.entries:
        try:
            p = arc.read(e)
        except Exception:
            continue
        if len(p) < 0x80: continue
        try:
            tid = struct.unpack_from('<I', p, 6)[0]
        except struct.error:
            continue
        out[tid] = p[:0x80]
    arc.close()
    return out


def main():
    cc = load_cc()
    ec = load_ec()
    pairs = []
    for art_id, eb in ec.items():
        if art_id < 0x4000: continue
        item_id = art_id - 0x4000
        if item_id not in cc: continue
        pairs.append((item_id, eb, cc[item_id]))
    print(f"# {len(pairs)} static pairs\n")

    # ---------- 1. Per-offset u8 histograms (only multi-value offsets) ----------
    print("## Per-offset value distributions (only offsets with >=3 unique u8 values)")
    print()
    interesting = []
    for o in range(0x80):
        c = Counter(struct.unpack_from('<B', eb, o)[0] for _, eb, _ in pairs)
        if len(c) >= 3:
            top = c.most_common(10)
            interesting.append((o, c, top))
    for o, c, top in interesting:
        s = ', '.join(f"{v}({n})" for v, n in top)
        print(f"  0x{o:02X}  ({len(c)} unique)  top: {s}")

    # ---------- 2. EC flags @ 0x39 / 0x41 vs CC.flags bit mapping ----------
    print()
    print("## Bit-by-bit correlation: EC flags @ 0x39 vs CC.flags")
    print()
    for ec_off, label in ((0x39, "Flags EC"), (0x41, "Flags Legacy")):
        ev = [struct.unpack_from('<Q', eb, ec_off)[0] for _, eb, _ in pairs]
        cv = [p[2]['flags'] for p in pairs]

        # For each EC bit, find best matching CC bit
        print(f"### {label} (@0x{ec_off:02X})")
        # Compute bit set frequencies and bit-pair counts
        ec_bit_set = [0] * 64
        cc_bit_set = [0] * 64
        cross = [[0]*64 for _ in range(64)]
        for a, b in zip(ev, cv):
            for i in range(64):
                ai = (a >> i) & 1
                bi = (b >> i) & 1
                if ai: ec_bit_set[i] += 1
                if bi: cc_bit_set[i] += 1
        for a, b in zip(ev, cv):
            for i in range(64):
                ai = (a >> i) & 1
                if not ai: continue
                for j in range(64):
                    if (b >> j) & 1:
                        cross[i][j] += 1

        N = len(pairs)
        # For each EC bit set in >=20 tiles, find the CC bit with highest co-occurrence
        for i in range(64):
            if ec_bit_set[i] < 20: continue
            best_j = max(range(64), key=lambda j: cross[i][j])
            best_overlap = cross[i][best_j]
            ec_freq = ec_bit_set[i]
            cc_freq = cc_bit_set[best_j]
            # Jaccard: overlap / (ec_only + cc_only + overlap)
            union = ec_freq + cc_freq - best_overlap
            jaccard = best_overlap / union if union else 0
            if jaccard < 0.5: continue
            print(f"    EC bit {i:>2} ({ec_freq:>5} set) ↔ CC bit {best_j:>2} ({cc_freq:>5} set)  "
                  f"overlap={best_overlap:>5}  Jaccard={jaccard:.2f}")
        print()


if __name__ == "__main__":
    main()
