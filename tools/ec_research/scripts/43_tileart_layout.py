"""Sample several tileart.uop records and probe candidate field layouts."""
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = HERE.parent / "out" / "tileart_samples"
OUT.mkdir(parents=True, exist_ok=True)

arc = UopArchive(EC / "tileart.uop")

# Pick known interesting tile ids and dump their raw bytes
ID_SAMPLES = [
    0,        # first land tile
    1,        # second land tile (dirt?)
    100,      # mid-range land
    0x4000,   # first static
    0x4001,
    0x4002,
    0x4100,   # arbitrary static mid-range
    0x8000,   # high static
    0xC000,   # very high
    0x14000,  # near max
    22137,    # face1 (from gamedata)
    8251,     # 'Short' hair tile art id
    5903,     # 'shoes' tile art id
    5433,     # 'long pants' tile art id
]

print(f"# tileart.uop  ({len(arc.entries)} entries)")
print()
print(f"{'id':>8} {'csize':>6} {'dsize':>6}  head_hex")
print("-" * 90)
for tid in ID_SAMPLES:
    name = f"build/tileart/{tid:08}.bin"
    h = hash_name(name)
    entry = arc.by_hash.get(h)
    if entry is None:
        print(f"{tid:>8}   MISS  (no entry for {name!r})")
        continue
    payload = arc.read(entry)
    head = payload[:min(64, len(payload))]
    hex_str = head.hex(" ")
    print(f"{tid:>8} {entry.compressed_size:>6} {entry.decompressed_size:>6}  {hex_str}")
    (OUT / f"{tid:08}.bin").write_bytes(payload)

print()
print("--- attempting structured decode of id 0x4000 (first static) ---")
name = f"build/tileart/{0x4000:08}.bin"
entry = arc.by_hash.get(hash_name(name))
if entry:
    p = arc.read(entry)
    print(f"size: {len(p)}")
    print(f"head: {p[:32].hex(' ')}")
    # tentative parse: try various small-int layouts
    if len(p) >= 4:
        print(f"  u32@0   = 0x{struct.unpack_from('<I', p, 0)[0]:08X}  ({struct.unpack_from('<I', p, 0)[0]})")
    if len(p) >= 8:
        print(f"  u32@4   = 0x{struct.unpack_from('<I', p, 4)[0]:08X}")
    if len(p) >= 24:
        print(f"  u8 row  = {' '.join(str(b) for b in p[:24])}")
    # Read with assumed: u32 flags / u8 weight / u8 layer / u16 count / u16 anim / u16 hue / ...
    if len(p) >= 16:
        fields = struct.unpack_from('<IBBHHHH', p, 0)
        print(f"  legacy-style guess: flags=0x{fields[0]:08X} weight={fields[1]} "
              f"layer={fields[2]} count={fields[3]} anim={fields[4]} hue={fields[5]} light={fields[6]}")
    if len(p) >= 18:
        h_byte = p[16]
        name_bytes = p[17:17+20]
        try:
            n = name_bytes.split(b'\x00', 1)[0].decode('ascii')
        except Exception:
            n = '?'
        print(f"  height_guess={h_byte}  name_guess={n!r}")
arc.close()
