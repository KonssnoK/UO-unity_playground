"""Render the iso-diamond preview for surface tiles offline.

For each tile in the slate-roof group, this simulates exactly what
WriteIsoDiamondAt would produce on screen: take the master HD texture,
crop per the tile's EcImage rect (or default 44×44), then warp that
sub-rect into a 44×44 iso diamond — same vertex / UV layout as the
in-engine quad. Saves PNGs in a single side-by-side sheet so we can
inspect them without launching the client.
"""
import io, struct, sys, bisect
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name
from PIL import Image, ImageDraw

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
hd = UopArchive(EC / 'Texture.uop')
lt = UopArchive(EC / 'LegacyTexture.uop')
ta = UopArchive(EC / 'tileart.uop')
sd_arc = UopArchive(EC / 'string_dictionary.uop')

sd = sd_arc.read(list(sd_arc.by_hash.values())[0])
entries = {}
pos = 0
while pos + 2 < len(sd):
    n = struct.unpack_from('<H', sd, pos)[0]
    if n == 0 or n > 1024: pos += 1; continue
    if pos + 2 + n > len(sd): break
    tb = sd[pos+2:pos+2+n]
    if all(0x20 <= b < 0x80 or b in (0x09, 0x0a) for b in tb):
        entries[pos] = tb.decode('utf-8'); pos += 2 + n; continue
    pos += 1
starts = sorted(entries)
def lookup_str(off):
    i = bisect.bisect_right(starts, off) - 1
    if i < 0: return None
    s = starts[i]
    return entries[s] if off <= s + 2 + len(entries[s]) else None


def get_ecimage(tile):
    aid = 0x4000 + tile
    e = ta.by_hash.get(hash_name(f'build/tileart/{aid:08}.bin'))
    if not e: return None, None
    p = ta.read(e)
    sd_off = struct.unpack_from('<I', p, 0x02)[0]
    ec = struct.unpack_from('<6i', p, 0x4D)
    return ec, lookup_str(sd_off)


def find_master_for(tile):
    """Pick the first tile in this tile's sd-name group that has its own HD."""
    _, my_name = get_ecimage(tile)
    if not my_name: return tile if hd.by_hash.get(hash_name(f'build/worldart/{tile:08}.dds')) else None
    # Walk backward to find the nearest HD owner with the same name.
    for t in range(tile, -1, -1):
        if hd.by_hash.get(hash_name(f'build/worldart/{t:08}.dds')):
            _, n = get_ecimage(t)
            if n == my_name:
                return t
    return None


def is_fully_opaque_dds(dds: bytes) -> bool:
    """Match the runtime IsFullyOpaqueDds gate: DXT1 = always opaque;
    DXT5 = scan a0/a1 of every block (16-byte stride) and require both = 255."""
    if len(dds) < 128: return False
    if dds[:4] != b'DDS ': return False
    fourcc = dds[84:88]
    if fourcc == b'DXT1': return True
    if fourcc != b'DXT5': return False
    off = 128
    while off + 16 <= len(dds):
        if dds[off] != 255 or dds[off + 1] != 255: return False
        off += 16
    return True


def warp_to_diamond(src_img, target_size=44):
    """Map src_img (any size) corner-to-corner onto an inscribed diamond
    inside a target_size×target_size canvas. Same UV mapping as WriteIsoDiamondAt:
      top    (TARGET/2, 0)        UV (0, 0)
      right  (TARGET, TARGET/2)   UV (1, 0)
      left   (0, TARGET/2)        UV (0, 1)
      bottom (TARGET/2, TARGET)   UV (1, 1)
    For each output pixel inside the diamond, compute its barycentric
    position in the diamond, derive UV via bilinear interpolation of the
    four corner UVs, sample the source image, write the pixel.
    """
    T = target_size
    out = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    sw, sh = src_img.size
    for y in range(T):
        for x in range(T):
            # Check if inside diamond: |x - T/2|/(T/2) + |y - T/2|/(T/2) <= 1
            dx = abs(x - T/2.0) / (T/2.0)
            dy = abs(y - T/2.0) / (T/2.0)
            if dx + dy > 1.0: continue
            # Barycentric in the diamond:
            #   alpha = (x_normalized + y_normalized) / 2 with proper origin
            # Easier: bilinear with axes rotated 45°.
            # Diamond local coords: u_axis = (1,1)/sqrt2 (top→bottom), v_axis = (1,-1)/sqrt2 (left→right)
            # x_n = x / (T-1), y_n = y / (T-1)
            # We want UV such that:
            #   pixel(T/2, 0)      -> uv (0, 0)     [top]
            #   pixel(T,   T/2)    -> uv (1, 0)     [right]
            #   pixel(0,   T/2)    -> uv (0, 1)     [left]
            #   pixel(T/2, T)      -> uv (1, 1)     [bottom]
            # By inspection:
            #   u = (x + y - T/2) / T    so top→0, right→1/2+1/2=1, left→-1/2+1/2=0, bottom→1/2+1/2=1
            #   wait: top(T/2,0):    (T/2 + 0 - T/2)/T = 0      ✓
            #         right(T,T/2):  (T + T/2 - T/2)/T = 1       ✓
            #         left(0,T/2):   (0 + T/2 - T/2)/T = 0       ✓
            #         bottom(T/2,T): (T/2 + T - T/2)/T = 1       ✓
            #   v = (y - x + T/2) / T
            #         top:    (0 - T/2 + T/2)/T = 0              ✓
            #         right:  (T/2 - T + T/2)/T = 0              ✓
            #         left:   (T/2 - 0 + T/2)/T = 1              ✓
            #         bottom: (T - T/2 + T/2)/T = 1              ✓
            u = (x + y - T/2.0) / float(T)
            v = (y - x + T/2.0) / float(T)
            if u < 0: u = 0
            if v < 0: v = 0
            if u > 1: u = 1
            if v > 1: v = 1
            sx = int(round(u * (sw - 1)))
            sy = int(round(v * (sh - 1)))
            out.putpixel((x, y), src_img.getpixel((sx, sy)))
    return out


OUT = Path(r"C:\src\ClassicUO\tools\ec_research\dump_iso_diamond")
OUT.mkdir(exist_ok=True)

# Slate-roof group only — 1414 starts a different group (palm-frond, alpha sprite).
TILES = list(range(1406, 1414))
panels = []
for tile in TILES:
    ec, name = get_ecimage(tile)
    if ec is None:
        panels.append((tile, None, "no record")); continue
    master_tile = find_master_for(tile)
    own_hd_e = hd.by_hash.get(hash_name(f'build/worldart/{tile:08}.dds'))
    if not master_tile:
        # No master found; render the legacy DDS as-is (CC equivalent)
        leg = lt.by_hash.get(hash_name(f'build/tileartlegacy/{tile:08}.dds'))
        if leg:
            d = lt.read(leg)
            src = Image.open(io.BytesIO(d)).convert('RGBA')
            panels.append((tile, src, f"LEGACY (no master)"))
        else:
            panels.append((tile, None, "no master, no legacy"))
        continue
    master_dds = hd.read(hd.by_hash[hash_name(f'build/worldart/{master_tile:08}.dds')])
    master = Image.open(io.BytesIO(master_dds)).convert('RGBA')
    # Match in-engine gate: only warp to diamond when the master is a
    # tileable terrain texture (fully opaque). Otherwise render as a
    # regular alpha-trimmed sprite — same as ChunkMesh would do.
    if not is_fully_opaque_dds(master_dds):
        bbox = master.getbbox() or (0, 0, master.width, master.height)
        sprite = master.crop(bbox)
        panels.append((tile, sprite, f"SPRITE (alpha-trim {bbox})"))
        continue
    # Crop per EcImage (+1) or default 44x44
    if ec[2] > 0 and ec[3] > 0:
        x0, y0, x1, y1 = ec[0], ec[1], ec[2] + 1, ec[3] + 1
    else:
        x0, y0, x1, y1 = 0, 0, 44, 44
    x0 = max(0, min(master.width,  x0))
    y0 = max(0, min(master.height, y0))
    x1 = max(x0 + 1, min(master.width,  x1))
    y1 = max(y0 + 1, min(master.height, y1))
    crop = master.crop((x0, y0, x1, y1))
    diamond = warp_to_diamond(crop, 44)
    # Also pull legacy for comparison
    leg_img = None
    leg = lt.by_hash.get(hash_name(f'build/tileartlegacy/{tile:08}.dds'))
    if leg:
        leg_img = Image.open(io.BytesIO(lt.read(leg))).convert('RGBA')
    panels.append((tile, (master_tile, ec, crop, diamond, leg_img), f"master={master_tile} crop={(x0, y0, x1-x0, y1-y0)}"))

# Build a sheet
PAD = 12
ROW_H = 64 + 64 + 64 + 32  # master crop, diamond, legacy, labels
COL_W = 110
N = len(panels)
W = COL_W * N + PAD
H = ROW_H + PAD * 2 + 24
sheet = Image.new('RGBA', (W, H), (30, 30, 30, 255))
dr = ImageDraw.Draw(sheet)


def paste_centered(canvas, img, cx, cy):
    x = int(cx - img.width / 2)
    y = int(cy - img.height / 2)
    canvas.paste(img, (x, y), img)


for i, (tile, data, label) in enumerate(panels):
    col_x = PAD + i * COL_W + COL_W // 2
    dr.text((col_x - 30, PAD), f'tile {tile}', fill=(255, 255, 255, 255))
    if data is None:
        dr.text((col_x - 30, PAD + 20), str(label), fill=(200, 100, 100, 255))
        continue
    if isinstance(data, Image.Image):
        # Legacy fallback case
        paste_centered(sheet, data, col_x, PAD + 60)
        dr.text((col_x - 30, PAD + 96), str(label), fill=(200, 200, 100, 255))
        continue
    master_tile, ec, crop, diamond, leg = data
    # Row 1: crop (master's sub-rect)
    crop_show = crop.resize((min(64, crop.width), min(64, crop.height)),
                            Image.NEAREST) if max(crop.size) > 64 else crop
    paste_centered(sheet, crop_show, col_x, PAD + 60)
    dr.text((col_x - 30, PAD + 96), 'CROP', fill=(180, 180, 180, 255))
    # Row 2: diamond (warp of crop)
    paste_centered(sheet, diamond, col_x, PAD + 60 + 76)
    dr.text((col_x - 30, PAD + 60 + 76 + 24), 'DIAMOND', fill=(140, 220, 140, 255))
    # Row 3: legacy if exists
    if leg is not None:
        paste_centered(sheet, leg, col_x, PAD + 60 + 76 + 76)
        dr.text((col_x - 30, PAD + 60 + 76 + 76 + 36), 'LEGACY', fill=(180, 180, 220, 255))

out_path = OUT / 'iso_diamond_sheet.png'
sheet.save(out_path)
print(f'wrote {out_path}')

# Also save individual files for tiles
for tile, data, label in panels:
    if data is None or isinstance(data, Image.Image): continue
    master_tile, ec, crop, diamond, leg = data
    diamond.save(OUT / f'tile_{tile}_diamond.png')

ta.close(); hd.close(); lt.close(); sd_arc.close()
