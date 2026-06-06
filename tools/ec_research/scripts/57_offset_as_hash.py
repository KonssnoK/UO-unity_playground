"""Test: is sd_off actually a hash of the filename (low 32 bits)?
For tile 16384 sd_off=45085: does Jenkins('data\\worldart\\00000461_rattan_wall.tga') low32 = 45085?"""
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import hash_name, UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

# Known mappings observed
known = [
    (16384, 45085, 'data\\worldart\\00000461_rattan_wall.tga'),
    (16385, 45087, 'data\\worldart\\00000461_rattan_wall.tga'),  # same string, different sd_off?
    (16640,  7478, 'data\\tileartenhanced\\73.tga'),
    (22137, 24115, 'data\\tileartlegacy\\248.tga'),
    (19674, 54565, 'data\\tileartenhanced\\560.tga'),
    (22137, 58231, 'data\\worldart\\00000596_moorish_sandstone_wall.tga'),
]

for tile, sd_off, fname in known:
    h = hash_name(fname)
    low32 = h & 0xFFFFFFFF
    high32 = h >> 32
    print(f"tile {tile:>6}  sd_off={sd_off:>6}  hash=0x{h:016X}  low32={low32:>10}  high32={high32:>10}")

# Also try without "data\" prefix
print("\n-- without 'data\\\\' prefix --")
for tile, sd_off, fname in known:
    short = fname.removeprefix('data\\')
    h = hash_name(short)
    low32 = h & 0xFFFFFFFF
    print(f"tile {tile:>6}  sd_off={sd_off:>6}  short={short!r}  low32={low32:>10}")

# Also try forward slashes
print("\n-- forward slashes --")
for tile, sd_off, fname in known:
    fs = fname.replace('\\', '/')
    h = hash_name(fs)
    print(f"tile {tile:>6}  sd_off={sd_off:>6}  fs={fs!r}  low32={h & 0xFFFFFFFF:>10}")

# What's at byte offset sd_off in dict?
arc = UopArchive(EC / "string_dictionary.uop")
sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
arc.close()
print("\n-- raw 4 bytes at sd_off (LE u32) --")
for tile, sd_off, _ in known:
    raw = struct.unpack_from("<I", sd, sd_off)[0]
    print(f"  tile {tile:>6}  bytes@{sd_off}: 0x{raw:08X}")
