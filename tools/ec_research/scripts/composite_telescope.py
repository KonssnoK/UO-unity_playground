"""Composite multi 207 (telescope) using UOReader's exact EC formula.
Produces telescope_composite.png and a per-tile debug table."""
import sys, struct, io
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(r"C:\src\ClassicUO\tools\ec_research")))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
mc = UopArchive(EC / "MultiCollection.uop")
ta = UopArchive(EC / "TileArt.uop")
tx = UopArchive(EC / "Texture.uop")

# Variable-length multi record parser (matches UOReader.Multi/MultiItem.cs Load):
data = mc.read(mc.by_hash[hash_name("build/multicollection/000207.bin")])
class R:
    def __init__(self, b): self.b=b; self.o=0
    def u16(self): v=struct.unpack_from('<H',self.b,self.o)[0]; self.o+=2; return v
    def i16(self): v=struct.unpack_from('<h',self.b,self.o)[0]; self.o+=2; return v
    def u32(self): v=struct.unpack_from('<I',self.b,self.o)[0]; self.o+=4; return v
    def i32(self): v=struct.unpack_from('<i',self.b,self.o)[0]; self.o+=4; return v
    def u8(self):  v=self.b[self.o]; self.o+=1; return v
r = R(data)
multi_id = r.u32(); count = r.u32()
tiles = []
for _ in range(count):
    g = r.u16(); x = r.i16(); y = r.i16(); z = r.i16()
    z = z & 0xFF
    if z >= 128: z -= 256  # sbyte
    u1 = r.u8(); u2 = r.u8()
    sc = r.u32()
    strs = []
    for _ in range(sc):
        n = r.i32(); strs.append(n)
    tiles.append((g, x, y, z, u1, u2, strs))
print(f"multi {multi_id}  tiles={len(tiles)}  unique_graphics={len(set(t[0] for t in tiles))}")
in_range = [t for t in tiles if 5209 <= t[0] <= 5274]
print(f"  in 5209-5274: {len(in_range)}")
xs = [t[1] for t in tiles]; ys = [t[2] for t in tiles]; zs = [t[3] for t in tiles]
print(f"  x={min(xs)}..{max(xs)}  y={min(ys)}..{max(ys)}  z={min(zs)}..{max(zs)}")

# Parse tileart record to get EcImage [X0,Y0,X1,Y1,dx,dy] and WorldArt[0].sd_index
sd = UopArchive(EC / "string_dictionary.uop")
sd_blob = sd.read(sd.by_hash[hash_name("build/stringdictionary/string_dictionary.bin")])
strings = []
p = 14; cnt = struct.unpack_from('<I', sd_blob, 8)[0]
for _ in range(cnt):
    L = struct.unpack_from('<H', sd_blob, p)[0]; p += 2
    strings.append(sd_blob[p:p+L].decode('ascii', errors='replace')); p += L

def parse_tileart(tile_id):
    e = ta.by_hash.get(hash_name(f"build/tileart/{tile_id:08d}.bin"))
    if e is None: return None
    buf = ta.read(e); r = R(buf)
    r.u16(); r.u32(); r.u32(); r.u8(); r.u8()
    struct.unpack_from('<ff', r.b, r.o); r.o += 8
    r.u32(); r.u32(); r.u32(); r.u32(); r.u8()
    struct.unpack_from('<f', r.b, r.o); r.o += 4
    r.u32(); struct.unpack_from('<ff', r.b, r.o); r.o += 8
    r.u32(); 
    r.o += 8 + 8 + 4  # u64 + u64 + u32
    # EcImage 6×i32, LegacyImage 6×i32
    ec_rect = [r.i32() for _ in range(6)]   # X0,Y0,X1,Y1,dx,dy
    leg_rect = [r.i32() for _ in range(6)]
    # SUB_9_1, SUB_9_2 (tile-trans / texture-trans tables)
    n = r.u8()
    for _ in range(n): r.u8(); r.u32()
    n = r.u8()
    for _ in range(n): r.u8(); r.u32()
    c = r.u32()
    for _ in range(c): r.u32(); r.u32()
    # SUB_9_4 with continue-fix
    c32 = r.u32()
    for _ in range(c32):
        v = r.u8()
        if v == 0:
            sc = r.u32()
            for _ in range(sc): r.u32(); r.u32()
        elif v == 1:
            r.u8(); r.u32()
    s = r.u8()
    if s != 0: r.u32(); r.u32(); r.u32(); r.u32()
    r.u8(); r.u8(); r.u8(); r.u8()
    # WorldArt group
    val = r.u8()
    sd_idx = -1
    if val != 0:
        r.u8(); shader = r.u32(); cnt2 = r.u8()
        if cnt2 > 0:
            sd_idx = r.u32()
            r.u8(); struct.unpack_from('<f', r.b, r.o); r.o += 4
            r.u32(); r.u32()
            for _ in range(cnt2 - 1):
                r.u32(); r.u8(); r.u32(); r.u32(); r.u32()
    return ec_rect, leg_rect, sd_idx

# Composite using EC formula (cell_half=32, z_scale=6)
import os
W = 2400; H = 1600
img = Image.new("RGBA", (W, H), (40, 40, 40, 255))
cx, cy = 400, 1300

debug_lines = []
ddsdec_path = Path("C:/src/ClassicUO/tools/ec_research")
sys.path.insert(0, str(ddsdec_path))
def load_dds(blob, w_hint=None, h_hint=None):
    """Load DDS bytes via PIL via fallback to BC3 decode."""
    try:
        return Image.open(io.BytesIO(blob)).convert("RGBA")
    except Exception:
        # Fallback minimal DXT5 decode
        return None

ordered = sorted(tiles, key=lambda t: (t[3], t[2], t[1]))
for tile in ordered:
    if not (5209 <= tile[0] <= 5274): continue
    g, x, y, z, u1, u2, _ = tile
    res = parse_tileart(g)
    if res is None: continue
    ec_rect, leg_rect, sd_idx = res
    X0, Y0, X1, Y1, dx, dy = ec_rect
    # WorldArt sd_idx -> sprite id
    if sd_idx < 0 or sd_idx >= len(strings): continue
    s = strings[sd_idx]
    # Expect path like Data\WorldArt\00012345_Name.tga
    import re
    m = re.search(r'(\d{8})', s)
    if not m: continue
    sprite_id = int(m.group(1))
    dds_path = f"build/worldart/{sprite_id:08d}.dds"
    h = hash_name(dds_path)
    if h not in tx.by_hash: continue
    blob = tx.read(tx.by_hash[h])
    img_tile = load_dds(blob)
    if img_tile is None: continue
    # EC formula:
    cell_half = 32; zscale = 6
    srcW = X1 - X0 + 1; srcH = Y1 - Y0 + 1
    if srcW <= 0 or srcH <= 0: continue
    px = cx + (x - y) * cell_half
    py = cy + (x + y) * cell_half
    if srcW % 2 == 1: px -= 1
    px -= cell_half
    py += (5 - z) * zscale
    py -= srcH
    py += dy
    px += dx
    # Crop & paste
    crop = img_tile.crop((X0, Y0, X1+1, Y1+1))
    img.paste(crop, (px, py), crop)
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    d.rectangle([px, py, px+srcW-1, py+srcH-1], outline=(255,0,0,255), width=1)
    debug_lines.append(f"g={g} sprite={sprite_id} xyz=({x},{y},{z}) rect=({X0},{Y0},{X1},{Y1}) dx={dx} dy={dy} -> ({px},{py})")

out_dir = Path(r"C:\src\ClassicUO\tools\ec_research\out")
out_dir.mkdir(exist_ok=True)
# Crop to non-empty bbox
bbox = img.getbbox()
img_c = img.crop(bbox) if bbox else img
img_c.save(out_dir / "telescope_composite.png")
(out_dir / "telescope_debug.txt").write_text("\n".join(debug_lines))
print(f"\nSaved {out_dir / 'telescope_composite.png'} ({img_c.size})")
print(f"Saved {out_dir / 'telescope_debug.txt'}")

# === Also produce CC-scale version of same multi for direct compare ===
img2 = Image.new("RGBA", (W, H), (40, 40, 40, 255))
for tile in ordered:
    g, x, y, z, u1, u2, _ = tile
    if not (5209 <= g <= 5274): continue
    res = parse_tileart(g)
    if res is None: continue
    ec_rect, leg_rect, sd_idx = res
    X0, Y0, X1, Y1, dx, dy = ec_rect
    if sd_idx < 0 or sd_idx >= len(strings): continue
    s = strings[sd_idx]
    import re
    m = re.search(r'(\d{8})', s)
    if not m: continue
    sprite_id = int(m.group(1))
    h = hash_name(f"build/worldart/{sprite_id:08d}.dds")
    if h not in tx.by_hash: continue
    blob = tx.read(tx.by_hash[h])
    img_tile = load_dds(blob)
    if img_tile is None: continue
    srcW = X1 - X0 + 1; srcH = Y1 - Y0 + 1
    if srcW <= 0 or srcH <= 0: continue
    # Scale HD content + dx/dy by 22/32 = 0.6875
    SCALE = 22.0 / 32.0
    cell_half = 22; zscale = 4
    px = cx + (x - y) * cell_half
    py = cy + (x + y) * cell_half
    if srcW % 2 == 1: px -= 1
    px -= cell_half
    py += (5 - z) * zscale
    crop = img_tile.crop((X0, Y0, X1+1, Y1+1))
    nw = max(1, int(round(srcW * SCALE)))
    nh = max(1, int(round(srcH * SCALE)))
    crop_s = crop.resize((nw, nh), Image.LANCZOS)
    py -= nh
    py += int(round(dy * SCALE))
    px += int(round(dx * SCALE))
    img2.paste(crop_s, (px, py), crop_s)
    from PIL import ImageDraw
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([px, py, px+nw-1, py+nh-1], outline=(255,0,0,255), width=1)

bbox2 = img2.getbbox()
img2_c = img2.crop(bbox2) if bbox2 else img2
img2_c.save(out_dir / "telescope_composite_cc.png")
print(f"Saved CC-scale {out_dir / 'telescope_composite_cc.png'} ({img2_c.size})")
mc.close(); ta.close(); tx.close(); sd.close()
