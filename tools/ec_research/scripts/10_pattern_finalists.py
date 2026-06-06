"""Test the actual format strings extracted from UOSA.exe against UOP hash sets.

Discovered tokens: %08d_LegacyTileArt, %08d_TileArt, %08d_Texture, %08d_GumpArt.
Path convention from string_dictionary: Build/<MixedCaseFolder>/<file>.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def probe(arc_name, patterns, probe_max=80_000):
    arc = UopArchive(EC / arc_name)
    seen = set(arc.by_hash.keys())
    arc.close()
    print(f"\n=== {arc_name} ({len(seen)} entries) ===")
    for pat in patterns:
        hits = sum(1 for i in range(probe_max) if hash_name(pat.format(i)) in seen)
        if hits > 0:
            print(f"  HITS {hits}/{len(seen)}: {pat!r}")
        else:
            print(f"   0 : {pat!r}")


legacy_tex_pats = [
    "Build/LegacyTexture/{0:08}_LegacyTileArt.dds",
    "build/legacytexture/{0:08}_legacytileart.dds",
    "Build/LegacyTexture/{0:08}_LegacyTileArt",
    "Build/LegacyTextureData/{0:08}_LegacyTileArt.dds",
    "Build\\LegacyTexture\\{0:08}_LegacyTileArt.dds",
    "build/legacytexture/{0:08}_LegacyTileArt.dds",
    "Build/LegacyTexture/{0:08}_LegacyTileArt.tex",
    "{0:08}_LegacyTileArt.dds",
    "{0:08}_LegacyTileArt",
    "LegacyTexture/{0:08}_LegacyTileArt.dds",
]
texture_pats = [
    "Build/Texture/{0:08}_TileArt.dds",
    "Build/Texture/{0:08}_Texture.dds",
    "Build/Texture/{0:08}_TileArt",
    "Build/EnhancedTexture/{0:08}_Texture.dds",
    "Build/EnhancedTexture/{0:08}_TileArt.dds",
    "build/texture/{0:08}_tileart.dds",
    "{0:08}_TileArt.dds",
    "{0:08}_Texture.dds",
    "Build\\Texture\\{0:08}_TileArt.dds",
]
af1_pats = [
    "Build/AnimationFrame1/{0:08}_Animation.dds",
    "Build/AnimationFrame1/{0:08}_AnimationFrame.dds",
    "Build/AnimationFrame1/{0:08}_AnimationFrame.bin",
    "Build/AnimationFrame1/{0:08}_AnimationFrameSet.bin",
    "Build/AnimationFrameSet/{0:08}_AnimationFrameSet.bin",
    "Build/AnimationFrame/{0:08}_AnimationFrameSet.bin",
    "Build/AnimationFrameSet/1/{0:08}.bin",
    "Build/Animation/{0:08}_Frame.bin",
    "Build/Animations/{0:08}_AnimationFrame.bin",
]

probe("LegacyTexture.uop", legacy_tex_pats)
probe("Texture.uop", texture_pats, probe_max=20000)
probe("AnimationFrame1.uop", af1_pats, probe_max=20000)
