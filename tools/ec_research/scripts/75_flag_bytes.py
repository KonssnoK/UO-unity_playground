"""Test: is EC tileart Flags EC@0x39 / Legacy@0x41 the same u64 as CC.flags?
For each tile, compute (EC u64) ^ (CC.flags) and report the XOR-mask
histogram — bits that differ across many tiles indicate semantic
remapping; bits that always agree indicate a 1:1 mapping.
"""
from __future__ import annotations
import struct, sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
TILEDATA = CC / "tiledata.mul"


def load_cc():
    data = TILEDATA.read_bytes()
    p = 512 * (4 + 32 * 30); out = {}; gi = 0; gsize = 4 + 32 * 41
    while p + gsize <= len(data):
        ep = p + 4
        for i in range(32):
            out[gi*32+i] = struct.unpack_from('<Q', data, ep)[0]
            ep += 41
        p += gsize; gi += 1
    return out


def load_ec():
    arc = UopArchive(EC / 'tileart.uop')
    out = {}
    for e in arc.entries:
        try: p = arc.read(e)
        except Exception: continue
        if len(p) < 0x80: continue
        try: tid = struct.unpack_from('<I', p, 6)[0]
        except struct.error: continue
        out[tid] = p[:0x80]
    arc.close(); return out


def main():
    cc_flags = load_cc()
    ec_recs  = load_ec()
    pairs = []
    for art_id, eb in ec_recs.items():
        if art_id < 0x4000: continue
        item_id = art_id - 0x4000
        if item_id not in cc_flags: continue
        pairs.append((item_id, eb, cc_flags[item_id]))

    print(f"{len(pairs)} static pairs\n")

    for label, off in (("Flags EC", 0x39), ("Flags Legacy", 0x41)):
        print(f"## {label} (@0x{off:02X})  vs  CC.flags")
        ev = [struct.unpack_from('<Q', eb, off)[0] for _, eb, _ in pairs]
        cv = [cf for _, _, cf in pairs]
        exact = sum(1 for a, b in zip(ev, cv) if a == b)
        low_byte_eq = sum(1 for a, b in zip(ev, cv) if (a & 0xFF) == (b & 0xFF))
        low_word_eq = sum(1 for a, b in zip(ev, cv) if (a & 0xFFFF) == (b & 0xFFFF))
        low_dw_eq   = sum(1 for a, b in zip(ev, cv) if (a & 0xFFFFFFFF) == (b & 0xFFFFFFFF))
        # XOR histogram: shows bits that disagree
        xor_bit_counts = [0] * 64
        for a, b in zip(ev, cv):
            x = a ^ b
            for i in range(64):
                if (x >> i) & 1: xor_bit_counts[i] += 1
        print(f"  exact equal           : {exact:>6} / {len(pairs)}")
        print(f"  low byte (8 bits) eq  : {low_byte_eq:>6} / {len(pairs)}  ({100*low_byte_eq/len(pairs):.1f}%)")
        print(f"  low word (16) eq      : {low_word_eq:>6} / {len(pairs)}  ({100*low_word_eq/len(pairs):.1f}%)")
        print(f"  low dword (32) eq     : {low_dw_eq:>6} / {len(pairs)}  ({100*low_dw_eq/len(pairs):.1f}%)")
        print(f"  bit-disagreement histogram (out of {len(pairs)}):")
        for i in range(32):
            if xor_bit_counts[i] > 0:
                pct = 100 * xor_bit_counts[i] / len(pairs)
                print(f"    bit {i:>2}: {xor_bit_counts[i]:>5} differ ({pct:5.1f}%)")
        print()


if __name__ == "__main__":
    main()
