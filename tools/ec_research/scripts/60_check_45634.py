"""What's actually at dict offset 45630..45680?"""
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

start, end = 45620, 45720
print(f"Raw bytes {start}..{end}:")
for i in range(start, end, 16):
    chunk = sd[i:i+16]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    asc_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
    print(f"  {i:>6}: {hex_str:<48} | {asc_str}")

print()
# Walk and find entries spanning 45620..45680
p = 16
entries = []
while p + 2 <= len(sd):
    length = struct.unpack_from("<H", sd, p)[0]
    if length == 0 or length > 500: break
    content_start = p + 2
    content_end = content_start + length
    if content_end > len(sd): break
    entries.append((p, content_start, content_end, length))
    p = content_end

# Print entries near 45634
print("Entries near offset 45634:")
for prefix, cs, ce, ln in entries:
    if abs(cs - 45634) < 100 or abs(ce - 45634) < 100:
        s = sd[cs: ce].decode("ascii", errors="replace")
        contains = "**CONTAINS 45634**" if cs <= 45634 < ce else ""
        contains_35 = "**CONTAINS 45635**" if cs <= 45635 < ce else ""
        print(f"  prefix@{prefix}  content@{cs}..{ce}  len={ln}  {contains} {contains_35}")
        print(f"    {s!r}")
