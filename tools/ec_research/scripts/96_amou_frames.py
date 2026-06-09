"""Parse AMOU frame data after the palette.

Hypothesis:
  0x00..0x1F: header (magic AMOU + version + dsize + body_id + bbox + atlas dims)
  0x20: u32 frame_count
  0x24: u32 palette_byte_size (= num_colors * 4)
  0x28-0x2F: 8 bytes of flags/dimensions (per-body)
  0x30..0x30+palette_byte_size: palette of (R, G, B, flag) tuples
  0x30+palette_byte_size..: frame stream
"""
import io, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
archives = [UopArchive(EC / f"AnimationFrame{i}.uop") for i in range(1, 7)]

def fetch(body, action):
    key = f"build/animationframe/{body:06}/{action:02}.bin"
    h = hash_name(key)
    for arc in archives:
        e = arc.by_hash.get(h)
        if e: return arc.read(e)
    return None

def hexline(data, off, n=32):
    chunk = data[off:off+n]
    return ' '.join(f'{b:02x}' for b in chunk)

# Pick human male idle
data = fetch(400, 0)
print(f'data size: {len(data)}')

frame_count = struct.unpack_from('<I', data, 0x20)[0]
pal_bytes   = struct.unpack_from('<I', data, 0x24)[0]
pal_entries = pal_bytes // 4
pal_end = 0x30 + pal_bytes
print(f'frame_count(@0x20) = {frame_count}')
print(f'palette: {pal_entries} entries x 4 = {pal_bytes} B')
print(f'palette ends at offset 0x{pal_end:X}')
print(f'remaining after palette: {len(data) - pal_end} bytes')

print()
print(f'=== bytes 0x{pal_end:X} .. (frame area start) ===')
for o in range(0, 128, 16):
    print(f'  0x{pal_end+o:X}: {hexline(data, pal_end+o, 16)}')

# Plausible frame-record layouts to try:
#   16 bytes: count(u32) + 4xi16 bbox + (size or offset) u32
#   12 bytes: 4xi16 bbox + u32
# Let's hypothesize a header per frame, then variable-length pixel stream.

# First frame area bytes at body=400 action=0 are: 00 00 04 00 f1 ff b8 ff 0e 00 fe ff 0d 13 00 00 ...
# Read as 2-byte signed values: (0, 4, -15, -72, 14, -2, 4877, 0)
# - "0" "4" then bbox (-15,-72)..(14,-2) — fits inside global bbox
# - 0x130D = 4877 — could be pixel count or stream size
# Try this layout:
#   i16 cellX, cellY (?)        2x2=4
#   i16 minX, minY, maxX, maxY  4x2=8
#   u16 pixel_count (?)         2
#   u16 ???                     2
#   ... pixels
print()
print(f'=== try frame record: 16 B header at 0x{pal_end:X} ===')
fp = pal_end
n_show = 6
for i in range(n_show):
    if fp + 16 > len(data): break
    cellx = struct.unpack_from('<h', data, fp)[0]
    celly = struct.unpack_from('<h', data, fp+2)[0]
    bbox = struct.unpack_from('<4h', data, fp+4)
    px_count_or_size = struct.unpack_from('<I', data, fp+12)[0]
    print(f'  frame {i} @ 0x{fp:X}: cellxy=({cellx},{celly}) bbox=({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}) tail=0x{px_count_or_size:08X}={px_count_or_size}')
    # advance speculatively
    fp += 16 + px_count_or_size
    print(f'    next would be 0x{fp:X}')

# Try a different layout: header is just bbox (8 B) + u32 size, no cellxy
print()
print(f'=== try frame record: 12 B header (bbox+size) ===')
fp = pal_end
for i in range(n_show):
    if fp + 12 > len(data): break
    bbox = struct.unpack_from('<4h', data, fp)
    sz = struct.unpack_from('<I', data, fp+8)[0]
    print(f'  frame {i} @ 0x{fp:X}: bbox=({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}) size=0x{sz:08X}={sz}')
    fp += 12 + sz
    if fp > len(data): print(f'    overflow!'); break
    print(f'    next would be 0x{fp:X}')

for a in archives:
    a.close()
