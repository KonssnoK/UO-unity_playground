"""Confirm GumpArtMask uses Build\\GumpArtMask\\0%d.dds → build/gumpartmask/0%d.dds."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
arc = UopArchive(EC / "GumpArtMask.uop")
seen = arc.by_hash
print(f"GumpArtMask entries: {len(seen)}")

# Pattern from binary: Build\GumpArtMask\0%d.dds  (with %d not padded; '0' literal prefix)
patterns = [
    "build/gumpartmask/0{0}.dds",         # lowercased + forward slash, literal '0' prefix
    "build/gumpartmask/{0}.dds",
    "Build/GumpArtMask/0{0}.dds",         # original case
    "build/gumpartmask/0{0:08}.dds",
    "build/gumpartmask/0{0:d}.dds",
]
for pat in patterns:
    hits = sum(1 for i in range(60000) if hash_name(pat.format(i)) in seen)
    print(f"  {hits}/{len(seen)} : {pat!r}")

arc.close()
