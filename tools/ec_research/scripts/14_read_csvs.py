"""Read mobart.csv and legacyterrainmap.csv from GameData.uop."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

OUT = Path(__file__).resolve().parent.parent / "out" / "GameData"
OUT.mkdir(parents=True, exist_ok=True)

arc = UopArchive(EC / "GameData.uop")
seen = arc.by_hash

names = [
    "data/gamedata/legacyterrainmap.csv",
    "data/gamedata/mobart.csv",
    "data/gamedata/legacycontainers.csv",
]

for n in names:
    entry = seen.get(hash_name(n))
    if entry is None:
        print(f"missing: {n}")
        continue
    data = arc.read(entry)
    fn = OUT / n.split("/")[-1]
    fn.write_bytes(data)
    print(f"\n=== {n}  ({len(data)} bytes) -> {fn}")
    text = data.decode('latin-1')
    # Print first 30 lines
    for i, line in enumerate(text.splitlines()[:30]):
        print(f"  {line}")

arc.close()
