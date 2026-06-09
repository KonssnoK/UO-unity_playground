"""Verified AMOU pixel decoder — ported from UOReader (Kons, 2013).

Source: UOReader_0.8.7 / UOFrameBin.cs + UOFrame.cs (decompiled).

Header layout (44 B) — CORRECTED vs prior speculation:
  0x00 [4]  magic 'AMOU' (4th byte unused in check)
  0x04 [4]  version
  0x08 [4]  total_size
  0x0C [4]  body_id
  0x10 [2]  init_x      (i16, NOT min_x — see bbox semantics)
  0x12 [2]  init_y
  0x14 [2]  end_x
  0x16 [2]  end_y
  0x18 [4]  colour_count
  0x1C [4]  colour_offset   (palette starts here, NOT at 0x30)
  0x20 [4]  frames_count    (REAL count — not nominal)
  0x24 [4]  frames_offset   (frame table starts here)
  (0x28..0x2F: typically 0 — was speculated "flags" in prior doc, actually unused/reserved)

Palette: colour_count × (R, G, B, alpha_flag)

Frame table at frames_offset, frames_count × 16 B:
  +0x00 u16  id (often 0)
  +0x02 u16  frame_index
  +0x04 4×i16  init_x, init_y, end_x, end_y
  +0x0C u32  data_offset_relative_to_frames_offset  (NOT cumulative end offset!)

Pixel area starts at frames_offset + frames_count * 16.
Frame i pixel stream begins at: frames_offset + i*16 + data_offset_field.
Width = end_x - init_x  (NO +1)
Height = end_y - init_y

Pixel stream — antialiased RLE:
  Position advances row-major across the bbox.
  Read byte b:
    if b < 128: skip b transparent pixels.
    else:
      Read byte b2. hi = b2 >> 4; lo = b2 & 0xF.
      if hi > 0: 1 anti-aliased edge pixel, blend palette[next byte] with
                 prior color at weight hi/16. Advance 1.
      Then (b - 128) solid pixels, palette index = next byte each. Advance 1 each.
      if lo > 0: 1 trailing anti-aliased pixel (same blend math, lo/16).
"""
import struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def fetch(body, action):
    arcs = [UopArchive(EC / f"AnimationFrame{i}.uop") for i in range(1, 7)]
    key = f"build/animationframe/{body:06}/{action:02}.bin"
    h = hash_name(key)
    try:
        for a in arcs:
            e = a.by_hash.get(h)
            if e:
                return a.read(e)
    finally:
        for a in arcs:
            a.close()
    return None


def parse_amou(data):
    assert data[:3] == b'AMO'
    version = struct.unpack_from('<I', data, 4)[0]
    total = struct.unpack_from('<I', data, 8)[0]
    body_id = struct.unpack_from('<I', data, 0x0C)[0]
    init_x, init_y, end_x, end_y = struct.unpack_from('<4h', data, 0x10)
    col_count = struct.unpack_from('<I', data, 0x18)[0]
    col_off = struct.unpack_from('<I', data, 0x1C)[0]
    frm_count = struct.unpack_from('<I', data, 0x20)[0]
    frm_off = struct.unpack_from('<I', data, 0x24)[0]

    palette = [tuple(data[col_off + i*4 + k] for k in range(4)) for i in range(col_count)]

    frames = []
    for i in range(frm_count):
        o = frm_off + i * 16
        fid, fidx = struct.unpack_from('<HH', data, o)
        fix, fiy, fex, fey = struct.unpack_from('<4h', data, o + 4)
        rel = struct.unpack_from('<I', data, o + 12)[0]
        pix_off = frm_off + i * 16 + rel
        frames.append({
            'id': fid, 'frame': fidx,
            'init_x': fix, 'init_y': fiy, 'end_x': fex, 'end_y': fey,
            'width': fex - fix, 'height': fey - fiy,
            'pixel_off': pix_off,
        })

    # compute per-frame byte sizes from cumulative pixel offsets
    pix_area_start = frm_off + frm_count * 16
    sorted_starts = sorted(set(f['pixel_off'] for f in frames)) + [total]
    next_after = {s: sorted_starts[i+1] for i, s in enumerate(sorted_starts[:-1])}
    for f in frames:
        f['pixel_end'] = next_after.get(f['pixel_off'], total)

    return {
        'version': version, 'total': total, 'body_id': body_id,
        'bbox': (init_x, init_y, end_x, end_y),
        'palette': palette, 'frames': frames,
        'pixel_area_start': pix_area_start,
    }


def _blend(c0, c1, w):
    # UOReader's odd long-arithmetic blend reduces to: out = c0*w/16 + c1*(16-w)/16
    # over each channel. (w is 1..15.)
    r = (c0[0] * w + c1[0] * (16 - w)) // 16
    g = (c0[1] * w + c1[1] * (16 - w)) // 16
    b = (c0[2] * w + c1[2] * (16 - w)) // 16
    return (r, g, b, 255)


def decode_frame(stream, width, height, palette):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    px = img.load()
    x, y = 0, 0

    def advance():
        nonlocal x, y
        x += 1
        if x >= width:
            x = 0
            y += 1

    off = 0
    while y < height and off < len(stream):
        b = stream[off]; off += 1
        if b < 128:
            for _ in range(b):
                advance()
                if y >= height:
                    return img
            continue
        b2 = stream[off]; off += 1
        hi = b2 >> 4
        lo = b2 & 0x0F
        if hi > 0:
            idx = stream[off]; off += 1
            base = palette[idx]
            prior = px[x, y]
            col = _blend(base, prior, hi)
            px[x, y] = col
            advance()
            if y >= height: return img
        for _ in range(b - 128):
            idx = stream[off]; off += 1
            r, g, bl, _a = palette[idx]
            px[x, y] = (r, g, bl, 255)
            advance()
            if y >= height: return img
        if lo > 0:
            idx = stream[off]; off += 1
            base = palette[idx]
            prior = px[x, y]
            col = _blend(base, prior, lo)
            px[x, y] = col
            advance()
    return img


if __name__ == '__main__':
    data = fetch(400, 0)
    P = parse_amou(data)
    print(f"body={P['body_id']} bbox={P['bbox']} palette={len(P['palette'])} frames={len(P['frames'])}")

    OUT = Path(r"C:\src\ClassicUO\tools\ec_research\dump_amou_decoded")
    OUT.mkdir(exist_ok=True)

    # palette strip
    palimg = Image.new('RGBA', (len(P['palette']) * 8, 32), (0, 0, 0, 255))
    for i, (r, g, b, a) in enumerate(P['palette']):
        for dy in range(32):
            for dx in range(8):
                palimg.putpixel((i*8+dx, dy), (r, g, b, 255))
    palimg.save(OUT / 'palette.png')

    for i, f in enumerate(P['frames'][:16]):
        stream = data[f['pixel_off']:f['pixel_end']]
        img = decode_frame(stream, f['width'], f['height'], P['palette'])
        img2 = img.resize((img.width * 3, img.height * 3), Image.NEAREST)
        img2.save(OUT / f"frame_{i:02d}_idx{f['frame']:03d}.png")
        print(f"  frame {i} idx={f['frame']} {f['width']}x{f['height']} bytes={len(stream)} -> ok")
