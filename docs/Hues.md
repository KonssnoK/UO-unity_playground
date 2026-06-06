# Hues.uop — EC hue ramp texture + per-hue swatches

The Enhanced-Client hue table. Feeds the `HueSampler` used by every sprite
pixel shader (`UOSprite.psh`, `UOSpriteUI.psh`) to recolour masked pixels of
mobiles, statics and gumps. Replaces CC's `hues.mul`.

## Container

MYP UOP (`magic 0x50594D`). 2,624,982 B, **3003 entries**. All entries are
zlib-compressed (`flag == 1`).

| entry | format | size | role |
|-------|--------|------|------|
| 0 | DDS, 32-bit RGBA (uncompressed, fourCC 0) | 64×64 | small/default texture (purpose TBD) |
| **1** | **DDS, 32-bit RGBA (uncompressed)** | **1024×1024** | **the hue-ramp texture = `HueSampler`** |
| 2 … 3002 | BMP, 32-bit BGRA | 256×2 | per-hue solid swatch (base / radar colour), one per hue (~3001 ≈ 3000 hues) |

DDS pixel format for entries 0/1: `RGBBitCount=32`, `R=0x00FF0000 G=0x0000FF00
B=0x000000FF A=0xFF000000` → stored **BGRA** in file bytes (offset 128 = pixel
data, no mips).

## entry1 — the hue-ramp texture (HueSampler)

1024×1024 RGBA. Layout (verified by sampling):

- **y axis = hue index** (one ramp per row).
- **x axis = intensity step** (0 → 1023, dark → bright). A masked sprite pixel's
  luminance/red selects the column.
- Sampling `HueSampler(x = pixel intensity, y = hue index)` returns the final
  recoloured RGBA. Unused cells are transparent `(0,0,0,0)`.

Sample rows (cols 0,16,32,64,128 → RGB):
```
row   2: (0,0,48) (0,0,56) (0,0,64) (0,0,80)  (0,0,120)   blue ramp
row  32: (48,0,8) (56,0,8) (64,0,8) (80,0,16) (120,0,24)  red ramp
row1001: (24,24,24)(32,32,32)(40,40,40)(64,64,64)(112,112,112) greyscale ramp
row1002: (0,0,8) (8,8,16) (24,16,24)(56,40,48)(112,88,88)  skin/brown ramp
```
So each row is a dark→light gradient *in that hue*. The shader therefore does
`out.rgb = HueSampler(pixel.intensity, hue).rgb` for masked pixels (an intensity
remap into the hue ramp), gated by `HueMaskSampler`.

> NOTE: the texture is 1024 rows but UO has ~3000 hue ids. Whether row == hue id
> directly (covering 0..1023) with higher ids handled elsewhere, or the hue id
> is remapped/scaled into 0..1023, is **not yet confirmed** — needs a check
> against a known hue (e.g. skin 1002 / a dye) vs the row that produces it.

## entries 2..3002 — per-hue swatches

Each is a 256×2 32-bit BGRA BMP filled with a **single solid colour** = that
hue's representative/base colour (radar/preview). Examples:

```
entry   2: BGRA (8,0,0)     → RGB (0,0,8)      near-black
entry   3: BGRA (184,0,0)   → RGB (0,0,184)    blue
entry   4: BGRA (232,0,0)   → RGB (0,0,232)    bright blue
entry1004: BGRA (144,160,208)→ RGB (208,160,144) tan / skin
```
(Index→hue-id mapping likewise TBD; entry2 is presumably hue 0 or 1.)

## How it applies to animations & statics

Same path for both (mask-based partial hue):

1. Sprite texture from `SpriteSampler` (AMOU frame / static DDS).
2. `HueMaskSampler` marks hueable pixels:
   - **animations:** the AMOU palette 4th-byte flag (see `AnimationFrame_AMOU.md`)
   - **statics:** the per-sprite mask DDS (`HAS_HUEMASK_TEX`, see static art path)
3. For masked pixels: `colour = HueSampler(pixel.intensity, mobileOrItemHue)`.
   Unmasked pixels pass through (fixed neutral / pre-coloured detail).

To replicate EC colours exactly in ClassicUO we'd build a CUO hue lookup from
`Hues.uop` entry1 (or reuse CC `hues.mul` if ramps are close enough) and apply
it to the flag/mask pixels by the mobile hue — instead of CC's `R==G==B`
partial-hue test, which targets the wrong pixels.

---

## VERIFIED — EC hues == CC hues.mul

Matched EC `Hues.uop` against classic `hues.mul`:

- **Per-hue swatch mapping is direct: `entry[2 + N]` = UO hue `N`.** The swatch's
  solid colour equals that hue's **bright-end ramp value** (CC `hues.mul` hue N,
  ramp index ~30):

  | hue N | EC swatch (entry 2+N) RGB | CC hue N ramp[30] | Δ² |
  |------:|---------------------------|-------------------|----|
  | 0     | (0,0,8)                   | (0,0,8)           | 0  |
  | 1     | (0,0,184)                 | (0,0,180)         | 16 |
  | 2     | (0,0,232)                 | (0,0,230)         | 4  |
  | 33    | (232,48,88)               | (230,49,90)       | 9  |
  | 64    | (152,240,96)              | (148,238,98)      | 24 |
  | 128   | (224,56,144)              | (222,57,148)      | 21 |
  | 1002  | (208,160,144)             | (205,156,139)     | 50 |  ← skin
  | 2999  | (0,0,8)                   | (0,0,8)           | 0  |

  Overall-nearest-hue search returns N for each swatch → **the EC hue set is the
  same as CC `hues.mul`** (same ids, same colours). ClassicUO already has them.

- **The 1024×1024 ramp texture (entry1) is NOT hue-id-ordered** (row 128 is
  cyan while hue 128 is magenta; row 1002 is skin like hue 1002 but the curve is
  brighter/whiter than CC). Its row ordering / exact role is still unresolved —
  but it does not matter for ClassicUO because the hue colours equal CC's.

### Consequence for ClassicUO colouring
We do **not** need to import `Hues.uop`. To colour EC sprites (anim or static)
correctly we can reuse CUO's existing CC hue ramps, applied to the **masked**
pixels (AMOU palette flag=1 / static mask DDS) by the mobile/item hue — i.e.
mask-based partial hue instead of CC's `R==G==B` test.

Caveat at **hue 0**: CC and EC use *different base art* (CC art is greyscale,
AMOU is pre-coloured), so a hue-0 mobile cannot be made pixel-identical to
classic — `SHADER_NONE` (baked AMOU colour) is the right default there. Hued
mobiles/items (non-zero hue) ramp the same in both and will match.
