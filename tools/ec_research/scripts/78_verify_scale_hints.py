"""For each static tile that has both HD + CC art, check:
  - 0x0C (float) vs (HD visible W / CC visible W)
  - 0x10 (float) vs (HD visible H / CC visible H)
If 0x0C/0x10 are the per-tile HD-to-CC scale factors, the values should
match the measured ratios. Print correlation stats + outliers.
"""
import struct, sys, io
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")


def cc_visible(buf):
    if len(buf) < 12: return None
    w = struct.unpack_from('<H', buf, 4)[0]
    h = struct.unpack_from('<H', buf, 6)[0]
    line_offsets = struct.unpack_from(f'<{h}H', buf, 8)
    data_start = 8 + h * 2
    xmin = w; ymin = h; xmax = -1; ymax = -1
    for y in range(h):
        if line_offsets[y] == 0 and y != 0: continue
        ptr = data_start + line_offsets[y] * 2; x = 0
        while True:
            if ptr + 4 > len(buf): break
            xoffs = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
            run   = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
            if xoffs + run >= 2048 or xoffs + run == 0: break
            x += xoffs
            for _ in range(run):
                if ptr + 2 > len(buf): break
                val = struct.unpack_from('<H', buf, ptr)[0]; ptr += 2
                if val:
                    if x < xmin: xmin = x
                    if x > xmax: xmax = x
                    if y < ymin: ymin = y
                    if y > ymax: ymax = y
                x += 1
    if xmax < 0: return None
    return (xmax-xmin+1, ymax-ymin+1)


def hd_visible(arc, item_id):
    ent = arc.by_hash.get(hash_name(f'build/worldart/{item_id:08}.dds'))
    if not ent: return None
    try:
        img = Image.open(io.BytesIO(arc.read(ent))).convert('RGBA')
        bbox = img.getbbox()
        if not bbox: return None
        return (bbox[2]-bbox[0], bbox[3]-bbox[1])
    except Exception:
        return None


tileart = UopArchive(EC / 'tileart.uop')
hd      = UopArchive(EC / 'Texture.uop')
ccart   = UopArchive(CC / 'artLegacyMUL.uop')

ratios = []
print(f"{'item_id':>7}  {'0x0C':>6}  {'HD_W/CC_W':>10}  {'0x10':>6}  {'HD_H/CC_H':>10}  match?")
shown = 0
for item_id in range(0, 0x4000):
    art_id = 0x4000 + item_id
    ent = tileart.by_hash.get(hash_name(f'build/tileart/{art_id:08}.bin'))
    if not ent: continue
    p = tileart.read(ent)
    if len(p) < 0x14: continue
    f_0c = struct.unpack_from('<f', p, 0x0C)[0]
    f_10 = struct.unpack_from('<f', p, 0x10)[0]

    hd_vis = hd_visible(hd, item_id)
    if hd_vis is None: continue

    cc_buf = ccart.get_by_name(f'build/artlegacymul/{art_id:08}.tga')
    if not cc_buf: continue
    cc_vis = cc_visible(cc_buf)
    if cc_vis is None: continue

    rw = hd_vis[0] / cc_vis[0]
    rh = hd_vis[1] / cc_vis[1]
    ratios.append((f_0c, rw, f_10, rh))
    if shown < 40:
        m = "OK" if abs(f_10 - rh) < 0.1 else "no"
        print(f"{item_id:>7}  {f_0c:6.3f}  {rw:10.3f}  {f_10:6.3f}  {rh:10.3f}  {m}")
        shown += 1
    if len(ratios) >= 500: break

# Stats: for tiles where 0x0C == 1.0 and 0x10 == 1.5, what does the HD/CC ratio look like?
print(f"\nGathered {len(ratios)} pairs\n")

# Histogram of 0x10 values
c10 = Counter(round(f, 2) for _, _, f, _ in ratios)
print("0x10 value distribution:", c10.most_common(8))

# For tiles where 0x10 == 1.5, what's the actual height ratio?
group_15 = [r for f0c, _, f10, r in ratios if abs(f10 - 1.5) < 0.01]
group_10 = [r for f0c, _, f10, r in ratios if abs(f10 - 1.0) < 0.01]
print(f"\nFor 0x10 == 1.5 ({len(group_15)} tiles):")
if group_15:
    print(f"  HD/CC height ratio mean={sum(group_15)/len(group_15):.3f}, median={sorted(group_15)[len(group_15)//2]:.3f}")
print(f"For 0x10 == 1.0 ({len(group_10)} tiles):")
if group_10:
    print(f"  HD/CC height ratio mean={sum(group_10)/len(group_10):.3f}, median={sorted(group_10)[len(group_10)//2]:.3f}")

tileart.close(); hd.close(); ccart.close()
