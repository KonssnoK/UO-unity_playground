"""The binary mentions TileArt, LegacyTileArt, GumpArt — maybe the folder name
inside the UOP isn't the .uop stem but those aliases."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def probe(arc, patterns, probe_max):
    seen = arc.by_hash
    print(f"\n--- {arc.path.name} ({len(seen)}) ---")
    for pat in patterns:
        hits = sum(1 for i in range(probe_max) if hash_name(pat.format(i)) in seen)
        print(f"  {hits}/{len(seen)} : {pat!r}")


with UopArchive(EC / "LegacyTexture.uop") as a:
    probe(a, [
        "build/legacytileart/{0:08}.dds",
        "build/legacytileart/{0:d}.dds",
        "build/legacytileart/{0}.dds",
        "build/legacytileart/{0:08}_legacytileart.dds",
        "build/legacytileart/{0:08}_LegacyTileArt.dds",
    ], 70000)

with UopArchive(EC / "Texture.uop") as a:
    probe(a, [
        "build/tileart/{0:08}.dds",
        "build/tileart/{0:d}.dds",
        "build/tileart/{0}.dds",
        "build/tileart/{0:08}_tileart.dds",
        "build/tileart/{0:08}_TileArt.dds",
    ], 30000)

with UopArchive(EC / "GumpArtMask.uop") as a:
    probe(a, [
        "build/gumpart/{0:08}.dds",
        "build/gumpart/{0:d}.dds",
        "build/gumpart/0{0}.dds",
        "build/gumpart/0{0:d}.dds",
        "build/gumpart/{0:08}_gumpart.dds",
        "build/gumpart/{0:08}_GumpArt.dds",
    ], 30000)
