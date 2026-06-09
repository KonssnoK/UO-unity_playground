"""Compare CC, EC legacy, and EC HD sprite dimensions for a sample of
static tiles to figure out HD's scaling convention. Output a histogram
of (HD width / Legacy width) and (HD height / Legacy height) ratios —
if HD is just a uniform 2x of legacy, the ratios should cluster at 2.0.
"""
from __future__ import annotations
import struct, sys, io
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")


def get_dims(arc, key):
    ent = arc.by_hash.get(hash_name(key))
    if not ent: return None
    try:
        dds = arc.read(ent)
        img = Image.open(io.BytesIO(dds)).convert('RGBA')
        bbox = img.getbbox() or (0, 0, img.width, img.height)
        return (img.width, img.height, bbox[2]-bbox[0], bbox[3]-bbox[1], bbox[0], bbox[1])
    except Exception:
        return None


def get_cc_dims(arc, item_id):
    art_id = 0x4000 + item_id
    buf = arc.get_by_name(f'build/artlegacymul/{art_id:08}.tga')
    if not buf or len(buf) < 12: return None
    w = struct.unpack_from('<H', buf, 4)[0]
    h = struct.unpack_from('<H', buf, 6)[0]
    return (w, h)


hd = UopArchive(EC / 'Texture.uop')
lg = UopArchive(EC / 'LegacyTexture.uop')
ccart = UopArchive(CC / 'artLegacyMUL.uop')

# Walk every entry in Texture.uop to find HD sprites for static item_ids
print("Scanning Texture.uop for static HD entries (sampling first 200 hits)...")
samples = []
for item_id in range(0, 0x4000):
    hd_dims = get_dims(hd, f'build/worldart/{item_id:08}.dds')
    if hd_dims is None: continue
    lg_dims = get_dims(lg, f'build/tileartlegacy/{item_id:08}.dds')
    cc_dims = get_cc_dims(ccart, item_id)
    samples.append((item_id, cc_dims, lg_dims, hd_dims))
    if len(samples) >= 200: break

print(f"\n{len(samples)} samples gathered\n")
print(f"{'item_id':>7}  {'CC w×h':<11}  {'Legacy canvas':<14}  {'Legacy visible':<22}  {'HD canvas':<14}  {'HD visible':<24}")
for item_id, cc, lg_dims, hd_dims in samples[:40]:
    cc_s  = f"{cc[0]}×{cc[1]}" if cc else "—"
    lg_s  = f"{lg_dims[0]}×{lg_dims[1]}" if lg_dims else "—"
    lg_vs = f"{lg_dims[2]}×{lg_dims[3]}@({lg_dims[4]},{lg_dims[5]})" if lg_dims else "—"
    hd_s  = f"{hd_dims[0]}×{hd_dims[1]}"
    hd_vs = f"{hd_dims[2]}×{hd_dims[3]}@({hd_dims[4]},{hd_dims[5]})"
    print(f"{item_id:>7}  {cc_s:<11}  {lg_s:<14}  {lg_vs:<22}  {hd_s:<14}  {hd_vs:<24}")

print()
print("# HD-canvas / Legacy-canvas ratio histogram (canvas-to-canvas):")
ratios_w = Counter()
ratios_h = Counter()
for item_id, cc, lg_dims, hd_dims in samples:
    if lg_dims is None: continue
    rw = round(hd_dims[0] / lg_dims[0], 2)
    rh = round(hd_dims[1] / lg_dims[1], 2)
    ratios_w[rw] += 1
    ratios_h[rh] += 1
print(f"  width ratios  top: {ratios_w.most_common(8)}")
print(f"  height ratios top: {ratios_h.most_common(8)}")

print()
print("# HD-visible / Legacy-visible ratio histogram:")
vrw = Counter()
vrh = Counter()
for item_id, cc, lg_dims, hd_dims in samples:
    if lg_dims is None or lg_dims[2] == 0: continue
    rw = round(hd_dims[2] / lg_dims[2], 2)
    rh = round(hd_dims[3] / lg_dims[3], 2)
    vrw[rw] += 1
    vrh[rh] += 1
print(f"  visible-w ratios top: {vrw.most_common(8)}")
print(f"  visible-h ratios top: {vrh.most_common(8)}")

print()
print("# HD-visible / CC-canvas ratio (HD sprite vs original CC art size):")
ccr_w = Counter(); ccr_h = Counter()
for item_id, cc, lg_dims, hd_dims in samples:
    if cc is None or cc[0] == 0: continue
    rw = round(hd_dims[2] / cc[0], 2)
    rh = round(hd_dims[3] / cc[1], 2)
    ccr_w[rw] += 1
    ccr_h[rh] += 1
print(f"  vis-w/CC-w top: {ccr_w.most_common(8)}")
print(f"  vis-h/CC-h top: {ccr_h.most_common(8)}")
hd.close(); lg.close(); ccart.close()
