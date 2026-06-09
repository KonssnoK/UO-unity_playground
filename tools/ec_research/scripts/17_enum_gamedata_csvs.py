"""Find every 'data/gamedata/<name>.csv' reference in UOSA.exe and test them
against GameData.uop. Then read interesting ones."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
data = (EC / "UOSA.exe").read_bytes()

# All printable strings >= 8 chars
strings = set(re.findall(rb"[\x20-\x7E]{8,}", data))

paths: set[str] = set()
for s in strings:
    try:
        text = s.decode('ascii')
    except UnicodeDecodeError:
        continue
    for m in re.findall(r"data/gamedata/[\w./_-]+", text):
        paths.add(m)
    for m in re.findall(r"data/[\w./_-]+\.csv", text):
        paths.add(m)
    for m in re.findall(r"data/[\w./_-]+\.xml", text):
        paths.add(m)
    for m in re.findall(r"data/[\w./_-]+\.bin", text):
        paths.add(m)

# Also look for any string ending in .csv
for s in strings:
    try:
        t = s.decode('ascii')
    except UnicodeDecodeError:
        continue
    if t.endswith('.csv'):
        paths.add(t)

print(f"Found {len(paths)} unique 'data/...' or *.csv references")
for p in sorted(paths):
    print(f"  {p}")

# Test against GameData.uop
arc = UopArchive(EC / "GameData.uop")
seen = arc.by_hash
arc.close()
print(f"\n--- testing against GameData.uop ({len(seen)} entries) ---")
for p in sorted(paths):
    if hash_name(p) in seen:
        print(f"  HIT: {p}")
    elif hash_name(p.lower()) in seen:
        print(f"  HIT (lowered): {p.lower()}")
