"""Grep decompressed payloads for literal asset name references.

EC data tables (GameData, TerrainDefinition, LegacyTerrain XML) often reference
texture files by their internal path. Finding those gives us the hash pattern.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

PATTERNS = [
    re.compile(rb"build/[\w./\\-]+"),
    re.compile(rb"[\w/\\-]+\.dds"),
    re.compile(rb"[\w/\\-]+\.tga"),
    re.compile(rb"[\w/\\-]+\.bin"),
    re.compile(rb"\w*[Tt]exture[\w/\\-]*"),
    re.compile(rb"\w*[Tt]errain[\w/\\-]*"),
    re.compile(rb"\w*[Aa]nimation[\w/\\-]*"),
]


def grep_archive(name: str, max_entries: int = 50) -> set[bytes]:
    found: set[bytes] = set()
    arc = UopArchive(EC / name)
    print(f"\n=== {name} ({len(arc.entries)} entries) ===")
    for i, (e, payload) in enumerate(arc.iter_decompressed()):
        if i >= max_entries:
            break
        for pat in PATTERNS:
            for m in pat.findall(payload):
                if 4 <= len(m) <= 120 and m not in found:
                    found.add(m)
    arc.close()
    for s in sorted(found):
        try:
            print(f"  {s.decode('ascii', errors='replace')!r}")
        except Exception:
            pass
    return found


if __name__ == "__main__":
    for name in [
        "GameData.uop",
        "TerrainDefinition.uop",
        "LegacyTerrain.uop",
        "AnimationDefinition.uop",
        "AnimationSequence.uop",
    ]:
        grep_archive(name, 200)
