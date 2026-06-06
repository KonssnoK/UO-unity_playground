"""Test literal CSV names against GameData.uop, and probe other clues."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def test(arc_name: str, names: list[str]):
    arc = UopArchive(EC / arc_name)
    seen = arc.by_hash
    print(f"\n=== {arc_name} ({len(seen)} entries) ===")
    for n in names:
        h = hash_name(n)
        if h in seen:
            print(f"  HIT: {n!r}")
        else:
            print(f"   no: {n!r}")
    arc.close()


# Strings extracted from binary
gamedata_candidates = [
    "data/gamedata/legacyterrainmap.csv",
    "data/gamedata/mobart.csv",
    "data/gamedata/legacycontainers.csv",
    "data/gamedata/legacyterrainmap",
    "data/gamedata/mobart",
    "data/gamedata/recipes.csv",
    "data/gamedata/faces.csv",
    "build/gamedata/legacyterrainmap.csv",
    "Build/GameData/legacyterrainmap.csv",
]
test("GameData.uop", gamedata_candidates)

# Try gump pattern just to confirm hashing convention
gump_candidates = [
    "build/gumpartmask/00000000.dds",
    "Build/GumpArtMask/00000000.dds",
    "Build/GumpArtMask/00.dds",
    "Build/GumpArtMask/0%d.dds".replace("%d", "0"),
    "Build\\GumpArtMask\\00.dds",
    "build/gumpartmask/0.dds",
]
test("GumpArtMask.uop", gump_candidates)
