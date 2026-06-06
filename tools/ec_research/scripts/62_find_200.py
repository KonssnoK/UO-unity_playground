"""Find dictionary entries matching tile 200 / sprite 200, and see what
offset they're at — then compare with the sd_off our parser extracted."""
import re
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
arc = UopArchive(EC / "string_dictionary.uop")
sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
arc.close()

# Walk dict
entries = []
p = 16
while p + 2 <= len(sd):
    length = struct.unpack_from("<H", sd, p)[0]
    if length == 0 or length > 500: break
    cs = p + 2; ce = cs + length
    if ce > len(sd): break
    entries.append((p, cs, ce, length, sd[cs: ce].decode("ascii", errors="replace")))
    p = ce

print(f"{len(entries)} entries loaded")

# Find anything that mentions sprite 200
rx = re.compile(r'(WorldArt\\0*200_|TileArtLegacy\\200\.|TileArtEnhanced\\200\.)', re.I)
hits = []
for prefix, cs, ce, ln, s in entries:
    if rx.search(s):
        hits.append((prefix, cs, ce, ln, s))

print(f"\nEntries referencing sprite '200':")
for prefix, cs, ce, ln, s in hits:
    print(f"  prefix@{prefix:>7}  content@{cs}..{ce}  len={ln:>3}  {s!r}")

# Also find entries within +- 50 bytes of sd_off=45634, to see what's there.
print(f"\nThe sd_off=45634 we extracted from tile 200's tileart record:")
for prefix, cs, ce, ln, s in entries:
    if abs(cs - 45634) < 100:
        marker = ""
        if cs <= 45634 < ce: marker = "  ← CONTAINS 45634"
        elif prefix <= 45634 < cs: marker = "  ← LEN-PREFIX BYTE"
        print(f"  prefix@{prefix:>6}  content@{cs}..{ce}  len={ln:>3}  {s!r}{marker}")

# And the *actual content offset* of TileArtLegacy\200.tga (or similar) — show its sd_off range
print(f"\nFor sprite_id 200, the offsets we'd EXPECT to see in tile 200's record:")
for prefix, cs, ce, ln, s in hits:
    print(f"  {s!r}: would point anywhere in content range [{cs}, {ce})")
