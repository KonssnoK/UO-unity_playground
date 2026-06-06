"""For tile_ids 1 and 2, dump:
  - CC art (the legacy artLegacyMUL .tga)
  - EC legacy DDS (LegacyTexture.uop/build/tileartlegacy/{item_id:08}.dds)
  - EC HD DDS  (Texture.uop/build/worldart/{item_id:08}.dds)
each with a red rectangle drawn at the LegacyImage / EcImage crop rect read
from the tileart record. Saves PNGs side-by-side so we can eyeball how the
offsets map to the visible content."""
from __future__ import annotations
import struct, sys, io
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
CC = Path(r"C:\Games\Electronic Arts\Ultima Online Classic")
OUT = HERE.parent / "out" / "offsets_viz"
OUT.mkdir(parents=True, exist_ok=True)

TILE_IDS = [2, 3]   # CC item ids

# Open archives once
tileart = UopArchive(EC / "tileart.uop")
lg      = UopArchive(EC / "LegacyTexture.uop")
hd      = UopArchive(EC / "Texture.uop")
ccart   = UopArchive(CC / "artLegacyMUL.uop")


def decode_cc_art(buf: bytes) -> Image.Image | None:
    """Decode classic .tga (run-length 16bpp). Returns RGBA PIL image."""
    if len(buf) < 12:
        return None
    w = struct.unpack_from("<H", buf, 4)[0]
    h = struct.unpack_from("<H", buf, 6)[0]
    line_offsets = struct.unpack_from(f"<{h}H", buf, 8)
    data_start = 8 + h * 2
    pixels = bytearray(w * h * 4)
    for y in range(h):
        if line_offsets[y] == 0 and y != 0:
            continue
        ptr = data_start + line_offsets[y] * 2
        x = 0
        while True:
            if ptr + 4 > len(buf):
                break
            xoffs = struct.unpack_from("<H", buf, ptr)[0]; ptr += 2
            run   = struct.unpack_from("<H", buf, ptr)[0]; ptr += 2
            if xoffs + run >= 2048 or xoffs + run == 0:
                break
            x += xoffs
            for _ in range(run):
                if ptr + 2 > len(buf):
                    break
                val = struct.unpack_from("<H", buf, ptr)[0]; ptr += 2
                if val:
                    r = ((val >> 10) & 0x1F) << 3
                    g = ((val >>  5) & 0x1F) << 3
                    b = ( val        & 0x1F) << 3
                    px = (y * w + x) * 4
                    pixels[px] = r; pixels[px+1] = g; pixels[px+2] = b; pixels[px+3] = 0xFF
                x += 1
    return Image.frombytes("RGBA", (w, h), bytes(pixels))


def with_rect(img: Image.Image, rect, color=(255, 0, 0, 255), label=None) -> Image.Image:
    """Return a copy of img with a 1-px rectangle drawn at rect=(x,y,w,h)."""
    out = img.copy().convert("RGBA")
    d = ImageDraw.Draw(out)
    x, y, w, h = rect
    d.rectangle([x, y, x + w - 1, y + h - 1], outline=color, width=1)
    if label:
        d.text((1, 1), label, fill=color)
    return out


def upscale(img: Image.Image, factor=4) -> Image.Image:
    """Nearest-neighbor upscale so the rectangle is visible at this size."""
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)


for tile_id in TILE_IDS:
    art_id = 0x4000 + tile_id
    print(f"\n=== tile {tile_id} (art_id {art_id}) ===")

    # 1. Read the tileart record and extract the two 6-int blocks
    rec_ent = tileart.by_hash.get(hash_name(f"build/tileart/{art_id:08}.bin"))
    if rec_ent is None:
        print(f"  no tileart record for art_id {art_id}")
        continue
    payload = tileart.read(rec_ent)
    ec_layout = struct.unpack_from("<6i", payload, 0x4D)
    lg_layout = struct.unpack_from("<6i", payload, 0x65)
    print(f"  EcImage     = {ec_layout}    (X0,Y0,X1,Y1, PixelsXOffset,PixelsYOffset)")
    print(f"  LegacyImage = {lg_layout}")
    ec_x0, ec_y0, ec_x1, ec_y1, ec_ax, ec_ay = ec_layout
    lg_x0, lg_y0, lg_x1, lg_y1, lg_ax, lg_ay = lg_layout

    # 2. CC art
    cc_buf = ccart.get_by_name(f"build/artlegacymul/{art_id:08}.tga")
    cc_img = decode_cc_art(cc_buf) if cc_buf else None
    if cc_img:
        # CC art has no record-supplied bounds; draw the natural bbox of the
        # opaque pixels for reference.
        bbox = cc_img.getbbox() or (0, 0, cc_img.width, cc_img.height)
        cc_with = with_rect(
            cc_img,
            (bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]),
            color=(0, 255, 0, 255),
            label=f"CC {cc_img.width}x{cc_img.height}",
        )
        upscale(cc_with).save(OUT / f"tile{tile_id:02}_cc.png")
        print(f"  CC art {cc_img.width}x{cc_img.height} visible {bbox} -> tile{tile_id:02}_cc.png")
    else:
        print(f"  no CC art")

    # 3. EC legacy DDS  (LegacyImage rect drawn in red)
    lg_ent = lg.by_hash.get(hash_name(f"build/tileartlegacy/{tile_id:08}.dds"))
    if lg_ent:
        dds = lg.read(lg_ent)
        try:
            ec_lg = Image.open(io.BytesIO(dds)).convert("RGBA")
            rect = (lg_x0, lg_y0, lg_x1 - lg_x0, lg_y1 - lg_y0)
            ec_lg_with = with_rect(
                ec_lg, rect, color=(255, 0, 0, 255),
                label=f"EC Legacy {ec_lg.width}x{ec_lg.height}  rect={rect}  anchor=({lg_ax},{lg_ay})",
            )
            upscale(ec_lg_with).save(OUT / f"tile{tile_id:02}_ec_legacy.png")
            print(f"  EC legacy {ec_lg.width}x{ec_lg.height} rect={rect} -> tile{tile_id:02}_ec_legacy.png")
        except Exception as e:
            print(f"  EC legacy decode failed: {e}")
    else:
        print(f"  no EC legacy DDS")

    # 4. EC HD DDS  (EcImage rect drawn in red)
    hd_ent = hd.by_hash.get(hash_name(f"build/worldart/{tile_id:08}.dds"))
    if hd_ent:
        dds = hd.read(hd_ent)
        try:
            ec_hd = Image.open(io.BytesIO(dds)).convert("RGBA")
            rect = (ec_x0, ec_y0, ec_x1 - ec_x0, ec_y1 - ec_y0)
            ec_hd_with = with_rect(
                ec_hd, rect, color=(255, 0, 0, 255),
                label=f"EC HD {ec_hd.width}x{ec_hd.height}  rect={rect}  anchor=({ec_ax},{ec_ay})",
            )
            upscale(ec_hd_with, factor=2).save(OUT / f"tile{tile_id:02}_ec_hd.png")
            print(f"  EC HD {ec_hd.width}x{ec_hd.height} rect={rect} -> tile{tile_id:02}_ec_hd.png")
        except Exception as e:
            print(f"  EC HD decode failed: {e}")
    else:
        print(f"  no EC HD DDS")

tileart.close(); lg.close(); hd.close(); ccart.close()
print(f"\nOutput dir: {OUT.resolve()}")
