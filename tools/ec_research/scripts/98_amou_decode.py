"""Robust AMOU parser + first attempt at decoding the pixel payload."""
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
    P = {}
    P['magic']      = data[:4]
    P['version']    = struct.unpack_from('<I', data, 4)[0]
    P['dsize']      = struct.unpack_from('<I', data, 8)[0]
    P['body_id']    = struct.unpack_from('<I', data, 0xC)[0]
    P['bbox']       = struct.unpack_from('<4h', data, 0x10)
    P['atlas_w']    = struct.unpack_from('<H', data, 0x18)[0]
    P['atlas_pad']  = struct.unpack_from('<H', data, 0x1A)[0]
    P['atlas_h']    = struct.unpack_from('<I', data, 0x1C)[0]
    P['nominal_count'] = struct.unpack_from('<I', data, 0x20)[0]
    P['pal_bytes']  = struct.unpack_from('<I', data, 0x24)[0]
    P['flags']      = data[0x28:0x30]

    pal_off = 0x30
    pal_end = pal_off + P['pal_bytes']
    P['palette'] = [(data[o], data[o+1], data[o+2], data[o+3])
                    for o in range(pal_off, pal_end, 4)]

    # Heuristic: walk table while entries look valid.
    gbbox = P['bbox']
    glb_minX, glb_minY, glb_maxX, glb_maxY = gbbox
    table_start = pal_end
    frames = []
    prev_off = 0
    cur = table_start
    while cur + 16 <= len(data):
        pad = struct.unpack_from('<H', data, cur)[0]
        idx = struct.unpack_from('<H', data, cur+2)[0]
        bbox = struct.unpack_from('<4h', data, cur+4)
        end_off = struct.unpack_from('<I', data, cur+12)[0]
        # Validity checks
        if pad != 0: break
        if not (idx < 1000): break
        if not (glb_minX - 1 <= bbox[0] <= glb_maxX): break
        if not (glb_minY - 1 <= bbox[1] <= glb_maxY): break
        if not (glb_minX <= bbox[2] <= glb_maxX + 1): break
        if not (glb_minY <= bbox[3] <= glb_maxY + 1): break
        if not (bbox[2] >= bbox[0] and bbox[3] >= bbox[1]): break
        if end_off <= prev_off: break
        if end_off > P['dsize']: break
        frames.append({'idx': idx, 'bbox': bbox, 'end_off': end_off})
        prev_off = end_off
        cur += 16
    P['frames'] = frames
    P['pixel_area_start'] = cur

    prev = 0
    for f in P['frames']:
        f['pixel_start'] = P['pixel_area_start'] + prev
        f['pixel_end']   = P['pixel_area_start'] + f['end_off']
        f['pixel_size']  = f['pixel_end'] - f['pixel_start']
        prev = f['end_off']
    return P


# Test on human male idle
data = fetch(400, 0)
P = parse_amou(data)
print(f'body={P["body_id"]} bbox={P["bbox"]} nominal_count={P["nominal_count"]}')
print(f'palette {len(P["palette"])} entries; table starts 0x{0x30 + P["pal_bytes"]:X}')
print(f'parsed {len(P["frames"])} valid frame entries')
print(f'pixel area starts 0x{P["pixel_area_start"]:X}, ends 0x{len(data):X}')
print(f'last frame end_off = {P["frames"][-1]["end_off"]} (expected {len(data) - P["pixel_area_start"]})')

# Examine first 5 frames' pixel data
print('\nFirst 5 frames:')
for f in P['frames'][:5]:
    bw = f['bbox'][2] - f['bbox'][0] + 1
    bh = f['bbox'][3] - f['bbox'][1] + 1
    nbytes = f['pixel_size']
    print(f'  idx={f["idx"]:3d} bbox={f["bbox"]} size={bw}x{bh}={bw*bh}px pixel_bytes={nbytes} ratio={nbytes/(bw*bh):.2f}')

# Look at first frame raw bytes
f0 = P['frames'][0]
pdata = data[f0['pixel_start']:f0['pixel_end']]
print(f'\n=== Frame 0 pixel ({len(pdata)} B), first 80 hex ===')
for i in range(0, 80, 16):
    print(f'  +0x{i:03X}: {pdata[i:i+16].hex()}')

# Hypothesis: line-by-line RLE — each row may start with a u16 count of pixels,
# then a stream of (count, color_index) or raw indices. Test the first u16 as row length.
print(f'\n--- first u16s of frame 0 pixel data ---')
for i in range(0, 32, 2):
    v = struct.unpack_from('<H', pdata, i)[0]
    print(f'  +{i:2d}: u16=0x{v:04X}={v}')

for a in archives:
    a.close()
