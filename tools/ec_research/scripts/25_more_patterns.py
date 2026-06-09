"""More targeted attempts based on the new context dump.

New tokens: 'Textures\\', 'WorldArt\\', 'WorldArt\\ref'.
And the literal `Build\\GumpArtMask\\0%d.dds` template — sprintf %d expands
without padding, so file 5 -> "05.dds", file 12 -> "012.dds".
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def test(arc_name, patterns, probe_max=30_000):
    arc = UopArchive(EC / arc_name)
    seen = arc.by_hash
    arc.close()
    print(f"\n=== {arc_name} ({len(seen)} entries) ===")
    best = 0
    best_pat = None
    for pat in patterns:
        hits = sum(1 for i in range(probe_max) if hash_name(pat.format(i)) in seen)
        marker = "**" if hits > best else "  "
        if hits > 0:
            print(f"{marker} {hits:6d}/{len(seen)} : {pat!r}")
        if hits > best:
            best = hits; best_pat = pat
    return best, best_pat


# GumpArtMask with literal `0`:
# sprintf("0%d", n) gives "00", "01", ..., "09", "010", "011", "0100"
gump_pats = [
    "build/gumpartmask/0{0:d}.dds",
    "build/gumpartmask/0{0}.dds",
    "Build/GumpArtMask/0{0:d}.dds",
    "Build\\GumpArtMask\\0{0:d}.dds",
    "build/gumpartmask/{0:d}.dds",
    "build/gumpartmask/{0:08}.dds",
    "build/gumpartmask/{0:08X}.dds",
]
test("GumpArtMask.uop", gump_pats)

# Texture.uop variations using "textures" and "worldart" folder hints
texture_pats = [
    "build/textures/{0:08}.dds",
    "build/worldart/{0:08}.dds",
    "build/worldart/ref/{0:08}.dds",
    "build/tileartenhanced/{0:08}.dds",
    "build/enhancedtexture/{0:08}.dds",
    "build/texture/{0:08}.dds",
    "build/tileart/{0:08}.dds",
]
test("Texture.uop", texture_pats)

# Maybe AnimationFrame* uses 2-level path like the CC convention
af_pats = [
    "build/animationframe/{0:06}.bin",
    "build/animationframeset/{0:06}.bin",
    "build/animationlegacyframe/{0:06}/{1:02}.bin",  # 2D below
    "build/animationframe/{0:06}/{1:02}.bin",
    "build/animationframe1/{0:06}/{1:02}.bin",
]
# Test 1D first
test("AnimationFrame1.uop", af_pats[:2], probe_max=20_000)

# 2D
for pat in af_pats[2:]:
    arc = UopArchive(EC / "AnimationFrame1.uop")
    seen = arc.by_hash; arc.close()
    hits = 0
    for body in range(2000):
        for action in range(64):
            if hash_name(pat.format(body, action)) in seen:
                hits += 1
    if hits > 0:
        print(f"  2D {hits}/{len(seen)} : {pat!r}")
