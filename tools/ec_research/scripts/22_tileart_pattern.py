"""Test TileArtLegacy / TileArtEnhanced as folder names — discovered in UOSA.exe."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def test(arc_name, patterns, probe_max=70_000):
    arc = UopArchive(EC / arc_name)
    seen = arc.by_hash
    arc.close()
    print(f"\n=== {arc_name} ({len(seen)} entries) ===")
    for pat in patterns:
        hits = sum(1 for i in range(probe_max) if hash_name(pat.format(i)) in seen)
        marker = "HIT" if hits > 0 else "   "
        print(f"  {marker} {hits:6d}/{len(seen)} : {pat!r}")


# Apply the lowercase + forward-slash convention that worked for the others
legacy_pats = [
    "build/tileartlegacy/{0:08}_legacytileart.dds",
    "build/tileartlegacy/{0:08}.dds",
    "build/tileartlegacy/{0:08}_tileart.dds",
    "build/tileartlegacy/{0:08}_legacy.dds",
    "build/tileartlegacy/{0:08}_tileartlegacy.dds",
    # mixed case
    "Build/TileArtLegacy/{0:08}_LegacyTileArt.dds",
    "Build\\TileArtLegacy\\{0:08}_LegacyTileArt.dds",
    "build/tileartlegacy/{0}.dds",
]
enhanced_pats = [
    "build/tileartenhanced/{0:08}_tileart.dds",
    "build/tileartenhanced/{0:08}.dds",
    "build/tileartenhanced/{0:08}_texture.dds",
    "build/tileartenhanced/{0:08}_enhanced.dds",
    "build/tileartenhanced/{0:08}_tileartenhanced.dds",
    "Build/TileArtEnhanced/{0:08}_TileArt.dds",
    "Build\\TileArtEnhanced\\{0:08}_TileArt.dds",
]
gump_pats = [
    "build/gumpartmask/0{0}.dds",      # exact literal from "Build\GumpArtMask\0%d.dds"
    "build/gumpartmask/0{0:d}.dds",
    "Build/GumpArtMask/0{0}.dds",
    "Build\\GumpArtMask\\0{0}.dds",
    "build/gumpartmask/{0:08}_gumpart.dds",
    "build/gumpartmask/{0:08}.dds",
]

test("LegacyTexture.uop", legacy_pats)
test("Texture.uop", enhanced_pats, probe_max=30_000)
test("GumpArtMask.uop", gump_pats)
