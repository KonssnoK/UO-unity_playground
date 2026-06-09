"""Decode AMOU frame pixel data.

Verified structure so far:
  0x00..0x1F   header (magic 'AMOU', version, dsize, body_id, bbox, atlas_w/h)
  0x20..0x23   u32 frame_count
  0x24..0x27   u32 palette_byte_size (= num_colors * 4)
  0x28..0x2F   8 bytes flags / per-body data
  0x30..pe     palette: num_colors * (u8 R, u8 G, u8 B, u8 alpha-flag)
  pe..pe+N16   frame index table: N entries * 16 B = (u16=0, u16 idx,
                                                       i16x4 bbox,
                                                       u32 end_offset_in_pixel_area)
  pe+N16..end  pixel area; each frame's bytes are [prev_end_offset .. this_end_offset)
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

def parse_amou(data):
    out = {}
    out['magic']      = data[:4]
    out['version']    = struct.unpack_from('<I', data, 4)[0]
    out['dsize']      = struct.unpack_from('<I', data, 8)[0]
    out['body_id']    = struct.unpack_from('<I', data, 0xC)[0]
    out['bbox']       = struct.unpack_from('<4h', data, 0x10)
    out['atlas_w']    = struct.unpack_from('<H', data, 0x18)[0]
    out['atlas_pad']  = struct.unpack_from('<H', data, 0x1A)[0]
    out['atlas_h']    = struct.unpack_from('<I', data, 0x1C)[0]
    out['frame_count']= struct.unpack_from('<I', data, 0x20)[0]
    out['pal_bytes']  = struct.unpack_from('<I', data, 0x24)[0]
    out['flags']      = data[0x28:0x30]

    pal_off = 0x30
    pal_end = pal_off + out['pal_bytes']
    palette = []
    for o in range(pal_off, pal_end, 4):
        r, g, b, a = data[o], data[o+1], data[o+2], data[o+3]
        palette.append((r, g, b, a))
    out['palette'] = palette

    # Frame index table: frame_count entries × 16 B
    table_start = pal_end
    table_end = table_start + out['frame_count'] * 16
    frames = []
    for i in range(out['frame_count']):
        o = table_start + i * 16
        pad      = struct.unpack_from('<H', data, o)[0]
        idx      = struct.unpack_from('<H', data, o+2)[0]
        fbbox    = struct.unpack_from('<4h', data, o+4)
        end_off  = struct.unpack_from('<I', data, o+12)[0]
        frames.append({'idx': idx, 'pad': pad, 'bbox': fbbox, 'end_off': end_off})
    out['frames'] = frames
    out['pixel_area_start'] = table_end

    # Pixel slices per frame
    prev = 0
    for f in frames:
        f['pixel_start'] = out['pixel_area_start'] + prev
        f['pixel_end']   = out['pixel_area_start'] + f['end_off']
        f['pixel_size']  = f['pixel_end'] - f['pixel_start']
        prev = f['end_off']
    return out

# Test on human male idle
data = fetch(400, 0)
P = parse_amou(data)
print(f'body_id={P["body_id"]} frame_count={P["frame_count"]} palette={len(P["palette"])} bbox={P["bbox"]}')
print(f'palette starts 0x30, ends 0x{0x30 + P["pal_bytes"]:X}')
print(f'frame table starts 0x{0x30 + P["pal_bytes"]:X}, pixel area starts 0x{P["pixel_area_start"]:X}')
print(f'data ends at 0x{len(data):X}; pixel area expected end = 0x{P["pixel_area_start"] + P["frames"][-1]["end_off"]:X}')
print()
print('First 6 frames:')
for f in P['frames'][:6]:
    print(f'  idx={f["idx"]:3d} pad=0x{f["pad"]:04X} bbox={f["bbox"]} pixel_size={f["pixel_size"]} pixel_start=0x{f["pixel_start"]:X}')

# Examine first frame's pixel bytes
f0 = P['frames'][0]
pdata = data[f0['pixel_start']:f0['pixel_end']]
print(f'\n=== Frame 0 pixel bytes (size {len(pdata)}) ===')
print(f'  first 64: {pdata[:64].hex()}')
print(f'  last 32:  {pdata[-32:].hex()}')

# Frame bbox: width = max_x - min_x, height = max_y - min_y
mn_x, mn_y, mx_x, mx_y = f0['bbox']
fw = mx_x - mn_x + 1
fh = mx_y - mn_y + 1
print(f'  bbox: ({mn_x},{mn_y})..({mx_x},{mx_y})  size {fw}x{fh} pixels = {fw*fh} total')
print(f'  if 1 byte/pixel (indexed palette): {fw*fh} bytes raw vs {len(pdata)} actual')
print(f'  → ratio {len(pdata)/(fw*fh):.2f}  (1.0 = uncompressed indices)')

# Look for RLE marker / common compressed-format hints
from collections import Counter
c = Counter(pdata)
top = c.most_common(8)
print(f'  byte freq top: {top}')

for a in archives:
    a.close()
