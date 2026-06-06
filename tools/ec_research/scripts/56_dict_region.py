"""Dump raw region of dictionary around offset 7478 and verify walk."""
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

# Dump from 7440 to 7600
start, end = 7440, 7600
print(f"Raw bytes {start}..{end}:")
chunk = sd[start:end]
hexlines = []
for i in range(0, len(chunk), 16):
    seg = chunk[i:i+16]
    hexstr = ' '.join(f'{b:02x}' for b in seg)
    asciistr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in seg)
    hexlines.append(f"  {start+i:>6}: {hexstr:<48} | {asciistr}")
print('\n'.join(hexlines))

# Compare with walk
print("\nLinear walk around this region:")
p = 7400  # start a bit before
# Catch up by simulating walk from offset 16
walk_p = 16
entries = []
while walk_p + 2 <= len(sd):
    length = struct.unpack_from("<H", sd, walk_p)[0]
    if length == 0 or length > 500:
        break
    entries.append((walk_p, length, sd[walk_p+2: walk_p+2+length].decode('ascii', errors='replace')))
    walk_p = walk_p + 2 + length

# Find entries whose content includes 7478
for prefix_off, length, s in entries:
    content_start = prefix_off + 2
    content_end = content_start + length
    if abs(content_start - 7478) < 100 or abs(content_end - 7478) < 100:
        print(f"  prefix@{prefix_off:>6}  content@{content_start:>6}..{content_end:>6}  len={length:>3}  {s!r}")
