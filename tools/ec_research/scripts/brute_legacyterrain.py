"""Exhaustive LegacyTerrain.uop naming brute-force."""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
EC = Path(r'C:\Games\Electronic Arts\Ultima Online Enhanced')
a = UopArchive(EC / 'LegacyTerrain.uop'); hashes = set(a.by_hash)
BS = chr(92)
ids, names, texmaps = [], [], []
for e in a.entries:
    try: d = a.read(e).decode('utf-8', 'ignore')
    except Exception: continue
    m = re.search(r'id="(\d+)"', d); n = re.search(r'name="([^"]+)"', d); t = re.search(r'texMap="(\d+)"', d)
    if m: ids.append(int(m.group(1)))
    if n: names.append(n.group(1))
    if t: texmaps.append(int(t.group(1)))
roots = ['legacyterrain', 'legacyterraindefinition', 'legacyterrains', 'terrain',
         'legacyterrainmap', 'legacyterraintype', 'terraintype', 'legacyterraindata']
exts = ['.bin', '.xml', '', '.txt', '.dat', '.terrain']
prefs = ['build/', 'Build/', 'build' + BS, 'Build' + BS, '']
def fmts(v): return [f'{v}', f'{v:08}', f'{v:06}', f'{v:05}', f'{v:04}']
hit = []
src = sorted(set(ids) | set(texmaps) | set(range(0, 5000)))
for pre in prefs:
    sep = BS if BS in pre else '/'
    for r in roots:
        for x in exts:
            for v in src:
                for f in fmts(v):
                    if hash_name(f'{pre}{r}{sep}{f}{x}') in hashes:
                        hit.append(f'{pre}{r}{sep}{f}{x}')
                if hit: break
            if hit: break
        if hit: break
    if hit: break
# name-based
for pre in prefs:
    sep = BS if BS in pre else '/'
    for r in roots:
        for x in exts:
            for nm in names[:300]:
                for cand in (nm, nm.lower(), nm.replace(' ', '_')):
                    if hash_name(f'{pre}{r}{sep}{cand}{x}') in hashes:
                        hit.append(f'{pre}{r}{sep}{cand}{x}')
print('total candidates checked across roots/prefs/exts/ids')
print('HITS:', hit[:10] if hit else 'NONE')
