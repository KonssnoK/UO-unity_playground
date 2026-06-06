"""Compare AMOU vs classic anim.mul frame dimensions for the same body/action.

Picks a body (default 400 = human male) and dumps frame 0 / dir 0:
  CC mul:  (W, H, CenterX, CenterY)
  AMOU:    main bbox (W, H), per-frame init/end, post-canvas dims

Then writes a side-by-side PNG so you can eyeball scale.

Usage:
    python compare_anim_dims.py [body] [action]
"""
import struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(r"C:\src\ClassicUO\tools\ec_research")))
from ec.uop import UopArchive, hash_name
from PIL import Image

CC_ROOT = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
EC_ROOT = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

# ---------- AMOU (EC) ----------
def fetch_amou(body, action):
    arcs = [UopArchive(EC_ROOT / f"AnimationFrame{i}.uop") for i in range(1, 7)]
    key = f"build/animationframe/{body:06}/{action:02}.bin"
    h = hash_name(key)
    try:
        for a in arcs:
            e = a.by_hash.get(h)
            if e: return a.read(e)
    finally:
        for a in arcs:
            a.close()
    return None

def parse_amou(data):
    main_init_x, main_init_y, main_end_x, main_end_y = struct.unpack_from('<4h', data, 0x10)
    col_count = struct.unpack_from('<I', data, 0x18)[0]
    col_off   = struct.unpack_from('<I', data, 0x1C)[0]
    frm_count = struct.unpack_from('<I', data, 0x20)[0]
    frm_off   = struct.unpack_from('<I', data, 0x24)[0]
    palette = [tuple(data[col_off + i*4 + k] for k in range(4)) for i in range(col_count)]
    frames = []
    for i in range(frm_count):
        o = frm_off + i * 16
        ix, iy, ex, ey = struct.unpack_from('<4h', data, o + 4)
        rel = struct.unpack_from('<I', data, o + 12)[0]
        frames.append({
            'init_x': ix, 'init_y': iy, 'end_x': ex, 'end_y': ey,
            'w': ex - ix, 'h': ey - iy,
            'pixel_off': frm_off + i * 16 + rel,
        })
    total = struct.unpack_from('<I', data, 8)[0]
    sorted_starts = sorted(set(f['pixel_off'] for f in frames)) + [total]
    nxt = {s: sorted_starts[i+1] for i, s in enumerate(sorted_starts[:-1])}
    for f in frames:
        f['pixel_end'] = nxt.get(f['pixel_off'], total)
    return {
        'main': (main_init_x, main_init_y, main_end_x, main_end_y),
        'main_w': main_end_x - main_init_x,
        'main_h': main_end_y - main_init_y,
        'palette': palette, 'frames': frames,
    }

def _blend(c0, c1, w):
    return tuple((c0[k]*w + c1[k]*(16-w)) // 16 for k in range(3)) + (255,)

def decode_amou_frame(stream, w, h, palette):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = img.load()
    pos, off = 0, 0
    total = w * h
    while pos < total and off < len(stream):
        b = stream[off]; off += 1
        if b < 128:
            pos += b
            continue
        b2 = stream[off]; off += 1
        hi, lo = b2 >> 4, b2 & 0xF
        nsolid = b - 128
        if hi > 0 and pos < total:
            idx = stream[off]; off += 1
            prior = px[pos % w, pos // w]
            base = palette[idx]
            px[pos % w, pos // w] = _blend(base, prior, hi)
            pos += 1
        for _ in range(nsolid):
            if pos >= total or off >= len(stream): break
            idx = stream[off]; off += 1
            r, g, b_, _a = palette[idx]
            px[pos % w, pos // w] = (r, g, b_, 255)
            pos += 1
        if lo > 0 and pos < total:
            idx = stream[off]; off += 1
            prior = px[pos % w, pos // w]
            base = palette[idx]
            px[pos % w, pos // w] = _blend(base, prior, lo)
            pos += 1
    return img


# ---------- CC anim.mul (classic) ----------
def cc_anim_path():
    p = CC_ROOT / "anim.mul"
    if p.exists(): return p, CC_ROOT / "anim.idx"
    return None, None

def cc_load_frame(body, action, direction, frame_idx):
    """Pull a single CC frame from anim.mul/anim.idx."""
    mul, idx = cc_anim_path()
    if mul is None: return None
    # Entry index in anim.idx: high bodies use complex math, but for body 400
    # this approximates: idx_entry = body * 110 + action * 5 + direction
    # (110 = max actions × 5 dirs for human-male in body 400's group;
    # for absolute correctness use bodyConv.def — outside scope here).
    entry = body * 110 + action * 5 + direction
    with open(idx, 'rb') as f:
        f.seek(entry * 12)
        e = f.read(12)
    if len(e) < 12: return None
    offset, length, _extra = struct.unpack('<iii', e)
    if offset == -1 or length <= 0: return None
    with open(mul, 'rb') as f:
        f.seek(offset)
        buf = f.read(length)
    # Palette: 256 × u16
    palette = struct.unpack_from('<256H', buf, 0)
    # frame_offsets table follows
    frame_count = struct.unpack_from('<I', buf, 512)[0]
    if frame_idx >= frame_count: return None
    fp_off = struct.unpack_from('<I', buf, 516 + frame_idx * 4)[0] + 512
    cx, cy, w, h = struct.unpack_from('<hhhh', buf, fp_off)
    return {'w': w, 'h': h, 'cx': cx, 'cy': cy, 'offset': offset, 'length': length}


# ---------- main ----------
if __name__ == '__main__':
    body = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    action = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    amou_data = fetch_amou(body, action)
    if amou_data is None:
        print(f"AMOU: no entry for body={body} action={action}")
    else:
        P = parse_amou(amou_data)
        print(f"\n=== AMOU body={body} action={action} ===")
        print(f"  main bbox: {P['main']}  → {P['main_w']}×{P['main_h']}")
        print(f"  frame count: {len(P['frames'])}")
        for i, f in enumerate(P['frames'][:5]):
            print(f"    frame {i:2d}: init=({f['init_x']:3d},{f['init_y']:3d})  end=({f['end_x']:3d},{f['end_y']:3d})  {f['w']}×{f['h']}")

    cc = cc_load_frame(body, action, 0, 0)
    if cc is None:
        print(f"\nCC: no entry for body={body} action={action} dir=0 frame=0 (might need bodyConv.def mapping)")
    else:
        print(f"\n=== CC anim.mul body={body} action={action} dir=0 frame=0 ===")
        print(f"  {cc['w']}×{cc['h']}  center=({cc['cx']},{cc['cy']})")

    if amou_data is not None and cc is not None:
        ratio_w = P['main_w'] / cc['w']
        ratio_h = P['main_h'] / cc['h']
        print(f"\n=== RATIO ===")
        print(f"  AMOU main / CC frame0:  W {ratio_w:.3f}×  H {ratio_h:.3f}×")

    # Save a montage of frame 0
    if amou_data is not None:
        OUT = Path(r"C:\src\ClassicUO\tools\ec_research\dump_anim_compare")
        OUT.mkdir(exist_ok=True)
        f0 = P['frames'][0]
        stream = amou_data[f0['pixel_off']:f0['pixel_end']]
        img = decode_amou_frame(stream, f0['w'], f0['h'], P['palette'])
        img.save(OUT / f"amou_{body}_{action}_f00.png")
        print(f"\nWrote: {OUT / f'amou_{body}_{action}_f00.png'}")
