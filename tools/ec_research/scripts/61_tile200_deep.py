"""Deep dive into tile 200's tileart record and surrounding dictionary entries."""
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

ART_ID = 200 + 0x4000

arc = UopArchive(EC / "tileart.uop")
payload = arc.read(arc.by_hash[hash_name(f"build/tileart/{ART_ID:08}.bin")])
arc.close()

print(f"tile 200 (art_id {ART_ID}) record bytes = {len(payload)}")

# Dump bytes from SUB_9_7 onwards
# First skip header + props + radar etc.
p = 0x7D
cnt = payload[p]; p += 1 + cnt * 5  # SUB_9
cnt = payload[p]; p += 1 + cnt * 5  # SUB_9_2
cnt = struct.unpack_from("<I", payload, p)[0]; p += 4 + cnt * 8  # SUB_9_3
cnt = struct.unpack_from("<I", payload, p)[0]; p += 4  # SUB_9_4
for _ in range(cnt):
    val = payload[p]; p += 1
    if val == 0:
        sub = struct.unpack_from("<I", payload, p)[0]; p += 4 + sub * 8
    elif val == 1: p += 5
    else: break
sitting = payload[p]; p += 1
if sitting != 0: p += 16
p += 4  # SUB_9_6

print(f"\nSUB_9_7 starts at 0x{p:X} ({p})")
sub_start = p
chunk = payload[sub_start: min(sub_start + 200, len(payload))]
print(f"Bytes:")
for i in range(0, len(chunk), 16):
    seg = chunk[i:i+16]
    hex_s = ' '.join(f'{b:02x}' for b in seg)
    asc_s = ''.join(chr(b) if 32 <= b < 127 else '.' for b in seg)
    print(f"  +{i:>3}: {hex_s:<48} | {asc_s}")

# Now parse step by step, printing what each interpretation gives
print(f"\nStep-by-step parse:")
p = sub_start
for gname in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
    val = payload[p]
    print(f"\n[{gname}] @ +{p - sub_start}: Val=0x{val:02X}")
    p += 1
    if val == 0:
        continue
    unk = payload[p]; p += 1
    shader = struct.unpack_from("<I", payload, p)[0]; p += 4
    count = payload[p]; p += 1
    print(f"  unk=0x{unk:02X}  shader=0x{shader:08X}  count={count}")
    for i in range(count):
        sd_off = struct.unpack_from("<I", payload, p)[0]
        b = payload[p+4]
        rep = struct.unpack_from("<f", payload, p+5)[0]
        d1 = struct.unpack_from("<I", payload, p+9)[0]
        d2 = struct.unpack_from("<I", payload, p+13)[0]
        print(f"  tex#{i} (17 bytes @ +{p - sub_start}): sd_off={sd_off}  b={b}  rep={rep}  d1={d1} d2={d2}")
        p += 17
    c2 = struct.unpack_from("<I", payload, p)[0]; print(f"  secondary count = {c2}")
    p += 4 + c2 * 4
    c3 = struct.unpack_from("<I", payload, p)[0]; print(f"  tertiary count = {c3}")
    p += 4 + c3 * 4

print(f"\nEnd of parsed SUB_9_7 at +{p - sub_start} (relative)")
print(f"Remaining bytes in record: {len(payload) - p}")

# Now load the dictionary and show entries 100 bytes before and after sd_off=45634
arc = UopArchive(EC / "string_dictionary.uop")
sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
arc.close()

# Walk the dict
entries = []
pp = 16
while pp + 2 <= len(sd):
    length = struct.unpack_from("<H", sd, pp)[0]
    if length == 0 or length > 500: break
    cs = pp + 2
    ce = cs + length
    if ce > len(sd): break
    s = sd[cs: ce].decode("ascii", errors="replace")
    entries.append((pp, cs, ce, length, s))
    pp = ce

# Show entries around sd_off=45634
print(f"\nDict entries around offset 45634:")
for prefix, cs, ce, ln, s in entries:
    if 45520 <= cs <= 45720 or 45520 <= ce <= 45720:
        print(f"  prefix@{prefix:>6}  content@{cs}..{ce}  len={ln:>3}  {s!r}")
