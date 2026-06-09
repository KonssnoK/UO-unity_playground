from ec.uop import UopArchive, hash_name
from pathlib import Path
import os

ec = r'C:\Games\Electronic Arts\Ultima Online Enhanced'

# Exact path from EC binary strings (FUN_00402d80)
exact = 'data/gamedata/equipconv.csv'

# Variations to try
variants = [
    exact,
    exact.upper(),
    exact.title(),
    'Data/GameData/EquipConv.csv',
    exact.replace('/', '\\'),
    'data\\gamedata\\equipconv.csv',
    'gamedata/equipconv.csv',
    'equipconv.csv',
    'build/data/gamedata/equipconv.csv',
    'build/gamedata/equipconv.csv',
    'build/equipconv.csv',
]

hash_set = {}
for v in variants:
    norm = v.lower().replace('\\', '/')
    hash_set[hash_name(norm)] = norm
    try:
        hash_set[hash_name(v)] = v
    except Exception:
        pass

print('Hash candidates:')
for h, v in hash_set.items():
    print(f'  {h:016x}  {v!r}')

all_uops = []
for root, _, files in os.walk(ec):
    for f in files:
        if f.endswith('.uop'):
            all_uops.append(Path(root) / f)
print(f'Scanning {len(all_uops)} UOPs')

for p in all_uops:
    try:
        a = UopArchive(p)
    except Exception:
        continue
    for e in a.entries:
        if e.hash in hash_set:
            print(f'HIT {p.name} :: {hash_set[e.hash]} (size {e.decompressed_size})')
