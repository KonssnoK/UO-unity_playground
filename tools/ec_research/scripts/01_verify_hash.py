"""Sanity-check the Python hash port against a known pattern.

build/terraintexture/{0:D8}.dds matches all 38 entries of TerrainTexture.uop.
We expect a 100% recovery rate here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def confirm(name: str, pattern: str, expected_hits: int, probe_max: int):
    arc = UopArchive(EC / name)
    seen = set(arc.by_hash.keys())
    hits = sum(1 for i in range(probe_max) if hash_name(pattern.format(i)) in seen)
    print(f"  {name}: pattern={pattern!r} -> {hits}/{len(seen)} (expected {expected_hits})")
    arc.close()
    return hits


if __name__ == "__main__":
    confirm("TerrainTexture.uop", "build/terraintexture/{:08}.dds", 38, 1000)
    confirm("AnimationSequence.uop", "build/animationsequence/{:08}.bin", 388, 5000)
    confirm("AnimationDefinition.uop", "build/animationdefinition/{:08}.bin", 1196, 80000)
