# `tileart.uop` record format — verified

Source spec: the project owner's wiki at
[`Tileart.creole`](wiki_assumptions/Tileart.creole) and
[`Texture.creole`](wiki_assumptions/Texture.creole) (the latter expands the
opaque `call TEXTURES()` referenced in the Tileart spec).

The Tileart wiki was treated as a hypothesis and cross-checked against real
records pulled from the current EC build. The Texture wiki (SUB_9_7 = "this
function tells informations about a texture" + full byte layout) closed the
loop: each tile's actual sprite reference is encoded as a `StringDictionary`
offset, not as a direct id, and the engine resolves it through the
`string_dictionary.uop` blob.

## Header (offsets 0x00 – 0x7D)

Empirical observations are from cross-correlating 22,615 EC tileart
records against CC `tiledata.mul` (see `tools/ec_research/scripts/73_…`
through `76_…`). "Unknown" entries that have new info from these scripts
are annotated.

| Offset | Type     | Field                       | Verified | Empirical observation                                  |
|-------:|----------|-----------------------------|:--------:|--------------------------------------------------------|
| 0x00   | u16      | Version                     | ✅       | `0x0004` in current build (wiki said `0x0003`)         |
| 0x02   | u32      | StringDictionary offset (name) | ✅    | Points into `string_dictionary.uop`; resolves to the tile's display name |
| 0x06   | u32      | TileID                      | ✅       | Matches the id we used in the hash lookup              |
| 0x0A   | u8       | Unknown bool                | ✅       | 0 or 1 (≈59% zero / 41% one across statics)            |
| 0x0B   | u8       | Padding                     | ✅       | Always 0 — alignment before f32 at 0x0C                |
| 0x0C   | f32      | Float (mostly 1.0)          | ✅       | 1.0 in 37923/40208 tiles; few have 1.05/1.25/0.4 — per-tile scale? |
| 0x10   | f32      | Float (mostly 1.5)          | ✅       | 1.5 in 39023 tiles; 1.0 in 1155; few outliers          |
| 0x14   | u32      | Fixed zero                  | ✅       |                                                        |
| 0x18   | u32      | **OldId / pre-EC tile id**  | ✅       | `0x00FFFFFF` = "no remap" (21196 tiles); otherwise real CC tile id of the pre-renumber sprite |
| 0x1C   | u32      | Unknown (statics: always 0) | ✅       | **0 for every paired static** (22,819); the "few hundred non-zero" are land/other tiles, not statics |
| 0x20   | u32      | **BodyType**                | ✅       | Named `BodyType` in the C# parser ([TileArt.cs:175](../../src/ClassicUO.Assets/TileArt.cs#L175)). Near-constant: `400` (human) in 22,717 statics, `666` (gargoyle) in 102 — a default owner/animation body id |
| 0x24   | u8       | Unknown                     | ✅       | Two values: 0x80 (land) or 0 (statics). On statics it is ~always 0 |
| 0x25   | f32      | **Render scale**            | ✅       | 1.0 default; `2.0` in ~530 statics, with rare `1.25/1.5/1.6/3.5`. Per-tile HD draw scale (`0x24` is its land-side companion) |
| 0x29   | u32      | Always 0                    | ✅       |                                                        |
| 0x2D   | f32      | **Lights[0]**               | ✅       | `Lights[0]` in C# parser ([TileArt.cs:179](../../src/ClassicUO.Assets/TileArt.cs#L179)). Range -5.0..2.0; non-zero in ~1000 tiles (light-source params) |
| 0x31   | f32      | **Lights[1]**               | ✅       | `Lights[1]`. Range -11.5..0; non-zero in ~1200 tiles   |
| 0x35   | u32      | Unknown                     | ✅       | 85 unique u32 values across statics — real per-tile data |
| 0x39   | u64      | **Flags (EC)**              | ✅       | **CC `TileFlag`, identical bit layout** — verified bit-for-bit against CC `tiledata.mul` (phi = 1.00 for ~20 bits; see [Flag mapping](#flag-mapping-ec-vs-cc)). The EC bit names come from the client's own flag table (`UOSA.exe FUN_00c11880`). |
| 0x41   | u64      | **Flags (legacy)**          | ✅       | Bit-perfect mirror of `0x39`; the legacy-side copy. |
| 0x49   | u32      | **Facing** (geometry class) | ✅       | Named `facing` in the C# parser ([TileArt.cs:184](../../src/ClassicUO.Assets/TileArt.cs#L184)). Statics: `1` (35,691 — normal/floor), `2` (432 — **walls**: 98% CC Wall, 92% Impassable), `3` (2,926 — impassable objects), `0` (150). Value 2 cleanly isolates vertical wall geometry. |
| 0x4D   | i32 × 6  | **EcSpriteLayout** (placeholder) | ⚠️  | `(x0, y0, x1, y1, anchorX, anchorY)` *in spec* but values are placeholder-filled for almost every static — see [discussion](#6-int-blocks-at-0x4d-and-0x65--not-what-they-appear) |
| 0x65   | i32 × 6  | **LegacySpriteLayout** (placeholder) | ⚠️ | Same caveat. ~70% of tiles have `(0, 0, 45, 46, 0, 0)` — that's a default, not real data |

### Flag mapping (EC vs CC) — RESOLVED ✅ (EC flags == CC TileFlag)

**The EC tileart `0x39` flags are CC's `TileFlag`, same bit layout, same
per-tile values.** Proven two ways:

1. **EC's own flag-name table** in the binary (`UOSA.exe`, `FUN_00c11880`,
   global `DAT_00e394e8`) — an array of `{name, mask}` pairs that *is* the CC
   `TileFlag` bit assignment (`0x1` background, `0x10` wall, `0x40` impassable,
   `0x80` wet, `0x200` surface, `0x40000` partialhue, …). See [EC flag enum](#ec-flag-enum).
2. **Bit-for-bit phi-correlation** vs CC `tiledata.mul` over **39,203 paired
   statics**, paired correctly (`EC tileart tid == CC item_id`):

| bit | name | setEC% | setCC% | phi | bit | name | setEC% | setCC% | phi |
|----:|------|------:|------:|----:|----:|------|------:|------:|----:|
| 0 | background | 20.4 | 20.4 | **1.00** | 13 | noshoot | 12.1 | 12.1 | **1.00** |
| 1 | weapon | 3.0 | 3.0 | **1.00** | 16 | mongen | 0.2 | 0.2 | **1.00** |
| 4 | wall | 8.5 | 8.4 | **1.00** | 17 | foliage | 6.8 | 6.8 | **1.00** |
| 6 | impassable | 36.0 | 36.0 | **1.00** | 18 | partialhue | 33.9 | 33.8 | **1.00** |
| 7 | wet | 1.0 | 1.2 | 0.92 | 21 | container | 1.4 | 1.4 | **1.00** |
| 9 | surface | 21.0 | 21.0 | **1.00** | 22 | wearable | 3.2 | 3.2 | **1.00** |
| 10 | bridge | 1.5 | 1.5 | **1.00** | 23 | lightsource | 3.4 | 3.4 | 0.99 |
| 11 | generic | 2.3 | 2.3 | **1.00** | 24 | animation | 8.1 | 9.4 | 0.91 |
| 12 | window | 0.8 | 0.8 | **1.00** | 27/28/29/30/31 | armor/…/stairs | — | — | **1.00** |

The only non-matching bits — `transparent` (2), `translucent` (3), `damaging`
(5), `article_a/an` (14/15), `usenewart` (19), `art_used` (26) — are flags EC
simply **leaves unset** in tileart (setEC% ≈ 0 while setCC% > 0). They're CC
metadata bits EC doesn't replicate here; everything spatial/gameplay matches CC
exactly. So **`0x39` can be fed straight into a CC `TileFlag` consumer.**

> ⚠️ **Pairing gotcha:** `scripts/73_tileart_vs_tiledata.py` pairs by
> `item_id = art_id − 0x4000`. That is **wrong** — the EC tileart record's
> `TileID` (offset `0x06`) **is the CC item_id directly** (no `0x4000` art
> offset). The bad pairing makes the flags look uncorrelated (an earlier draft
> of this doc wrongly concluded "EC flags are independent of CC" because of it).
> Pair by `tid == item_id`. Reproduce: [`scripts/flag_corr.py`](../scripts/flag_corr.py).

#### EC flag enum <a name="ec-flag-enum"></a>

Authoritative bit→name map from `FUN_00c11880` (bits 0–31 == CC `TileFlag`;
bits 32+ are **EC-specific render flags with no CC equivalent**):

| bit | name | bit | name | bit | name (EC-only) | set% |
|----:|------|----:|------|----:|------|-----:|
| 0 | background | 16 | mongen | 32 | nohouse | — |
| 1 | weapon | 17 | foliage | 33 | nodraw | 0.3 |
| 2 | transparent | 18 | partialhue | 34 | *(unnamed)* | 4.1 |
| 3 | translucent | 19 | usenewart | 35 | alphablend | 1.2 |
| 4 | wall | 20 | *(unnamed)* | 36 | noshadow | 0.1 |
| 5 | damaging | 21 | container | 37 | **pixelbleed** | **28.4** |
| 6 | impassable | 22 | wearable | 39 | playAnimOnce | 0.1 |
| 7 | wet | 23 | lightsource | 40 | multiMovable | 0.0 |
| 8 | ignored | 24 | animation | | | |
| 9 | surface | 25 | hover_over | | | |
| 10 | bridge | 26 | art_used | | | |
| 11 | generic | 27 | armor | | | |
| 12 | window | 28 | *(unnamed)* | | | |
| 13 | noshoot | 29 | *(unnamed)* | | | |
| 14 | article_a | 30 | stair_back | | | |
| 15 | article_an | 31 | stair_right | | | |

(`article_the`/`article` are aliases for bits 14|15 combined = `0xC000`.) The
notable EC-specific bit is **`pixelbleed` (bit 37, 28 % of statics)** — a
texture-edge bleed/sampling hint for the HD renderer; `alphablend` (35) and the
unnamed bit 34 (4 %) are the next most common.

## Sub-sections after the header

Wiki labels in parentheses match the original `Tileart.creole` for cross-reference.

| Section                       | Layout                                                       | Notes                                                                                 |
|-------------------------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------|
| **PropertiesEc** (SUB_9)      | `u8 count` + `count × { u8 prop, u32 value }`                | EC-side properties. **VERIFIED vs CC tiledata** (see [PropID table](#taepropid-verified)): `Weight`(0) matches CC weight **99.8 %**, `Height`(3) **99.7 %**, `Slot`(6) = CC layer **99.4 %**. |
| **PropertiesLegacy** (SUB_9_2)| same                                                         | Legacy-side copy (same `TAEPropID` ids; values diverge from EC only where CC/EC differ) |
| **MoneyItems** (SUB_9_3)      | `u32 count` + `count × { u32 amount, u32 id }`               | For currency stacks (gold, silver, …): which sprite to show at each amount threshold  |
| **AppearanceFilter** (SUB_9_4)| `u32 count` + variable per-entry                             | Animation appearance filter (race/gender/equipment branches)                          |
| **SittingData** (SUB_9_5)     | `u8 count` + (if non-zero) 4 × u32                           | Mount/chair sit-anchor offsets                                                        |
| **RadarColor** (SUB_9_6)      | 4 × u8                                                       | Minimap RGBA                                                                          |
| **TextureRefs** (SUB_9_7)     | four `TEXTURE()` blocks — `WorldArt`, `TileArtLegacy`, `TileArtEnhanced`, `Textures` | The actual sprite pointers — see [TextureRefs section](#textureRefs-the-texture-block) |
| **Effects** (SUB_9_8)         | `u8 effect_count` + variable per-effect                      | Visual effects (sparks, splash, animation overlays); *opcodes 0/1/2/7/10/11/12/15/16/17 each have their own body layout — not yet decoded*. Stored as `EffectsTail` in C#. |

### TAEPropID — the property ids <a name="taepropid-verified"></a>

`TAEPropID` (one byte per property, from [TileArt.cs:139](../../src/ClassicUO.Assets/TileArt.cs#L139)).
The three with a CC equivalent are **verified exact** (39,203 paired statics,
PropertiesEc vs CC `tiledata.mul`):

| id | name | freq (EC records) | CC equivalent | match |
|---:|------|------------------:|---------------|------:|
| 0 | Weight | 34,050 | `tiledata` weight | **99.8 %** |
| 1 | Quality | 2,044 | — | — |
| 2 | Quantity | 966 | — | — |
| 3 | Height | 29,785 | `tiledata` height | **99.7 %** |
| 4 | Value | 2,283 | — | — |
| 5 | AcVc | 1,040 | — | — |
| 6 | Slot | 1,265 | `tiledata` layer | **99.4 %** |
| 7 | Off_C8 | 32 | — | — |
| 8 | Appearance | 1,315 | — | — |
| 9 | Race / 10 Gender / 11 Paperdoll | rare | — | — |

So PropertiesEc is the EC-side mirror of CC item metadata; Weight/Height/Slot
can be read straight from it. Reproduce with the parser at offset `0x7D`
(`u8 count` then `count × {u8 id, u32 val}`).

### TextureRefs — the `TEXTURE()` block <a name="textureRefs-the-texture-block"></a>

A tileart record contains **four** of these blocks, one per namespace
(WorldArt / TileArtLegacy / TileArtEnhanced / Textures). Layout per block:

```
BYTE  enabled                     ← 0 = group empty, 1 = group has entries
if (enabled != 0):
    BYTE  unknown
    DWORD shader                  ← shader pointer (semantics opaque)
    BYTE  refCount
    refCount × {                  ← 17 bytes per texture reference
        DWORD sdIndex             ← StringDictionary 0-based INDEX (not byte offset!)
        BYTE
        FLOAT tileRepetition      ← 1.0 normally; >1 for tiling textures
        DWORD
        DWORD
    }
    DWORD secondaryCount;  secondaryCount × DWORD
    DWORD tertiaryCount;   tertiaryCount × DWORD
```

**Verified 2026-05-31 against UOReader's `StringDictionary.GetStringAtPosition`
and `stringDictionaryData.LoadUOP`**: the `sdIndex` field is the **0-based
index** into the parsed string list, not a byte offset into the blob.
Distinct tiles that *appeared* to share a string under a byte-offset
interpretation actually point at different list entries that happen to
contain similar text (e.g. tile 519 → index 1552 = `00000519_Plaster_Wall.tga`;
tile 521 → index 1552 too, since 521 reuses 519's HD master). The dictionary
header is 14 bytes (`i64 + u32 StringCount + i16`), followed by
`StringCount` Pascal-style entries (`u16 length` + ASCII).

## Resolution chain for 2D static placement (verified in-game)

**Important:** SUB_9_7's string-dictionary refs are **NOT** what EC's
static-art renderer uses. They feed the 3D model's surface textures, not
the 2D sprite that lives on the world tile. We discovered this after
chasing why CC tile 200 was rendering as "Jungle_Walls" sprite 467 instead
of the expected "Mage_Stone_Walls" sprite 200 — the SUB_9_7 chain pointed
to 467, but the actual in-game (and CC-equivalent) sprite is keyed
**directly by tile_id** in `LegacyTexture.uop` / `Texture.uop`.

### Direct lookup (the right one for 2D placement)

```
art_id
  └─► item_id = art_id - 0x4000   (statics; land uses art_id as-is)
        ├─► hash "build/worldart/{item_id:D8}.dds"   → Texture.uop (HD)
        └─► hash "build/tileartlegacy/{item_id:D8}.dds" → LegacyTexture.uop
```

Confirmed via Ghidra (`FUN_0051a840` — EC's HD tileart loader builds an
asset name `"{tile_id:08d}_TileArt"` and fetches the DDS by formatted
tile_id, not via SUB_9_7).

### Canvas convention (the key insight for placement)

EC's DDS canvas is **bigger** than CC's TGA canvas (e.g. 64×128 vs 44×89),
but the artwork sits at the **exact same pixel offset** within the canvas.

| Tile | CC canvas | CC alpha bbox | EC legacy canvas | EC legacy alpha bbox |
|-----:|-----------|---------------|------------------|----------------------|
| 2    | 44×89     | (20, 1, 24, 72) | 64×128          | (20, 1, 24, 72) ✓ same |
| 3    | 44×68     | (22, 1, 20, 67) | 64×128          | (22, 1, 20, 67) ✓ same |

So the two canvases share the same `(0,0)` origin — EC just extended the
canvas to the right/down to hold more pixel detail. To draw EC at the
correct world position, we use **CC's canvas dimensions** in the standard
`(W/2 - 22, H - 44)` anchor math and draw the whole EC DDS canvas at that
position. The visible content lands exactly where CC put it.

### 6-int blocks at 0x4D and 0x65 — partial-truth, still confusing

The wiki labels these `EcSpriteLayout`/`LegacySpriteLayout` ("bounds +
anchor"). Ghidra (`FUN_0051af20`, the legacy-art resolver) does read
LegacyImage and compute W=X1-X0, H=Y1-Y0:

```c
// vtable call fills X0,Y0,X1,Y1 from the tileart record's LegacyImage
*param_5 = uVar7;          // OUT width  = X1 - X0
*param_4 = DAT_00c9d1a0;   // OUT scale  = 1.0  (native)
*param_6 = uVar8;          // OUT height = Y1 - Y0

// fit-to-cell when oversized
if (cell_w < width || cell_h < height) {
    scale = min(cell_w / width, cell_h / height);
    width  = round(width  * scale);
    height = round(height * scale);
}
```

So `LegacyImage` is the **authoritative crop rect** inside the 64×64
legacy DDS, and the resolver scales the asset down to fit a 44×44 cell
when either dimension is larger. The early dismissal happened because:
- ~70 % of tiles ship `(0, 0, 44, 44, 0, 0)` (the unscaled "fill the
  cell" default) — those tiles have the artwork tucked into the top-left
  44×44 of their canvas, so drawing the whole canvas LOOKED right.
- Wall/statue tiles whose content sits *outside* a 44×44 box (e.g.
  tile 200 with content 32×108) reveal the breakage immediately: their
  `LegacyImage` is still default-`44×44`, the artwork extends below,
  and the visible alpha-bbox in the canvas is the truth — those tiles
  have legitimately stale `LegacyImage` and our render either crops them
  wrong or relies on alpha-trim instead.

| tile  | LegacyImage  | result                                            |
|------:|--------------|---------------------------------------------------|
| 1409  | (0,0,44,44)  | native, src=(0,0,44,44) within 64×64 DDS           |
| 1410  | (0,0,44,35)  | native, src=(0,0,44,35) — shorter, bottom-aligned  |
| 1411  | (0,0,46,54)  | scale = 44/54 ≈ 0.815 → 37×44 displayed             |
| 1414  | (0,0,48,63)  | scale = 44/63 ≈ 0.698 → 33×44 displayed             |

**Tried-and-reverted**: implementing the rect as a source-crop within
the 64×64 DDS (`src = (X0,Y0,W,H)` + fit-to-44 scale) produced no
visible improvement for roof tiles 1410/1411/1414 in-game. Either the
rect encodes display dimensions / hit-test (not where to crop in the
DDS), or the renderer combines it with another field we haven't
located. Reverted; legacy path stays on full-canvas src for now.

### EcImage at 0x4D — still TBD

For HD tiles, the EcImage rect (`(0,0,0,0)` for ~70 % of statics,
populated for the rest) is **NOT in HD-canvas pixels** — using it as a
raw source crop on populated HD tiles broke every one of them. The
coord system is still TBD (likely CC-pixel space or sub-piece coords),
so the HD path falls back to alpha-trim while we investigate.

## C# implementation map (updated)

- [`src/ClassicUO.Assets/EcArtLoader.cs`](../../src/ClassicUO.Assets/EcArtLoader.cs)
  - `TryGetDdsByArtId(artId)` — fetches the **color** DDS bytes by
    formatted tile_id (`build/tileartlegacy/{item_id:08}.dds`).
  - `TryGetMaskByArtId(artId)` — fetches the **hue mask** DDS bytes
    (`build/tileartlegacy/{1_000_000 + item_id:08}.dds`), or returns
    false when the sprite ships no mask.
- [`src/ClassicUO.Renderer/Arts/EcArt.cs`](../../src/ClassicUO.Renderer/Arts/EcArt.cs)
  - Decodes the color DDS → `Texture2D` and caches per-tile.
  - When a mask DDS is present, CPU-decodes both DXT5 buffers via
    `DecodeDxt5Rgba`, applies `ApplyHueMaskFromDds`, and replaces the
    texture with a fresh uncompressed (`SurfaceFormat.Color`) one.
- Render sites use **CC art's canvas dimensions** for the anchor math:
  - [`Game/GameObjects/Views/View.cs`](../../src/ClassicUO.Client/Game/GameObjects/Views/View.cs) (`DrawStatic`, `DrawStaticAnimated`)
  - [`Game/Map/ChunkMesh.cs`](../../src/ClassicUO.Client/Game/Map/ChunkMesh.cs) (`TryAddStaticLike`)
- Hue handling: EC draws pass the **same hueVec as the CC path** (with
  `IsPartialHue` honoured) — the mask preprocessing in `EcArt` makes
  the CC shader's strict `R==G==B` test produce per-pixel decisions
  that mirror EC's `lerp(color, hue, mask.a)`. See the
  [Partial-hue masks](#partial-hue-masks-per-sprite-in-legacytextureuop)
  section below.
- Shadows: EC draws use the **CC texture/UV** for `DrawShadow`, because
  EC's canvas has lots of transparent padding that would render as an
  oversized shadow blob.
- [`EcStringDictionary`](../../src/ClassicUO.Assets/EcStringDictionary.cs)
  and [`EcTileArtLoader`](../../src/ClassicUO.Assets/EcTileArtLoader.cs)
  still load and parse the SUB_9_7 records — they're used for tile
  *metadata* (flags, properties) but not for sprite resolution.

## What SUB_9_7 is actually for

The string-dictionary refs in SUB_9_7 point to the **3D model surface
textures**. EC's 3D renderer (which is disabled in the legacy 2D world
view we're targeting) reads SUB_9_7 to find the materials applied to each
face of the tile's 3D mesh. That's why a stone wall's tileart record
references "Jungle_Walls sprite 467" — that sprite is the texture mapped
onto the model's polygons, not the sprite shown on the 2D map.

## HD path (`Texture.uop` / `build/worldart/*.dds`)

HD has its own loader (`FUN_0051a840`) and uses a different rect convention
than legacy. Findings from Ghidra (`FUN_00459390` asset constructor) +
direct binary inspection:

### Crop rect

The asset's source crop comes from `EcImage` (tileart 0x4D):

```
srcX = X0
srcY = Y0
srcW = (X1 - X0) + 1   // FUN_00459390: in_EAX[2] += 1
srcH = (Y1 - Y0) + 1   // FUN_00459390: in_EAX[3] += 1
```

The +1 converts inclusive bounds to exclusive (matches Ghidra exactly).

When `EcImage` is empty (`X1 == Y1 == 0`), EC falls back to a hard-coded
`(0, 0, 44, 44)` rect:

```c
cVar3 = (**(code **)(*param_2 + 0x1c))();
if (cVar3 == '\0') {
    in_EAX[2] = 0x2c;  // X1 = 44
    in_EAX[3] = 0x2c;  // Y1 = 44
}
```

But that 44-pixel default is **for UI / icon rendering** (rendered through
the same loader path with a different scale source). For 2D world
placement of statics it produces a tiny ~29 CC-px sprite, so our code
intentionally **falls through to legacy when EcImage isn't populated**.

### Anchor offset (signed canvas padding) ✅ VERIFIED via UOReader

`EcImage` ints 4 and 5 carry `(PixelsXOffset, PixelsYOffset)` — signed
**canvas padding** around the sprite content, chosen by sign:

| Field    | Sign     | Effect                                          |
|----------|----------|-------------------------------------------------|
| `dx > 0` | positive | margin on the **left**, sprite shifts right    |
| `dx < 0` | negative | margin on the **right**, sprite stays at x = 0 |
| `dy > 0` | positive | margin on the **top**, sprite shifts down      |
| `dy < 0` | negative | margin on the **bottom**, sprite stays at y = 0 |

UOReader's render code (verbatim, from `TileartControlNew.cs` decompile):

```csharp
canvas.Width  = sprite.Width  + abs(dx);
canvas.Height = sprite.Height + abs(dy);
canvas.DrawImage(sprite, max(dx, 0), max(dy, 0));
```

The full draw-time canvas is then `(spriteW + |dx|, spriteH + |dy|)`,
with the world cell anchored at the canvas's bottom-center (same as CC).
This is what gives walls and statues their off-center placement
without any per-class anchor hacks — the dx/dy directly encode where
the sprite sits relative to the world cell.

**Note on UOReader's right-pane text:** the annotations
`wTot = w + dx` / `hTot = h + dy` use **signed** addition for human-
readability (e.g. ankh shows `hTot = 81` for `dy = -24`); the actual
drawing code uses `abs(dy)` so the real canvas height is 129. The
descriptive text and the rendering code use different formulas — trust
the rendering code.

**Examples** (verified per-record):

| Tile | EcImage `(x0,y0,x1,y1,dx,dy)` | Canvas | Content at | Effect |
|------|--------------------------------|--------|------------|--------|
| 2 (ankh)        | `(0, 0, 42, 105, 25, -24)` | 67 × 129 | (25, 0)  | shifted right; anchor 24 px below sprite |
| 201 (stone wall)| `(0, 0, 51, 167, 18, 0)`   | 69 × 167 | (18, 0)  | shifted right; bottom-aligned         |
| 16640 (small wall) | `(0, 0, 23, 35, 21, -20)` | 44 × 55 | (21, 0)  | shifted right; anchor below          |
| 22137 (marble wall)| `(7, 0, 58, 16, 6, -26)` | 57 × 42  | (6, 0)   | shifted right; anchor far below      |

The implication for CUO: the current `UsesCcAnchor` fallback (alpha-
trimmed HD bbox aligned to CC content's bottom-right) can be retired
once dx/dy padding is applied — the EC anchor is fully described by
these two signed ints.

### dx/dy in the binary: Ghidra trace ✅ VERIFIED

UOReader's preview-window rendering uses dx/dy as canvas-padding, but
that's *its* convention. We traced the actual engine usage end-to-end:

1. **`FUN_00459390`** (asset-rect reader) populates a sprite-descriptor
   struct from the tileart record. Both branches (EcImage-populated
   and legacy fallback) read all 6 ints from the rect into `in_EAX[0..5]`:
   ```
   in_EAX[0..3] = X0, Y0, X1, Y1
   in_EAX[4]    = dx              ← byte offset +0x10 in the struct
   in_EAX[5]    = dy              ← byte offset +0x14
   ```
   EcImage branch adds `+1` to X1/Y1 (inclusive→exclusive). Legacy
   branch multiplies X1/Y1 by `1.5` (CC-pixel → HD-pixel).

2. **`FUN_0051a840`** (extracts to floats for callers) reads those exact
   offsets:
   ```c
   *param_5 = *(float *)((int)local_a8 + 0x10);  // dx
   *param_6 = *(float *)((int)local_a8 + 0x14);  // dy
   ```

3. **`FUN_004e4380`** consumes them and passes them by name as **"topleft"**
   to a draw helper:
   ```c
   uVar4 = FUN_004d9b80(&DAT_00ca14d0, "topleft", (float)param_6, (float)param_7);
   ```

So dx/dy ARE live engine data — used as top-left screen-space offsets
when rendering sprites. The four callers of `FUN_0051a840` (`0057e920`,
`0057bfe0`, `004e4380`, `0051c240`) all hit UI/gump paths (strings:
`iconName`, `iconScale`, `objectType`, `topleft`). World statics use
the descriptor through different consumers (`005960f0`, `00445e70`).

### UOReader EC multi formula (verified pixel-exact, 2026-06-05)

Cross-checked CUO against the EC reference render of the telescope
multi (#207, tiles 5209-5274) via the offline composite at
[`tools/ec_research/out/telescope_composite_cc.png`](../out/telescope_composite_cc.png).

UOReader's draw helper (`MultiItem.cs` → `private void a(...)` line 352)
is the same for CC and EC, just with different cell pitches:

| target | cellHalf | zStep |
|---|---|---|
| CC | 22 | 4 |
| EC (HD) | 32 | 6 |

Position formula (HD pitch):
```
x = centerX + (xOff - yOff) * cellHalf
y = centerY + (xOff + yOff) * cellHalf
if (srcW odd) x -= 1                 ← parity
x -= cellHalf                        ← shift to cell LEFT (not center)
y += (5 - zOff) * zStep              ← elevation
y -= srcH                            ← top-anchor (texture grows up from baseline)
x += dx                              ← horizontal padding
y += dy                              ← vertical padding
draw(texture, x, y, srcRect=(X0, Y0, srcW=X1-X0+1, srcH=Y1-Y0+1))
```

Key facts that took digging to surface:
- **`X1`/`Y1` are INCLUSIVE** — `srcW = X1 - X0 + 1`, `srcH = Y1 - Y0 + 1`.
  UOReader's own `num3 = A_9 - A_7` (omitting the `+1`) is a 1-px bug
  in UOReader's preview, not the engine. CUO must use `+1`.
- **Anchor is bottom-LEFT on the cell grid**, not bottom-center. The
  `x -= cellHalf` shifts an empty (or atlas-cropped) sprite to the cell's
  left edge, then `dx` shifts further. For multi atlas pieces whose
  `srcW` is several cells wide, bottom-center math drifts by a full
  cell; cell-left math is exact.
- **`dx`/`dy` apply at HD pitch**. To render at CC scale, multiply by
  `22/32`. `LegacyImage.ldx`/`ldy` are the CC-pixel equivalents the
  engine pre-computed for the legacy path; for negative `dx` they
  match `round(dx * 22/32)` exactly.

**CUO routing (`EcArt.cs`)**: use cell-left anchor only when
`EcImage.X0 > 0 || EcImage.Y0 > 0` (atlas-packed multi piece sharing a
master with siblings). Standalone tiles where the master holds just
this tile's content (`X0=Y0=0`, walls/statues like 513/515/521) keep
CC-bbox alignment — the cell-left formula drifts them 1-2 px below
their CC neighbours because the HD canvas dimensions don't quite
match the CC bbox positions.

### Practical CUO port: where to apply dx/dy

After empirical testing across multiple commits, the answer turns out
to be path-dependent:

#### Legacy/UopEC path → SKIP dx/dy, draw full DDS at CC anchor

The "working" approach (commit `5e0475334`) for `tileartlegacy` DDS is:
- Source = the **full POT-padded DDS** (e.g. 64×128 for a 44×113 wall)
- Anchor math uses the **CC art's** canvas dimensions
  (`artInfo.UV.Width/Height`), not the EC DDS dims:
  ```csharp
  ax = (artInfo.UV.Width  >> 1) - 22;
  ay =  artInfo.UV.Height       - 44;
  src = new Rectangle(0, 0, ecArt.Texture.Width, ecArt.Texture.Height);
  ```
- DDS content sits at top-left; transparent POT padding is invisible;
  CC anchor places the content exactly where CC would place its own art.
- **No LegacyImage crop, no dx/dy adjustment.**

Applying UOReader's `canvas + |d|, draw at max(d,0)` math here breaks
tiles whose content layout already matches CC (most of them) because
CC's anchor formula implicitly accounts for the standard CC tile
positioning that EC's DDS files preserve.

#### KR/UopKR HD path → APPLY dx/dy with HD_TO_CC scale

For HD master textures (Texture.uop / `build/worldart/`) cropped via
`EcImage`:
- Source = the EcImage sub-rect `(X0, Y0)..(X1+1, Y1+1)` of the master
- **Scale** = `HD_TO_CC = 1/1.5 = 0.667` (NOT fit-to-44 — see below)
- Anchor math:
  ```csharp
  int dispW = (int)(Source.Width  * Scale.X);
  int dispH = (int)(Source.Height * Scale.Y);
  ax = (dispW >> 1) - 22 - shiftX;     // ← shiftX from dx
  ay =  dispH       - 44 - shiftY;     // ← shiftY from dy
  ```
- Where `shiftX = max(dx, 0) - |dx|/2`, `shiftY = max(dy, 0) - |dy|`
  (collapses UOReader's canvas+abs+draw-at math into a single offset
  from bottom-center anchor).

The fit-to-44 scale we originally pulled from Ghidra (`FUN_0051a840`)
turned out to be UI/icon path code. For world rendering we use the
HD_TO_CC ratio from `DAT_00c853b4 = 1.5` — i.e. one HD pixel maps
to two-thirds of a CC pixel. Without this, tiles like stone wall
(EcImage 51×167 = ~75 CC pixels worth) get crushed to 34×111.

#### EcImage-unpopulated tiles → fall through to legacy

When a tile lacks an EcImage rect in KR mode, we cannot anchor the HD
master without guessing, so we **fall back to the legacy DDS path**
(EC tileartlegacy DDS with CC anchor). Previously we tried an alpha-
trim + CC-bbox alignment hack — that's been retired now that dx/dy
explains the off-center cases for HD tiles that DO have EcImage.

### Render scale

Read from the EC binary at `DAT_00c9d1a0`:

```
DAT_00c9d1a0 = 1.0    // returned to Lua as the draw scale
```

So the EcImage rect's width/height are **already in target screen
pixels** — no rescaling needed at draw time.

For comparison, the legacy-with-scale branch uses
`DAT_00c853b4 = 1.5` to multiply LegacyImage X1/Y1, converting
CC-coord values to HD-pixel source coords. That branch isn't used for
ordinary statics either.

### Multi-texture composition (SUB_9_7 texture groups)

Each tileart record has four texture groups (`WorldArt`, `TileArtLegacy`,
`TileArtEnhanced`, `Textures`) and each group can be empty OR contain
**multiple textures** plus a **pixel shader ID**:

```
group:
  u8 val               (0 = empty group; non-zero = has shader+textures)
  u8 ?
  u32 ShaderId         (the pixel shader to use for this composite)
  u8 Count
  Count × { u32 sd_off, u8, f32 TextureRepetition, u32, u32 }   (17 B per tex)
  u32 c2; c2 × u32     (per-tex transform indices?)
  u32 c3; c3 × u32     (per-tex hue/colour indices?)
```

**Shader-ID distribution** across all 16,294 populated records:

| Group | Shader | Tex count | Tiles | Notes |
|-------|--------|-----------|-------|-------|
| WorldArt (KR HD) | `0x0001` | 2 | 9,175 | **standard `main + noise`** |
| WorldArt | `0x0001` | 1 | 2,878 | single texture |
| WorldArt | `0x0001` | 3 | 294   | adds a third overlay |
| WorldArt | `0x0BDF` | 4 | 299   | **custom 4-input composite** |
| WorldArt | `0x0BDF` | 3 | 30    | |
| WorldArt | `0x36C7` | 4 | 190   | **custom 4-input composite** |
| WorldArt | `0x36C7` | 3 | 132   | |
| WorldArt | `0x28500000` | 8 | 2 | outlier — 8-input mega-composite |
| TileArtLegacy / TileArtEnhanced / Textures | `0x0001` only | 1–3 | all | always default shader |

`Shader = 0x0001` corresponds to **`UOSpriteShader`** (per the Ghidra
string-table dump). Custom shaders `0x0BDF` and `0x36C7` are
specialised composites used by ~3% of tiles (mostly carpets, multi-
pattern rugs, decorated floors). The two `0x28500000` outlier tiles
are presumably high-fidelity hero pieces.

### `UOSpriteShader` is D3D9 Fixed-Function ✅ VERIFIED via Ghidra

`FUN_00593860` (the `UOSpriteShader` constructor) sets the object's
vftable to **`UOSpriteShaderFFP::vftable`** — "FFP" = **Fixed-Function
Pipeline**. The constructor binds **two textures** at struct offsets
`puVar2[0x3a]` (stage 0) and `puVar2[0x3b]` (stage 1):

```c
puVar2[0x3a] = first_texture;   // main tile sprite
puVar2[0x3b] = second_texture;  // built-in noise (sd_off = 3)
```

No custom HLSL is required to reproduce this — it's D3D9 multi-stage
texture blending using fixed-function ops (`MODULATE` of the two
stages, likely with stage 1 sampled at `uv × TextureRepetition`).

**Implication for the CUO port**: the standard 75% composite can be
reproduced via a 2-stage multiply: `output = sample(main, uv) ×
sample(noise, uv × 16)`. Either:
- A trivial CUO custom pixel shader that does `tex2D(s0, uv0) *
  tex2D(s1, uv1)` with `uv1 = uv0 × TextureRepetition`, OR
- Bake the composite at texture-upload time (multiply pixels once,
  then draw as a normal sprite — no shader needed, costs CPU at
  load but free at render).

The CPU-bake approach is much simpler for a first implementation
and fits CUO's existing static-texture caching model. The downside
is that the `TextureRepetition` factor is fixed at bake time, so
edits would require recaching.

Custom shaders `0x0BDF` and `0x36C7` (the carpet variants) are
presumably real HLSL — `Shaders.uop` would hold their compiled
effect bytecode. That's a separate research item.

### The magic `sd_off = 3` noise reference

The standard `0x0001` composite always pairs the per-tile texture
with a second texture at **`sd_off = 3, TextureRepetition = 16`**.
`sd_off = 3` falls **inside the dictionary's 16-byte header region** —
i.e. there's no actual string there. It's almost certainly a **magic
constant** the EC engine recognises and substitutes with a hard-coded
**built-in noise / pattern texture** that tiles 16× across the cell
for visual variation. Without it, EC carpets and floors would render
as flat, uniform fields.

### Composition examples (tiles 2749, 2750, 2768 — all carpets)

| Tile | Shader | Texture references                      |
|------|--------|------------------------------------------|
| 2750 | `0x0001` | `[main_carpet, noise(rep=16)]`         |
| 2768 | `0x0001` | `[main_carpet, noise(rep=16)]`         |
| 2749 | `0x0BDF` | 4 textures — pattern A, base color (rep=4), pattern A again, decoration overlay |

Tile 2749's variant pattern shows the custom shader provides a more
elaborate composite (e.g. multi-layered weave) than the standard
single-noise overlay.

### CUO implementation status

The current C# port (`EcTileArtLoader.cs::ParseTextureGroup`):
- **Reads** the shader ID but **discards it** (all groups → flat
  `List<EcSpriteRef>`).
- **Consumes** only the FIRST texture reference per group when
  rendering. The noise overlay and any subsequent textures are
  parsed but never applied at draw time.

**Fidelity gap**: standard-shader tiles render with no noise variation
(uniform texture instead of EC's variegated look). Custom-shader tiles
render the wrong layer entirely (whichever is at index 0).

**Why this isn't catastrophic** in our current state: the FlagsEc bit-34
iso-rotation bypass already routes surface tiles (which is what most
multi-texture tiles are — carpets, floors, roofs) to CC's pre-projected
art, which has its own colour variation baked in. Walls and statues
that stay on the EC HD path use shader `0x0001` with 2 textures, so
they lose only the noise overlay — a subtle aesthetic loss.

**Path to full fidelity** (future work):
1. Implement standard `0x0001` 2-texture composite as a custom pixel
   shader (multiply main × noise(uv*rep)). Covers ~9,175 tiles.
2. Reverse-engineer shaders `0x0BDF` and `0x36C7` from Ghidra. Covers
   ~650 tiles.
3. Implement the magic-noise texture (sd_off = 3) — either reverse-
   engineer EC's built-in or supply our own equivalent.
4. The chunked-mesh terrain renderer (the other future-work item) is
   the natural place to host all this — EC uses the same multi-stage
   sampler pipeline for terrain and surface statics.

### Constants (read directly from `UOSA.exe`)

| Symbol          | VA          | Value     | Meaning                                |
|-----------------|-------------|----------:|----------------------------------------|
| `DAT_00c9d1a0`  | 0x00c9d1a0  | `1.0f`    | Default scale returned by HD loader    |
| `DAT_00c853b4`  | 0x00c853b4  | `1.5f`    | Legacy-branch X1/Y1 multiplier         |
| `DAT_00d0a324`  | 0x00d0a324  | `0.6667f` | `= 1/1.5` (inverse, used elsewhere)    |
| `DAT_00d0a0dc`  | 0x00d0a0dc  | `2^32`    | int↔uint negative-value conversion     |

Tool: [`tools/ec_research/scripts/81_read_constants.py`](../scripts/81_read_constants.py)
parses PE headers and reads `.rdata` at those VAs.

### Per-tile coverage

- ~8,788 static `item_id`s have an HD DDS in `Texture.uop`.
- Only ~970 of those have a populated `EcImage` rect (well-defined HD
  source crop). The other ~7,820 have `EcImage = (0,0,0,0,0,0)`.
- For us: ~970 tiles use HD; the rest fall back to legacy.

### Per-tile world offset

The `offX, offY` (EcImage[4..5]) values are sparse — most tiles have
`(0, 0)`. Non-zero cases include:

| Tile (art_id) | EcImage                       | Notes                       |
|--------------:|-------------------------------|-----------------------------|
| 16640         | `(0, 0, 23, 35, 21, -20)`     | small wall, lifted up & right |
| 22137         | `(7, 0, 58, 16, 6, -26)`      | wide marble wall, lifted up |
| 16432         | `(0, 0, 65, 95, 0, 0)`        | no offset, just bounds       |

### EcImage is NOT a CC-equivalent crop — it's a per-piece slice

The fundamental difference between CC and EC for static placement:

- **CC**: one tile_id contains the WHOLE multi-cell object as a single
  sprite (e.g. tile 3806 is a complete pillar in one 43×85 TGA).
- **EC**: the SAME multi-cell object is split across multiple
  consecutive tile_ids, each carrying just ONE piece. The HD canvas
  per tile shows the whole figure for reference, but `EcImage` only
  marks the rect of THAT tile's piece (e.g. tile 3806's `EcImage` =
  `(0, 0, 65, 38)` — only the pillar's cap ornament, even though the
  HD canvas is 64×256 with the entire pillar visible inside it).

So for a CC-compatible renderer, **don't use `EcImage` as the crop**.
Use the **alpha-trimmed visible bbox of the HD canvas** instead —
that gives you the full figure the CC tile represents. Then anchor
its **bottom-right** at CC content's bottom-right (computed via
`Arts.GetRealArtBounds(idx)`).

Pseudo-code:

```
ccBox = Arts.GetRealArtBounds(graphic)         // visible bbox in CC canvas
ccCanvasTL = (baseX - (CC_W/2 - 22), baseY - (CC_H - 44))
ccContentBR.X = ccCanvasTL.X + ccBox.X + ccBox.Width
ccContentBR.Y = ccCanvasTL.Y + ccBox.Y + ccBox.Height

hdBbox = alpha_trim(HD_canvas)                 // via CPU DXT5 decode
dispW = hdBbox.W / 1.5                         // 1/1.5 = EC HD → CC pixels
dispH = hdBbox.H / 1.5
draw(hdTexture, source=hdBbox,
     posX = ccContentBR.X - dispW,
     posY = ccContentBR.Y - dispH,
     scaleX=2/3, scaleY=2/3)
```

`Arts.GetRealArtBounds` is already cached in
[`src/ClassicUO.Renderer/Arts/Art.cs`](../../src/ClassicUO.Renderer/Arts/Art.cs)
line 89 (it computes the bbox at first art-load).

**CPU DXT5 decode for HD alpha-trim**: `Texture2D.GetData<Color>` on a
DXT5 surface returns raw compressed block bytes (not decoded pixels) in
FNA/MonoGame. We use the same `DecodeDxt5Rgba` helper that the partial-
hue mask preprocessing uses to decode HD on the CPU and compute the
visible bbox correctly.

### Open HD questions — TO FIX LATER

- **Tile-pair anomaly (5649 vs 5650)** — these two banner tiles have
  **identical tileart records** except for the `TileID` field
  (same flags = `0xC1`, same `EcImage = (0,0,0,0,0,0)`, same
  `LegacyImage = (0,0,44,44,0,0)`, same record length). The only real
  difference is that tile 5650 has no HD DDS in `Texture.uop` while
  5649 does. Result: 5650 falls back to legacy (correct), 5649 uses
  the HD path and ends up misplaced + uncolored. There is nothing
  "special" about the banner's record — the misplacement comes from
  the generic HD canvas / CC canvas anchor mismatch. A future fix
  needs per-tile HD bbox alignment OR explicit per-tile metadata we
  haven't decoded yet.

- **HD hue on pre-colored textures** — most HD tiles have color baked
  per-pixel (e.g. tile 5649 banner: pixels are `(R=57, G=56, B=74)` —
  already blue). CC's hue shader uses only `color.r` to index the hue
  table, which washes the natural color when there's no `R==G==B`
  match. With `SHADER_NONE` the texture shows AS-IS, but for tile 5649
  in CC it's tinted to a brighter blue via the legacy mask path. EC's
  shader_04 says when `HAS_HUEMASK_TEX == 0` it uses `colorout = hue`
  (full replace), but our get_rgb implementation doesn't produce the
  same brightening effect because of the single-channel indexing.
  Likely fix: extend the shader's no-mask hue path to use a different
  channel or a brightness measure, OR ensure HD tiles always have a
  mask shipped (artist-side).


- **Tiles where HD content isn't at canvas (0,0)** — fallback would be
  to alpha-trim the HD DDS (decoding DXT5 on CPU since
  `Texture2D.GetData` returns raw blocks) and offset the placement by
  the trimmed bbox position. Most tiles don't need this.
- **What does `vtable[0x5c](0x80000)` actually check?** That's the
  per-call gate that decides HD vs legacy in `FUN_00459390`. It might
  check a flag on the texture-loader (presence of HD DDS) or a bit on
  the tile flags — we haven't traced its body.
- **What does `vtable[0x1c]()` check?** Returns the bool that decides
  EcImage-vs-`(0,0,44,44)` default in the HD branch.
- **Lua draw math**: `RequestTileArt` returns `(x, y, scale, w, h)` to
  Lua; the actual `batcher.Draw` call lives in Lua scripts inside
  `Interface.uop` / `MainMisc.uop`. We haven't decoded those, but the
  EC LUA renderer is for UI elements (paperdoll, icons) — the world
  static render path is C++ and uses the same FUN_005bfd30 asset
  fetcher but a different draw site we haven't fully traced.

## Effects / other open items

- **Effects bodies** (the `Effects` section) — preserved as a trailing byte
  buffer in `EcTileArtData.EffectsTail`. Not needed for static placement.
- **`EnhancedTexture.uop`** — registered in the EC binary
  (`FUN_00a70e5a`) but not shipped in most builds. Not relevant for the
  direct-lookup path either way; we only use `Texture.uop` and
  `LegacyTexture.uop`.

## Partial-hue masks (per-sprite, in LegacyTexture.uop)

EC's `Shaders.uop` ships an HLSL shader (extracted via
`tools/ec_research/scripts` to `out/ec_shaders/shader_04.hlsl`) that does
**mask-based partial hueing**:

```hlsl
float4 mask = tex2D(HueMaskSampler, IN.texCoord0).aaaa;
colorout = lerp(colorout, hue, mask);
```

So the "is this pixel hueable?" decision is NOT a runtime grayscale test
(CC's approach) — it's a separately-painted alpha mask per sprite.

**Mask DDS naming**: same archive (`LegacyTexture.uop`), key
`build/tileartlegacy/{1_000_000 + item_id:08}.dds`. So item 5650's color
DDS is at `00005650.dds` and its hue mask at `01005650.dds`. The mask's
**alpha** channel encodes hueability (255 = hue, 0 = leave alone).

**How we use it in CC's shader without a second sampler**: we CPU-decode
both the color and mask DXT5 DDSes, then walk every pixel of the color
texture:

- mask.alpha > 0 → snap `R=G=B=avg(R,G,B)` (the existing CC shader's
  strict `R==G==B` partial-hue test now passes → pixel gets hued)
- mask.alpha == 0 AND pixel was exactly `R==G==B` (e.g. a white pattern
  detail) → nudge `R` by ±1 (the test now fails → pixel stays its
  original color, NOT tinted)

The result is a fresh uncompressed (`SurfaceFormat.Color`) Texture2D
that renders identically to EC's mask-lerp through CC's existing shader.

### Why we decode DXT5 ourselves

FNA's `Texture2D.GetData<Color>` on a DXT5 surface returns the **raw
compressed block bytes** reinterpreted as Color structs (not decoded
pixels). Writing those back to a `SurfaceFormat.Color` texture produces
a recognisable but completely wrong checkerboard. The DXT5 decoder lives
in [`EcArt.DecodeDxt5Rgba`](../../src/ClassicUO.Renderer/Arts/EcArt.cs).

## Lessons learned the hard way

1. The string-dictionary chain ("SUB_9_7 → sd_off → filename → archive")
   is real and correct, but it answers a different question than the one
   2D placement needs. Wiki labels can be technically right and
   pragmatically misleading at the same time.
2. Direct lookups in EC tend to use formatted asset names
   (`{id:08d}_TileArt`, `{id:08d}.dds`, `{1_000_000+id:08d}.dds` for
   masks). Whenever a wiki spec routes through indirection, double-check
   whether the renderer code path actually uses that indirection or
   shortcuts to the formatted name.
3. The `EcImage`/`LegacyImage` 6-int blocks are placeholder-filled for
   most static tiles. Don't trust them as crop rects or anchors without
   visual verification against the actual DDS content.
4. EC DDS canvases share their `(0,0)` origin with CC TGA canvases —
   they just extend further right/down. Use CC's canvas dimensions in
   the anchor math and draw the whole EC canvas.
5. EC ships its own HLSL shaders inside `Shaders.uop` — they're plain
   readable HLSL with `//#param` permutation directives. When the
   rendering looks wrong, **extract the actual EC shader** before
   guessing at the algorithm.
6. `FNA.Texture2D.GetData<Color>` on a compressed surface (DXT*)
   returns the raw block bytes, not decoded RGBA. To mutate a DDS
   sprite, CPU-decode it first and build a fresh `SurfaceFormat.Color`
   texture from the decompressed buffer.
7. **HD ≠ "high-res CC".** EC's HD path uses an explicit per-tile
   source rect (`EcImage`) and only populates that rect for ~10% of
   tiles. The default `(0, 0, 44, 44)` fallback isn't for world
   rendering — it's a UI path. Always check `EcImage.Width > 0`
   before fetching the HD DDS for world placement; fall back to
   legacy otherwise.
8. **Read constants from the EXE for ground truth.** Symbols like
   `DAT_00c9d1a0` in Ghidra are just addresses — load `UOSA.exe`,
   parse the PE headers to find `.rdata` file offset, read the 4
   bytes at that VA and interpret as float. We found scale=1.0 and
   the legacy multiplier=1.5 this way after weeks of guessing.
9. **Ghidra symbols are intent, not gospel.** When `FUN_00459390`
   does `in_EAX[2] += 1`, that's the inclusive→exclusive rect
   conversion. Knowing the binary's actual arithmetic beats any
   wiki spec — wiki labels (like "EcSpriteLayout = bounds") tell
   you what fields exist; the binary tells you what they mean.
