"""Inspect the raw bytes of string_dictionary.bin around key offsets to
figure out the actual entry format."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

arc = UopArchive(EC / "string_dictionary.uop")
sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
arc.close()

print(f"size = {len(sd)} bytes")
print(f"first 64 bytes:\n  {sd[:64].hex(' ')}")
print()

# Try the early entry: bytes 16+ should start with u16 length = 14, then "UOSpriteShader"
import struct
length = struct.unpack_from("<H", sd, 16)[0]
print(f"u16 at offset 16 = {length}  → '{sd[18:18+length].decode('ascii', errors='replace')}'")

# Now check around offset 45085
for off in (45083, 45084, 45085, 45086, 45087, 45088, 45090, 45091, 7478, 7476, 24115, 24113):
    head = sd[max(0, off-4): off]
    me   = sd[off: off+50]
    ascii_me = ''.join(chr(b) if 32 <= b < 127 else '.' for b in me)
    print(f"\n@ {off}: prev4=[{head.hex(' ')}] this=[{me[:40].hex(' ')}]")
    print(f"             ascii: '{ascii_me[:40]}'")

# Cross-check: are strings preceded by u16 lengths?
# Walk forward from offset 18 (after first known string) and emit a few entries
print("\n=== Walking forward from offset 18 ===")
p = 18 + 14  # past UOSpriteShader
for _ in range(8):
    if p + 2 > len(sd): break
    length = struct.unpack_from("<H", sd, p)[0]
    if length > 200 or length == 0:
        # Maybe there's a single-byte tag here
        print(f"  @ {p}: byte={sd[p]:02x} (u16 len={length} unlikely)")
        # try advancing one byte
        p += 1
        continue
    try:
        s = sd[p+2: p+2+length].decode('ascii')
    except Exception:
        s = repr(sd[p+2: p+2+length])
    print(f"  @ {p}: len={length}  string={s!r}")
    p += 2 + length
