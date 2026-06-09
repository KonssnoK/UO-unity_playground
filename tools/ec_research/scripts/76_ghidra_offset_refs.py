"""Grep the Ghidra dump for `+ 0xNN` accesses on local pointers — these
often correspond to reads from struct fields. Report counts of each
offset accessed across all decompiled functions. Combined with our
header offset list, this tells us which fields the EC client ACTUALLY
reads (i.e. they're real semantic fields, not padding)."""
import json, re
from pathlib import Path

d = json.load(open(r'C:\src\ClassicUO\tools\ghidra\ghidra_dump.json'))
fns = d['decompiled_functions']

# Match patterns like `+ 0x39)` or `+ 57)` from decompiled C, both hex and decimal
hex_pat = re.compile(r'\+\s*0x([0-9A-Fa-f]+)\)')
dec_pat = re.compile(r'\+\s*(\d{1,3})\)')

# Header offsets of interest (header is 0x00..0x7C)
HEADER_RANGE = (0x00, 0x7C)

# Collect (offset -> [function_addrs that access it])
hits: dict[int, list[str]] = {}

for fn in fns:
    code = fn.get('decompiled') or ''
    if not code: continue
    found = set()
    for m in hex_pat.finditer(code):
        try: o = int(m.group(1), 16)
        except ValueError: continue
        if HEADER_RANGE[0] <= o <= HEADER_RANGE[1]:
            found.add(o)
    for m in dec_pat.finditer(code):
        try: o = int(m.group(1))
        except ValueError: continue
        if HEADER_RANGE[0] <= o <= HEADER_RANGE[1]:
            found.add(o)
    for o in found:
        hits.setdefault(o, []).append(fn['entry'])

print(f"Total fns scanned: {len(fns)}")
print()
print("# Offset access counts (how many fns reference each header offset)")
print()
print("offset | accesses | sample fn entries")
print("-------+----------+----------------")
for o in sorted(hits):
    addrs = hits[o]
    sample = ", ".join(addrs[:4])
    print(f"  0x{o:02X}   | {len(addrs):>5}   | {sample}")

# Targeted: only show offsets read by KNOWN tileart-handling functions
TILEART_FNS = {
    "0051a840": "HD tileart loader (uses '%08d_TileArt')",
    "0051af20": "Legacy tileart loader (uses '%08d_LegacyTileArt')",
    "005bfd30": "Helper called by both loaders",
    "00457b20": "Texture/asset resolver",
}

print()
print("# Offsets read SPECIFICALLY by tileart-handling fns")
print()
fn_by_entry = {f['entry']: f for f in fns}
for entry, label in TILEART_FNS.items():
    fn = fn_by_entry.get(entry)
    if not fn: continue
    code = fn.get('decompiled') or ''
    found = set()
    for m in hex_pat.finditer(code):
        try: o = int(m.group(1), 16)
        except ValueError: continue
        if HEADER_RANGE[0] <= o <= HEADER_RANGE[1]:
            found.add(o)
    for m in dec_pat.finditer(code):
        try: o = int(m.group(1))
        except ValueError: continue
        if HEADER_RANGE[0] <= o <= HEADER_RANGE[1]:
            found.add(o)
    print(f"### {entry}  — {label}")
    print(f"  offsets touched: {sorted(f'0x{o:02X}' for o in found)}")
    # Show the actual context for each offset in this fn
    for o in sorted(found):
        # find first context line
        for pat in (rf'\+\s*0x{o:X}\)', rf'\+\s*{o}\)'):
            m = re.search(pat, code)
            if m:
                start = max(0, m.start() - 100)
                end   = min(len(code), m.end() + 60)
                ctx = code[start:end].replace('\n', ' / ')
                print(f"    0x{o:02X}  ctx: ...{ctx}...")
                break
    print()
