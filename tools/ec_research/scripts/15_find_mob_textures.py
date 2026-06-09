"""Cross-reference mobart.csv filenames against all UOP archives."""
import sys
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CSV_PATH = Path(__file__).resolve().parent.parent / "out" / "GameData" / "mobart.csv"

# Read filenames
filenames = []
with CSV_PATH.open() as f:
    rd = csv.DictReader(f)
    for row in rd:
        fn = row.get("Filename", "").strip()
        if fn and fn.endswith(".dds"):
            filenames.append(fn)
print(f"Loaded {len(filenames)} mob texture filenames; sample: {filenames[:5]}")

# Path prefixes to try (lowercased)
prefixes = [
    "build/animations/",
    "build/animation/",
    "build/mobanimtexture/",
    "build/mobart/",
    "build/paperdoll/",
    "data/animations/",
    "data/gamedata/animations/",
    "animations/",
    "build/texture/animations/",
    "",
]

uops = ["Texture.uop", "LegacyTexture.uop", "Paperdoll.uop",
        "AnimationFrame1.uop", "AnimationFrame2.uop", "AnimationFrame3.uop",
        "AnimationFrame4.uop", "AnimationFrame5.uop", "AnimationFrame6.uop"]

for uop in uops:
    arc = UopArchive(EC / uop)
    seen = arc.by_hash
    arc.close()
    print(f"\n=== {uop} ({len(seen)} entries) ===")
    best_prefix = None
    best_hits = 0
    for prefix in prefixes:
        hits = sum(1 for fn in filenames if hash_name(prefix + fn.lower()) in seen)
        if hits > 0:
            print(f"  {hits:4d} hits: prefix={prefix!r}")
            if hits > best_hits:
                best_hits = hits
                best_prefix = prefix
        # also try original case
        hits = sum(1 for fn in filenames if hash_name(prefix + fn) in seen)
        if hits > 0:
            print(f"  {hits:4d} hits (orig case): prefix={prefix!r}")
