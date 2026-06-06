"""For each byte offset in the tileart record header (0x00..0x7C), walk
EVERY tileart record and collect:
  - per-offset value distribution as u8 / u16 / u32 / i32 / f32
  - top values, range
A wide value-range or many unique values hints at real per-tile data;
constants suggest a default. Output as Markdown to stdout.
"""
from __future__ import annotations
import struct, sys
from collections import Counter
from pathlib import Path
from statistics import mean, median

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

# Header offsets we care about
HEADER_OFFSETS = list(range(0x00, 0x7D))   # full header

def safe_unpack(payload: bytes, off: int, fmt: str):
    size = struct.calcsize(fmt)
    if off + size > len(payload): return None
    return struct.unpack_from('<' + fmt, payload, off)[0]


def main():
    arc = UopArchive(EC / 'tileart.uop')
    # For each offset, store a counter per dtype
    u8_counters  : dict[int, Counter] = {o: Counter() for o in HEADER_OFFSETS}
    u32_counters : dict[int, Counter] = {o: Counter() for o in HEADER_OFFSETS}
    f32_counters : dict[int, Counter] = {o: Counter() for o in HEADER_OFFSETS}
    # Track tile ids that show each value at offset 0x0A (the "unknown bool")
    sample_tiles : dict[int, dict[int, list[int]]] = {o: {} for o in HEADER_OFFSETS}

    total = 0
    for e in arc.entries:
        try:
            payload = arc.read(e)
        except Exception:
            continue
        if len(payload) < 0x7D: continue
        try:
            tile_id = struct.unpack_from('<I', payload, 6)[0]
        except struct.error:
            continue
        total += 1
        for o in HEADER_OFFSETS:
            v8  = safe_unpack(payload, o, 'B')
            v32 = safe_unpack(payload, o, 'I')
            f32 = safe_unpack(payload, o, 'f')
            if v8  is not None: u8_counters[o][v8] += 1
            if v32 is not None: u32_counters[o][v32] += 1
            if f32 is not None:
                # round float for binning, keep raw too in samples
                bucket = round(f32, 4)
                f32_counters[o][bucket] += 1
            if v8 is not None:
                sample_tiles[o].setdefault(v8, []).append(tile_id)
    arc.close()

    print(f"# Per-offset stats from {total} tileart records\n")
    print("Format: offset | unique-u8 | unique-u32 | most-common-u32(count) | float-range | hint")
    print("-" * 110)
    for o in HEADER_OFFSETS:
        u8c = u8_counters[o]
        u32c = u32_counters[o]
        f32c = f32_counters[o]
        top_u32 = u32c.most_common(3)
        top_f32 = f32c.most_common(3)
        # Determine if it looks "real data" (multi-value) or constant
        const = len(u8c) == 1
        # Floats: pull min/max
        try:
            fmin = min(f32c)
            fmax = max(f32c)
        except ValueError:
            fmin = fmax = 0
        hint = ""
        if const:
            v = next(iter(u8c))
            hint = f"u8 always {v}"
        elif len(u32c) == 1:
            v = next(iter(u32c))
            hint = f"u32 always 0x{v:08X}"
        else:
            hint = f"u8 vals={len(u8c)}  u32 vals={len(u32c)}"
        print(f"  0x{o:02X} | {len(u8c):>5} | {len(u32c):>5} | "
              f"{str(top_u32[:2]):<48} | "
              f"f32 [{fmin:.2f}..{fmax:.2f}] top={str(top_f32[:1])[:30]} | {hint}")

    # Specific deep dives
    print()
    print("## Offsets with INTERESTING variation (suggests real per-tile data)")
    print()
    for o in HEADER_OFFSETS:
        unique = len(u32_counters[o])
        if unique == 1: continue
        unique_u8 = len(u8_counters[o])
        # Skip 0x06..0x09 (TileID, definitely varies)
        if 6 <= o < 10: continue
        # Skip 0x02..0x05 (StringDictionary, varies)
        if 2 <= o < 6: continue
        if unique_u8 >= 4 or unique >= 10:
            # Show top 8 values + a few example tiles
            print(f"### offset 0x{o:02X}  ({unique_u8} u8 / {unique} u32 unique)")
            top = u8_counters[o].most_common(8)
            print(f"  u8 top: " + ', '.join(f"{v}({c})" for v, c in top))
            # Float sample if varied
            top_f = f32_counters[o].most_common(4)
            print(f"  f32 top: " + ', '.join(f"{v}({c})" for v, c in top_f))
            print()


if __name__ == "__main__":
    main()
