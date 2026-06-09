"""Find which functions reference each of the 4 SUB_9_7 group-name strings
in Ghidra's dump. The string symbols we saw earlier:
  's_WorldArt_00cb8a3c'
  's_WorldArt\\ref_00cb8a48'
  's_TileArtLegacy_00cb8a58'
  's_TileArtEnhanced_00cb8a68'
"""
import json
from pathlib import Path

ROOT = Path(r'C:\src\ClassicUO')
d = json.load(open(ROOT / 'tools/ghidra/ghidra_dump.json'))
sref = d['string_to_referring_functions']

print('=== Group-name string -> consumer fns ===')
for k in sorted(sref):
    if any(g in k for g in ('WorldArt', 'TileArtLegacy', 'TileArtEnhanced')):
        print(f'  {k!r}  ->  {sref[k][:6]}')

# Also show what each consumer fn does (signature + first ~25 lines)
fns_to_inspect = set()
for k, lst in sref.items():
    if any(g in k for g in ('WorldArt', 'TileArtLegacy', 'TileArtEnhanced')):
        fns_to_inspect.update(lst)

print()
print(f'=== Decompiles for {len(fns_to_inspect)} consumer fns ===')
for fn in d['decompiled_functions']:
    if fn['entry'] in fns_to_inspect:
        code = fn['decompiled']
        # Just first lines + lines mentioning the group names
        lines = code.splitlines()
        print(f'\n--- {fn["entry"]}  ({fn["name"]}) ---')
        for line in lines[:35]:
            print(f'  {line}')
        print('  ...')
        for line in lines[35:]:
            if any(g in line for g in ('WorldArt', 'TileArtLegacy', 'TileArtEnhanced')):
                print(f'  >> {line.strip()}')
