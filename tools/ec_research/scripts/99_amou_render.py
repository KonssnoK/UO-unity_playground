"""Try to decode AMOU pixel data using classic UO RLE (per-row run-length)
and render the first few frames to PNGs for visual verification.

Classic UO anim.mul format per frame:
    u16 width, u16 height, i16 cx, i16 cy
    [stream of u16 packed (offset, run_len) + pixel bytes]

EC AMOU frames already have a 16 B header in the index table (bbox), so the
pixel data starts directly with the run stream. We don't yet know the exact
packing — try a few variants.
"""
import io, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image

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
    pal_bytes = struct.unpack_from('<I', data, 0x24)[0]
    pal_end = 0x30 + pal_bytes
    palette = [(data[o], data[o+1], data[o+2], data[o+3]) for o in range(0x30, pal_end, 4)]
    gbbox = struct.unpack_from('<4h', data, 0x10)
    glb_minX, glb_minY, glb_maxX, glb_maxY = gbbox

    frames = []
    cur = pal_end
    prev_off = 0
    while cur + 16 <= len(data):
        pad = struct.unpack_from('<H', data, cur)[0]
        idx = struct.unpack_from('<H', data, cur+2)[0]
        bbox = struct.unpack_from('<4h', data, cur+4)
        end_off = struct.unpack_from('<I', data, cur+12)[0]
        if pad != 0 or idx >= 1000: break
        if not (glb_minX - 1 <= bbox[0] <= bbox[2] <= glb_maxX + 1): break
        if not (glb_minY - 1 <= bbox[1] <= bbox[3] <= glb_maxY + 1): break
        if end_off <= prev_off or end_off > len(data) - cur - 16: break
        frames.append({'idx': idx, 'bbox': bbox, 'end_off': end_off})
        prev_off = end_off
        cur += 16
    pixel_area_start = cur
    prev = 0
    for f in frames:
        f['pixel_start'] = pixel_area_start + prev
        f['pixel_end'] = pixel_area_start + f['end_off']
        prev = f['end_off']
    return palette, frames, gbbox


def palette_color(palette, idx):
    if idx >= len(palette): return (255, 0, 255, 255)   # error magenta
    r, g, b, a = palette[idx]
    # Treat 'a' field: 0 = opaque, 1 = transparent? Or A=255-a*255?
    # First pass: assume opaque, ignore the 4th byte flag
    return (r, g, b, 255)


def try_decode_classic_rle(pixel_bytes, bbox, palette):
    """Variant 3: byte-stream where high-bit set = skip transparent pixels,
    low-bit clear = literal palette index (a single pixel)."""
    bx0, by0, bx1, by1 = bbox
    w = bx1 - bx0 + 1
    h = by1 - by0 + 1
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))

    off = 0
    pos = 0   # linear pixel position
    total = w * h
    while off < len(pixel_bytes) and pos < total:
        b = pixel_bytes[off]
        off += 1
        if b & 0x80:
            # skip (b & 0x7F) pixels — or maybe (b & 0x7F)+1
            pos += (b & 0x7F)
        else:
            # literal palette index
            x = pos % w
            y = pos // w
            if y < h:
                img.putpixel((x, y), palette_color(palette, b))
            pos += 1
    return img


# Render first few frames of human male idle
data = fetch(400, 0)
palette, frames, gbbox = parse_amou(data)
print(f'parsed: {len(frames)} frames, palette {len(palette)} entries, global bbox {gbbox}')

OUT = Path(r"C:\src\ClassicUO\tools\ec_research\dump_amou")
OUT.mkdir(exist_ok=True)

for i, f in enumerate(frames[:6]):
    pdata = data[f['pixel_start']:f['pixel_end']]
    img = try_decode_classic_rle(pdata, f['bbox'], palette)
    if img is not None:
        path = OUT / f'frame_{i:02d}_idx{f["idx"]:03d}.png'
        # Upscale for visibility
        img2 = img.resize((img.width * 4, img.height * 4), Image.NEAREST)
        img2.save(path)
        print(f'  frame {i} idx={f["idx"]} bbox={f["bbox"]} -> {path}')

# Save palette as a strip too for inspection
PW = 16
PH = (len(palette) + PW - 1) // PW
pal_img = Image.new('RGBA', (PW * 16, PH * 16), (0, 0, 0, 255))
for i, (r, g, b, a) in enumerate(palette):
    for dy in range(16):
        for dx in range(16):
            pal_img.putpixel(((i % PW) * 16 + dx, (i // PW) * 16 + dy), (r, g, b, 255))
pal_img.save(OUT / 'palette.png')
print(f'palette image: {OUT / "palette.png"}')

for a in archives:
    a.close()
