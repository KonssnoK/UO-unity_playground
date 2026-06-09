# EC terrain renderer — implementation findings

Research output for porting the Enhanced Client (UOSA.exe) chunked-mesh terrain
renderer into ClassicUO. Sources: APItrace D3D9 capture
(`UOSA_lastframes.trace`), the 4096-vertex blob (`blob_call14840372.bin`), and
the Ghidra dump (`FUN_00461bc0` = `UOTerrainShader`/mesh builder, plus the
layer/resource functions). **Research only — no implementation.**

## TL;DR — the EC terrain recipe

Per 32×32-cell chunk, EC draws **one shared 4096-vertex mesh** (4 verts/cell)
**N times** (N = 6–10 = number of terrain layers present in that chunk), all
**fixed-function** (no pixel/vertex shader). Each draw lays one terrain layer:

- **Layer 0 = opaque base** (stage-3 alpha = vertex DIFFUSE = 1.0 → covers the
  whole chunk).
- **Layers 1..N-1 = alpha-tested overlays** (stage-3 alpha = a per-layer
  **coverage-mask texture**; `ALPHATESTENABLE=TRUE` discards uncovered pixels →
  the layer is "stamped" only where its mask passes). **This is the splat.**

Each layer's *colour* is `lerp(baseAlbedo, partnerAlbedo, blendMask.a)` (two
**`build/worldart` HD textures** world-tiled, blended by a red mask's alpha) then
**× the per-vertex colour (lighting)**. The splat weight is the stage-3 coverage
mask's alpha. **⚠ See [P1 CORRECTION] at the bottom: the albedo is `Texture.uop`
worldart, NOT `TerrainTexture.uop` atlases — the M3/P1 "atlas" text below is
superseded.**

---

## M2 (gating) — per-vertex `D3DCOLOR` is lighting, NOT a splat mask

**Answer: terrain is NOT blended via per-vertex alpha.** The N layer-draws of a
chunk all use the **same vertex buffer** (verified: draws 0–5 → VB `0x1eafd9e0`,
draws 6–15 → VB `0x1dfbb580`; run-lengths 6,10,7,10,…). A shared VB means the
per-vertex `D3DCOLOR` is **identical across a chunk's layers**, so it cannot be a
per-layer blend weight. The colours are 64 near-grey values (`0xffDADADA`
dominant, alpha `0xff`) — **per-vertex lighting** (the mesh builder computes
normals + dot-products into this colour; see M5/Ghidra). The splat weight is the
per-layer **coverage-mask texture** in stage 3 (below).

---

## M3 — the 4 texture-stage recipe (fixed function)

> **⚠ SUPERSEDED IN PART by [P1 CORRECTION] (bottom of doc).** The stage *ops*
> here are right, but the **texture identities are wrong**: t0/t2 are
> `build/worldart` albedo (a base/partner pair), **not** `TerrainTexture.uop`
> atlases; t1 is a worldart **red blend mask** (alpha only); and stage 3
> modulates by **vertex DIFFUSE (lighting)** with t3 supplying **alpha only**.
> The cumulative-state recipe is in the correction.

`SetPixelShader(NULL)` and `SetVertexShader(NULL)` for every terrain draw — pure
fixed-function multitexture. Per-draw state (from the trace, draw 0 onward):

| Stage | COLOROP | result | tex (count over frame) | role | texcoord | tex-matrix scale |
|------:|---------|--------|------------------------|------|----------|------------------|
| 0 | `SELECTARG1`(TEXTURE) → **TEMP** | TEMP=t0 | **11 distinct** | terrain-atlas **base** | 0 (world) | ×0.25 |
| 1 | `SELECTARG1`; **ALPHAOP SELECTARG1, ALPHAARG1=TEXTURE** | CURRENT.a = t1.a | **2 distinct** (global) | **detail/blend mask** (its alpha) | 0 (world) | ×0.03125 (1/32) |
| 2 | **`BLENDCURRENTALPHA`**, ARG1=TEXTURE | lerp(CURRENT, t2, CURRENT.a) | **11 distinct** | terrain-atlas **blend partner** | 0 (world) | ×0.1 |
| 3 | **`MODULATE`**, ARG1=TEXTURE; **ALPHAOP SELECTARG1** | CURRENT×t3 | **46 distinct** (per chunk×layer) | **coverage mask** (its alpha = splat) | **1 (chunk 0..1)** | — |

Stage-3 alpha source switches per layer (the key):
- **Layer 0:** `ALPHAARG1 = D3DTA_DIFFUSE` → final alpha = vertex alpha = 1.0 →
  opaque base.
- **Layers 1+:** `ALPHAARG1 = D3DTA_TEXTURE` → final alpha = **t3 coverage-mask
  alpha** → alpha-tested overlay.

Pass render state: `LIGHTING=FALSE`, `ALPHATESTENABLE=TRUE`, `ZWRITEENABLE=TRUE`,
`ZENABLE` on; `ALPHABLENDENABLE` is **off** during the terrain block (toggled
`FALSE` right after it). So overlays composite by **alpha-test stamping** over
the opaque base at equal Z (painter's order by draw sequence), not by
alpha-blend. (`ALPHAREF` seen at 0 and 10 for variants.)

### What the textures are
- **t0 / t2** — terrain-type **atlas slices** from `TerrainTexture.uop` (256²
  DXT). World-tiled (×0.25 and ×0.1 of world XZ → tiles every 4 and 10 cells).
  Only 11 distinct each over the frame = the 11 terrain types visible. Each
  layer blends two of them via t1.
- **t1** — a **global detail/blend mask** (only 2 distinct in the whole frame),
  tiled ×1/32 (once per chunk-ish); its **alpha** drives the `BLENDCURRENTALPHA`
  between t0 and t2 (adds intra-cell texture variation/transition).
- **t3** — the **per-chunk, per-layer coverage mask** (46 distinct = chunks ×
  overlay-layers), sampled at the **chunk-normalized UV** (0..1). Its **alpha is
  the splat weight**; `MODULATE` also tints the colour by it.

This is enough to reproduce in a pixel shader: `base = lerp(tex(atlasA, worldUV*0.25), tex(atlasB, worldUV*0.1), tex(detail, worldUV/32).a); out.rgb = base.rgb * tex(cover, chunkUV).rgb * vertexLight.rgb; out.a = (layer==0)? 1 : tex(cover, chunkUV).a;` then alpha-test.

---

## M1 — `TerrainDefinition.uop` record layout

Records are `build/terraindefinition/{N}.bin` (N = non-padded decimal index, 249
records, variable length). Serialized Gamebryo-style object: fixed header +
variable **layer list** + fixed footer.

```
// header
0x00  u32  rec_id        // INTERNAL id (119463..119858 mostly, 155 distinct, reused).
                         //   NOT the texMap. (see M7)
0x04  u32  index         // == the file index N (and == the texMap that addresses it). 249/249.
0x08  u32  (0)
0x0C  f32  global_param  // small {0,0.1,0.15,0.25,0.5,1.0,5.0} per-record scalar (blend/height?)
0x10..      serialized sub-preamble (alignment varies by record form @0x38 = 0/1/2 — don't
                         //   treat past ~0x10 as a flat struct)
// layer list  (marker `01 00`, then:)
 u32  base_rec_id
 u8   N                  // layer count
 N × { u32 layer_rec_id  // neighbour/blend-partner reference, in the INTERNAL rec_id space
                         //   (chained rec_id+1,+2,… for sequential terrain; cross-refs otherwise)
       f32 layer_param   // per-layer scalar {0.5,1,2,4,5,6,8,12,16,32} = blend weight / tiling scale
       u8  seq_index     // layer ordinal 0..N-1 (= texture-stage order)
       u8[7] pad(0) }
// footer (~44 B, constant)
 f32 (0.0) ; u32 0x04 ; 16×0 ; u32 0x04 ; 16 B (per-record fine floats e.g. -0.0075, else 0)
```

- **Length is N-driven:** common form `len = 154 + (N-3)*17` (exact over 92
  records). Two other record "forms" (`@0x38` = 0 or 2) prepend a small preamble
  but carry the **same layer-list grammar**.
- The **two `0x04` footer markers** = a fixed "4" tag, consistent with the
  **4 texture stages**.
- **Verified examples:** rec 0 (rec_id 0x1D2A7, idx 0) N=3 → layers
  {0x1D2A9 p=8, 0x1D2AA p=6, 0x1D2AB p=32}; rec 8 N=5; rec 10 N=4. `0x1D2AB`
  recurs across many records = a shared blend layer.

**Caveat / open:** the layer's *base atlas slice* is referenced by
`layer_rec_id` (internal id) — resolved one hop later (rec_id → an entry in
`TerrainTexture.uop`'s 38-atlas index, giving atlas# + sub-rect). The record does
**not** store a raw 0..37 atlas index. To follow the adjacency graph, build a
`rec_id (0x00) → record-index` map by scanning all 249 records. Whether
`layer_param` is blend-weight vs tiling-repeat is the main remaining ambiguity
(best pinned by reading the TerrainDefinition **deserializer**, reached via
`FUN_004cc3f0 → FUN_00a7222c`, not the render fn).

Ghidra: `FUN_00461bc0` is the **mesh builder** — loops `0x20×0x20` cells, scales
texcoords ×`0.03125`, builds a `TerrainTriShape` + `UOTerrainTexturingProperty`
with one entry per record layer; `FUN_00461790` is the layer-type factory
(`UODefaultTerrainLayer` / `UOWaterTerrainLayer` / `UOBumpMapTerrainLayer`).

---

## M8 — vertex declaration (32-byte, verified)

From the blob + the stage texcoord usage (the in-trace 24-byte decls are the
sprite variant; the terrain decl `0x1dfe93e0` was created before the captured
frames, but the layout is unambiguous):

```
offset 0   D3DDECLTYPE_FLOAT3    POSITION  idx0   // world (X, Yelev, Z)
offset 12  D3DDECLTYPE_D3DCOLOR  COLOR     idx0   // per-vertex lighting (ARGB, a=0xff)
offset 16  D3DDECLTYPE_FLOAT2    TEXCOORD  idx0   // WORLD UV = raw (worldX, worldZ)
offset 24  D3DDECLTYPE_FLOAT2    TEXCOORD  idx1   // CHUNK UV = 0..1 across the 32 cells (step 1/32)
// stride 32
```

Blob sample (cell 0,0 corners), confirming: POS `(1312.00, -0.198, -1472.01)`,
col `0xffDADADA`, uv0 `(1312, -1472)` (= world XZ), uv1 `(0, 0)`,`(0.03125,0)`,…

---

## M4 — UV formulas

- **uv0 (offset 16) = raw world (X, Z)** — i.e. `K = 1`, NOT divided. The
  per-stage **texture matrices** then scale it: stage0 ×0.25 (atlas tiles every 4
  world units), stage1 ×0.03125 (detail tiles every 32 = once/chunk), stage2 ×0.1
  (atlas-partner tiles every 10). All texture matrices are
  `diag(s, -s, 1)` 2×3 (note the **−s on V** → V flipped).
- **uv1 (offset 24) = chunk-normalized 0..1** (step `1/32` per cell). Used by
  **stage 3 only** (`TEXCOORDINDEX=1`) to sample the per-layer **coverage mask**
  once across the chunk — i.e. the splat weight is addressed in chunk space, so
  the mask is a 32×32-ish per-chunk texture.

---

## M5 — elevation (map Z → world Y) — PARTIAL

POS.Y is small and per-cell (range `-0.378 .. -0.127` in the blob; the 4 corners
of a cell are a planar bilinear patch, e.g. NW `-0.1975`, NE=SW `-0.1622`, SE
`-0.1268`, step ≈ `0.0353`). The mesh builder (`FUN_00461bc0`) computes X/Z as
`worldX = cellX (+1)`, `worldZ = -(cellY (+1))` (Z negated) and feeds per-cell
heights into Y; the only clean literal in the function is `0.03125` (texcoords).
The Z→Y scale is **not a literal** — it comes from the per-cell map height (and
possibly `global_param`/record floats). **To pin the constant:** correlate the
blob POS.Y at world `(1312, -1472)` against the actual EC map Z at that tile
(read the facet/map data), or read the height term in the mesh builder's vertex
assembly. The corner step `≈0.0353` is the candidate per-Z-unit scale (unconfirmed).

---

## M6 — `legacyterrainmap.csv` (inside `GameData.uop`)

`data/gamedata/legacyterrainmap.csv`, UTF-8, **4162 data rows**, 3 columns:

```
legacyId,newId,newSubType
1,0,1
3,1,0
9,20,0
...
```

- **legacyId** — classic land/tiledata graphic id (input key), 1..16379 sparse.
- **newId** — EC terrain-type id = the `terrainType` XML `id` (many legacy ids
  collapse onto one newId; e.g. 187 legacy ids → newId 0 fallback).
- **newSubType** — small **per-newId variant index** (0 → 3510 rows, 1 → 647,
  2 → 5). Disambiguates which rotation/edge/transition variant of that terrain to
  use when several legacy tiles share a newId.

---

## M7 — the join (CORRECTED) + typeFlags

**The hypothesised `texMap == rec_id` join is WRONG.** Verified on real data:

- `texMap` is the **record INDEX** → `build/terraindefinition/{texMap}.bin`
  (the record whose `0x04` field == texMap). The record's `0x00` `rec_id` is an
  unrelated internal id (119xxx); `texMap → rec_id` match rate = **0.0%**, but
  `texMap → record-at-index` = **249/249** exact.
- Full chain: **`legacyId →(csv)→ newId →(LegacyTerrain XML, id==newId)→ texMap
  →(index)→ TerrainDefinition[texMap]`**. Worked: newId 3 `grass` texMap 3 →
  TD[3]; newId 10 `furrows` texMap 10 → TD[10]; etc.
- The link is **intentionally sparse**: only **181/249** TD records are
  referenced; ~94% of the 4108 terrain types have **no** TD record (default
  behaviour).
- `LegacyTerrain.uop`: 4108 XML `<terrainType id name texMap><typeFlags>…`.

**typeFlags frequencies** (the renderer/gameplay flags):

| flag | count | | combination | count |
|---|---:|---|---|---:|
| impassable | 1235 | | (none) | 2569 |
| nohouse | 168 | | impassable | 1164 |
| surface | 153 | | nohouse | 168 |
| wet | 103 | | surface+wet | 73 |
| wall | 40 | | surface | 56 |
| mongen | 5 | | impassable+wall | 39 |
| no_diagonal | 2 | | impassable+surface+wet | 24 |

`wet` co-occurs almost only with `surface` (standable water). `impassable` is the
dominant blocker (often with `wall`).

---

## Open items for implementation
1. **M5 constant** — the exact map-Z→world-Y scale (correlate blob Y vs map Z, or
   read the mesh-builder height term).
2. ~~`layer_rec_id → (atlas#, sub-rect)` resolution~~ — **SOLVED**, see
   [P1 CORRECTION] Q3: it is `TextureInfo.textureIDX → string_dictionary →
   "{worldartId}_{Name}.tga"`, fully static. `layer_param` = `repetition` (tiling,
   scale `1/rep`). Build the lookup at runtime — see [P1 CORRECTION] Q3 "How to
   pull the textures at runtime".
3. **t1/t3 mask textures** — where the per-chunk coverage masks (t3) come from
   (generated from the cell terrain-type grid? a per-chunk render target?) — the
   46 distinct t3 textures are created outside the captured frames; capture
   `CreateTexture`/`UpdateTexture` for them in the full trace to confirm
   dimensions (expected ~32² A8) and source.

---

# Appendix — open items resolved (P1 gating, P2, P3)

## P1 (GATING) — layer → atlas + `layer_param` meaning

### `layer_param` = TILING denominator (NOT a blend weight) — confirmed
The per-stage texture-matrix scales captured in the trace are **exactly**
`1/{4,5,6,8,9,10,16,24,32,48}` (e.g. `0.25=1/4`, `0.10=1/10`, `0.03125=1/32`,
`0.0208=1/48`) — i.e. **the set of `layer_param` values**. So a layer's
texcoord scale = `1 / layer_param`: the atlas **repeats once every `layer_param`
world units** (cells). It is a **tiling/repeat scale**. (The most common tilings
are `1/4` and `1/16`.) The blend weighting is *not* here — it comes from the
mask textures (t1 alpha → `BLENDCURRENTALPHA`, t3 alpha → alpha-test; see M3).

### `texMap` = atlas id — ❌ WRONG, see [P1 CORRECTION]
> **Retracted.** The base ground texture is **not** `build/terraintexture/{texMap}.dds`.
> `TerrainTexture.uop` atlases are cream gradients and are **not used** in the
> terrain pass; the albedo is a `build/worldart` (`Texture.uop`) HD texture,
> resolved **statically** via `TerrainDefinition.TextureInfo → string_dictionary →
> "{worldartId}_{Name}.tga"` (see [P1 CORRECTION] Q3). The paragraph
> below is kept only for the archive facts (38 atlases, 256² DXT5).

`TerrainTexture.uop` = **38 atlases, ids `[1..17, 20..40]`, each 256² DXT5**.
A terrain's **base** texture is `build/terraintexture/{texMap:08}.dds`
**directly** (grass id 3 → atlas 3; furrows id 10 → atlas 10). **No sub-rect** —
the texture matrices are scale-only `diag(s, -s, 1)` (note V flipped) with
`WRAP` addressing, so the whole 256² atlas tiles. (texMap = newId = the XML
terrainType id; see M7 chain.)

### The layer list = the terrain's TEXTURE STACK
> **⚠ "atlas" identities below are SUPERSEDED by [P1 CORRECTION].** The stage
> *structure* (4 disjoint sets, base/partner/mask/coverage) is correct, but
> t0/t1/t2 are `build/worldart` textures, not `TerrainTexture.uop` atlases, and
> the "layer `rec_id`s" are actually `TextureInfo.textureIDX` string-dictionary
> indices (→ `"{worldartId}_{Name}.tga"`). Read the structure here, the
> identities + the static chain in the correction (Q3).

The trace shows **four disjoint texture sets** per chunk (0 overlap between
them): stage0 = **11 base atlases** (t0), stage2 = **11 *different* detail/
variation atlases** (t2), stage1 = **2 global detail masks** (t1, its alpha is
the BLENDCURRENTALPHA weight), stage3 = **46 per-chunk coverage masks** (t3).
So each terrain type draws as `lerp(baseAtlas, detailAtlas, detailMask.a)` then
coverage-masked. The `TerrainDefinition` record's **N-entry layer list is that
stack**, one entry per texture, each carrying its own `1/param` tiling and a
`seq_index` (= stage order). The **recurring shared `layer_rec_id` (e.g.
`0x1d2ab`, param 16)** across grass/grass2 is the **global detail mask** (t1,
only 2 distinct in the whole frame).

Worked examples (verified record bytes):
- **grass** texMap 3 → atlas 3; rec_id `0x1d3c9`, `base_rid 0x1d2a8`, **N=3**
  layers: `{0x1d3ca param5 seq0}`, `{0x1d3cb param5 seq1}`, `{0x1d2ab param16 seq2}`
  = base(1/5) + detail(1/5) + shared-mask(1/16).
- **grass2** texMap 4 → atlas 4; same `base_rid 0x1d2a8` (grass family),
  N=3 params 4/4/16, shared `0x1d2ab` mask.
- **furrows** texMap 10 → atlas 10; rec_id `0x38b5`, N=4, params 12/4/6/8.

### Still not fully pinned — `layer_rec_id → atlas` ✅ NOW SOLVED (see [P1 CORRECTION] Q3)
> **Solved & retracted.** The "`layer_rec_id`s in the 119xxx space" are
> `TextureInfo.textureIDX` **string-dictionary indices**, not resource-cache
> sub-resource ids. They resolve **statically**: `values[textureIDX]` =
> `"{worldartId:08x}_{Name}.tga"` in `string_dictionary.uop`. The worked examples
> below labelled these as "atlas N / params / seq" — corrected meanings:
> `{textureIDX, repetition, textureSlot}`, resolving to WorldArt files. The layer
> object type *is* chosen by the `shaderNameIDX` string (`FUN_00461790`:
> `UODefaultTerrainLayer` / `UOWaterTerrainLayer` / `UOBumpMapTerrainLayer`) — that
> part was right. The original (partly mislabelled) notes are kept below for the
> byte-structure record only.

The base resolves cleanly (`record.rec_id@0 → record.index@4 = texMap → atlas`).
The **other layer entries** reference textures by `layer_rec_id` in the internal
119xxx id space (usually `rec_id+1, +2`, plus the shared mask id). These are
**not** other TerrainDefinition records' rec_ids — they're sub-resource ids
resolved through the Gamebryo resource cache (`FUN_004cc3f0 → FUN_00a7222c`,
keyed by id; the layer object type is chosen by string in `FUN_00461790`:
`UODefaultTerrainLayer` / `UOWaterTerrainLayer` / `UOBumpMapTerrainLayer`).
The `base_rid` is shared across a terrain *family* (grass 3 & 4 both `0x1d2a8`),
i.e. there's material inheritance. **To bind the detail atlas + mask concretely**,
map the trace's t2/t1 texture pointers to their source DDS via the full-trace
`CreateTexture` order (the base atlas binding — `atlas[texMap]` — is enough to
start; the detail/mask are a refinement).

## P2 — t3 coverage masks: runtime-generated per-chunk splat masks

**Source (strong inference): generated at runtime from the per-cell terrain
grid, one mask per (chunk, overlay-layer).** Evidence: t3 has **46 distinct
textures** for just the few visible chunks (≈ chunks × overlay-layers), each
sampled at the **chunk-normalized UV (0..1)** — i.e. one tile across the 32×32
chunk. Per-chunk masks cannot be static authored assets (millions of chunks), so
they are built from the cell terrain-type grid: for each terrain layer present
in a chunk, a coverage mask whose alpha marks the cells of that terrain. Stage 3
takes that alpha as the overlay's coverage (layer 0 uses DIFFUSE=opaque instead;
overlays use `ALPHAARG1=TEXTURE`=t3.a, then alpha-test stamps it — see M3). Soft
edges come from t1 (the BLENDCURRENTALPHA detail mask) + bilinear filtering.

*Dimensions/format/generator function pending* a full-trace
`CreateTexture`/`LockRect` capture of a t3 address (e.g. `0x20bca720`) — the
mining over `UOSA.trace` (318 MB) was still streaming at write time. Expected
~32² (or 33²) `A8`/`A8L8`, CPU-locked-and-filled (not D3DX-loaded), point or
bilinear filtered (matters for edge feathering).

## P3 — map Z → world Y — mechanism found, scale still open

The render fn does **not** compute elevation: it assembles each vertex as
`POS = precomputed_corner + chunk_origin`, i.e. `Y = pfVar17[-4] + param_1[3]`
(`FUN_00461bc0` lines 176–178). The **map-Z→Y scale lives in the mesh
*precompute*** that fills `pfVar17` (the per-cell corner array, stride `0x180`),
**not** in the render function (whose only float literal is `0.03125` for
texcoords). From the blob the corner-to-corner Y step is a uniform **`≈0.0353`
per cell** (planar bilinear patch), the candidate per-Z-unit scale.

A facet-Z correlation was attempted: blob world `(1312, -1472)` → facet0 sector
`1303` (`= sx*64+sy`, matches the sector filename id), but those cells read
**z = 0 (flat)** while the blob's POS.Y still varies `−0.20 ± 0.13` — so either
the blob chunk is on a different facet/region, or POS.Y includes a projection/
bias term beyond raw elevation. **Open:** read the precompute function's height
term, or correlate the blob against the correct facet/region's per-cell z (the
facet sector z-bytes are decoded — see Facets.md — so this is a tractable
follow-up once the blob's facet is identified).

---

# P1 CORRECTION — the ground albedo is `Texture.uop` worldart, NOT `TerrainTexture.uop`

> **This section supersedes the earlier claims** "texMap = atlas id", "t0/t2 are
> `TerrainTexture.uop` atlas slices", and "t1 is a global detail mask from
> `TerrainTexture.uop`". Those were inferred from texture *format/count* without
> decoding the actual bound pixels. **Decoding the real pixels (apitrace
> `--blobs` + manual BC1/BC3 decode) and byte-matching them to the archives
> proves the terrain textures come from `Texture.uop` (`build/worldart`), and
> that `TerrainTexture.uop`'s 38 atlases are not used in the base terrain pass at
> all.** Method: extracted every `memcpy` fill blob in the texture-upload batch
> (calls 768979–770800 of `UOSA.trace`), BC-decoded them, and `==`-compared the
> raw DXT payloads against `TerrainTexture.uop`, `Texture.uop`. Verified.

## Q1 — all 38 `TerrainTexture.uop` atlases are detail/glow/mask, none are albedo
Dumped every atlas (ids `[1..17, 20..40]`, 256² DXT5) to PNG. **All 38 are faint
cream/tan radial gradients, glows, and soft brush blobs, mostly transparent
(opaque coverage ≈1–20 %; only ids 20/21/22 and 30/31 are fully opaque and those
are dark noise / flat yellow).** None is a recognisable grass/stone/sand ground
texture. **Byte-check:** none of the 38 atlas payloads equals *any* texture bound
in the terrain draws. So `TerrainTexture.uop` plays **no role in the base terrain
color** in the captured scene (it is likely a separate effect/transition/“classic
terrain” set). `atlas[texMap]` being a cream gradient is therefore expected — it
was never the albedo.

## Q2 (THE UNBLOCKER) — the ground color comes from `build/worldart` (`Texture.uop`)
The textures bound in the actual terrain `DrawIndexedPrimitive`s decode to
**recognisable grass/earth albedo** and **byte-exact-match `Texture.uop`
entries**. For the first terrain chunk (VB `0x1eafd9e0`, draw @ call 770855):

| stage | trace ptr | dims/fmt | decoded content | **source (`build/worldart/…`)** | role |
|------:|-----------|----------|-----------------|----------------------------------|------|
| 0 (t0)| `0x1d807ae0` | 256² DXT5 | green grass | **`02000011.dds`** | **base albedo** → TEMP |
| 1 (t1)| `0x1d476a80` | 256² DXT5 | **red mask** | **`01000003.dds`** | blend mask (its **alpha** = lerp weight) |
| 2 (t2)| `0x1d806620` | 512² DXT5 | green grass | **`02000010.dds`** | **partner albedo** (blended in) |
| 3 (t3)| `0x20bca720` | (mask) | coverage | runtime per-chunk | splat coverage (its **alpha**) |

> **If you implement one thing:** for this grass chunk the visible ground color =
> `lerp(worldart 0x02000011, worldart 0x02000010, worldart 0x01000003 .alpha)`.
> **All three live in `Texture.uop`, none in `TerrainTexture.uop`.**

Across the whole startup texture batch, **78 of the bound terrain textures
byte-matched `Texture.uop`** (0 matched `TerrainTexture.uop`). The worldart ids
used fall in three id bands:

- **`0x01xxxxxx`** — `_noise`/`_alpha`/`cube` **masks & cubemaps** (e.g. `01000003_noise_alpha`, `01000004_noise_alpha_sharp`, `01000013_water_alpha`, `01000014_cube0`, `01000017_cube3`); the blend mask's **alpha** is consumed at stage 1.
- **`0x02xxxxxx`** — terrain **albedo**, in **`_A`/`_B` pairs** per material (e.g. `02000010_Grass_C`/`02000011_Grass_B`, `02000070_Sand_A`/`02000071_Sand_B`): the **even** id (`_A`/`_C`) = 512² partner → stage 2; the **odd** id (`_B`) = 256² base → stage 0. The id is just the asset's own WorldArt id — **the 8-hex prefix of its `_Name.tga`** (see Q3); it is looked up by *name via the string dictionary*, not computed.
- **`0x03xxxxxx`** — additional WorldArt assets (some materials’ extra slot-4 overlays).

`worldart_id` is **not** `0x02000000 | legacyLandId` (tested: grass land `0x03–0x06`
and the CC sand land `0x0436` are all **absent**) — it is simply the WorldArt
asset id (filename prefix) that the `TerrainDefinition` record names through the
string dictionary. **Q3 below gives the exact, fully-static mapping + the complete
212-row table.**

## Q3 — terrain-type → worldart id is **FULLY STATIC** (string dictionary) ✅ SOLVED

> **This supersedes the earlier "runtime resource cache" guess in this section.**
> The mapping is 100 % recoverable from the `.uop` files — no client run needed.
> The `TerrainDefinition` record itself carries the texture references, as a
> `TextureInfo` block whose `textureIDX` is an **index into `string_dictionary.uop`**;
> the indexed string is the WorldArt filename, and **the worldart id is that
> filename's 8-hex-digit prefix**. Confirmed three ways: (a) it reproduces the
> exact textures the D3D trace bound for the grass chunk, (b) the shader-name
> field resolves to the three Ghidra layer classes, (c) the WorldArt path form
> matches the disassembly (`FUN_004604a0` builds `Data\WorldArt\…`; `FUN_004cb850`
> hard-codes `Data\WorldArt\01000045_noise.tga`).

**What I mis-parsed in M1/P1:** the `TerrainDefinition` "layer list" *is* the
`TextureInfo.texturesArray`. The fields I called `{layer_rec_id, layer_param,
seq_index}` are actually `{textureIDX (string-dict index), repetition (tiling),
textureSlot}`. They are **not** Gamebryo resource ids.

### The full resolution chain (for the coder)
```
facet cell  ──►  landtileGraphic (legacy land-tile id)            [facetN.uop, see Facets.md]
            ──►  legacyterrainmap.csv : legacyId → (newId, newSub) [GameData.uop / shipped csv]
            ──►  TerrainDefinition[newId]                          [TerrainDefinition.uop, record index = newId = "texMap"]
                   .shaderNameIDX  → stringDict → "UODefaultTerrainLayer" | "UOWaterTerrainLayer" | "UOBumpMapTerrainLayer"
                   .texturesArray[] each:
                       textureIDX  → stringDict → "{worldartId:08x}_{Name}.tga"   (worldart id = the 8-hex prefix)
                       repetition  → texture tiling (texcoord scale = 1 / repetition)
                       textureSlot → role (see slot map below)
            ──►  worldart id  → build/worldart/{id:08x}.dds        [Texture.uop]  ← the actual albedo/mask/cube DDS
```

### Binary formats (confirmed vs UOReader structs + raw bytes + Ghidra)
**`string_dictionary.uop`** (1 entry, `build/stringdictionary/string_dictionary.bin`):
```
u64 unk; u32 count; i16 unk;   then count × { u16 len; char[len] }   // values[] indexed sequentially
```
`textureIDX` / `shaderNameIDX` / `nameIDX` are **indices into `values[]`** (not byte offsets).

**`TerrainDefinition.uop`** record `build/terraindefinition/{N}.bin` (N = record index = texMap/newId):
```
u32 nameIDX;  u32 index(=N);  u32 _u3; u32 _u4; u32 _u5;
u32 aliasCount;  aliasCount × { u32 countIndex; u32 oldAlias; u64 flags }   // 16 B each
TextureInfo textures;                                                       // ← the texture stack
```
**`TextureInfo`** (same struct used by `tileart.uop`):
```
u8 texturePresent;  if 0 → end.
u8 unk;  i32 shaderNameIDX;  u8 texturesCount;
texturesCount × { u32 textureIDX; u8 unk; f32 repetition; i32 textureSlot; i32 unk }   // 17 B each
u32 count2; count2 × i32;   u32 count3; count3 × f32;     // usually 0
```

### Worked example — grass (matches the trace byte-for-byte)
`TerrainDefinition[1]` `name="grass"` `shader="UODefaultTerrainLayer"`:
| slot | textureIDX | string (WorldArt file) | worldart id | repetition | D3D stage it feeds |
|----:|-----------|------------------------|-------------|-----------:|--------------------|
| 0 | `0x1d3c8`* | `02000010_Grass_C.tga` | `0x02000010` (512²) | 10 | **stage 2** (partner, scale 1/10) |
| 1 | `0x1d3c9`* | `02000011_Grass_B.tga` | `0x02000011` (256²) |  4 | **stage 0** (base → TEMP, scale 1/4) |
| 2 | `0x1d2ab`  | `01000003_noise_alpha.tga` | `0x01000003` |  32 | **stage 1** (blend mask alpha, scale 1/32) |

The trace's grass chunk bound `t0=0x02000011`(1/4), `t2=0x02000010`(1/10),
`t1=0x01000003`(1/32) — identical. (*indices shown illustratively; read them from the record.)

### Slot → stage role (by shader class)
- **`UODefaultTerrainLayer`** (203/212): slot0 = `_A`/`_C` partner → **stage 2**; slot1 = `_B` base → **stage 0 (TEMP)**; slot2 = `noise_alpha` blend mask → **stage 1** (alpha = lerp weight). (Some records add slot4 = an extra detail/overlay.)
- **`UOWaterTerrainLayer`** (8/212, e.g. water/lava): slot0 = `*_alpha` mask, slot1 = diffuse (`water`/`Lava_A`), slot2 = `cube3` (reflection cubemap). Animated/scrolled.
- **`UOBumpMapTerrainLayer`** (1/212, snow): the default 3 **plus** slot3 = `water_alpha`, slot4 = `cube0` (normal/bump map).

### How to pull the textures at runtime (do this — no pre-generated table)
Everything is computed from shipped uops at load time. **No CSV, no client dump.**
There are **212** terrain records; e.g. sand = texMap 7 → `Sand_A` `0x02000070` +
`Sand_B` `0x02000071` + `noise_alpha`. `TerrainTexture.uop`'s 38 gradient atlases
are **not referenced by any record** — ignore them for terrain.

**Step 0 — load the string table once** (from `string_dictionary.uop`, single entry):
```
read: u64 _, u32 count, i16 _
values = []; repeat count times: { u16 len; values.add(ascii(read len bytes)) }
```

**Step 1 — build texMap → textures, once at startup** (from `TerrainDefinition.uop`,
record file `build/terraindefinition/{N}.bin`, where N = the record index = texMap):
```
parseTerrainDef(bytes b):
    u32 nameIDX; u32 index(=texMap); u32 _u3,_u4,_u5
    u32 aliasCount; skip aliasCount * 16 bytes          // alias = {u32,u32,u64}
    // ---- TextureInfo ----
    u8 present; if present==0: return (no textures)
    u8 _unk1; i32 shaderNameIDX; u8 texCount
    layers = []
    repeat texCount:
        u32 textureIDX; u8 _unk; f32 repetition; i32 slot; i32 _unk
        string file = values[textureIDX]                // e.g. "02000011_Grass_B.tga"
        uint worldartId = hexPrefix8(file)              // 0x02000011  (first 8 hex chars)
        layers.add({ worldartId, repetition, slot })
    shader = values[shaderNameIDX]                       // "UODefaultTerrainLayer" | "UOWaterTerrainLayer" | "UOBumpMapTerrainLayer"
    return { texMap=index, shader, layers }
```

**Step 2 — map a facet cell → texMap** (see M6/M7): `landtileGraphic` →
`legacyterrainmap.csv` (in `GameData.uop`) → `newId` = the record index used in Step 1.

**Step 3 — bind by slot/shader role** (see the slot map above + Q4 recipe). For
`UODefaultTerrainLayer`: base = slot1 (`_B`), partner = slot0 (`_A`/`_C`), mask =
slot2 (`noise_alpha`); texcoord scale = `1 / repetition`.

**Step 4 — fetch each pixel source** from `Texture.uop`:
`worldartId → build/worldart/{worldartId:08x}.dds` (DXT1/DXT5; DXT1 = opaque
albedo, DXT5 mask carries the alpha). Decode and sample per the Q4 composition.

> This is exactly what the EC client does (`FUN_00461790` dispatches on the
> `shaderName` string; `FUN_004604a0` opens `Data\WorldArt\{id}…`) and what the
> working Unity prototype does (`UOResourceManager.getTerrainDefinition` +
> `getStringDictValue` + `TextureInfo`). Re-derive the lookup at load — it stays
> correct across game patches, where a snapshot file would go stale.

## Q4 — corrected per-pixel composition (full fixed-function state)
The earlier M3 recipe was wrong because the **lastframes trace only shows
per-draw state *deltas***; the args that wire `TEMP` and `DIFFUSE` into the blend
are set **once at init** (before the trim) and were invisible. Reconstructing the
**cumulative** stage state from call 1 of the full `UOSA.trace` gives the real
config:

```
Stage0  COLOROP=SELECTARG1  COLORARG1=TEXTURE(t0)  RESULTARG=TEMP   ALPHAOP=DISABLE
Stage1  COLOROP=SELECTARG1  COLORARG1=CURRENT      (rgb passthrough)
        ALPHAOP=SELECTARG1  ALPHAARG1=TEXTURE(t1)                   → CURRENT.a = mask.a
Stage2  COLOROP=BLENDCURRENTALPHA  COLORARG1=TEXTURE(t2)  COLORARG2=TEMP(t0)
Stage3  COLOROP=MODULATE    COLORARG1=CURRENT      COLORARG2=DIFFUSE
        ALPHAOP=SELECTARG1  ALPHAARG1=TEXTURE(t3)   TEXCOORDINDEX=1 (chunk UV)
RS: LIGHTING=FALSE  COLORVERTEX=TRUE  ALPHATESTENABLE=TRUE (ref 0, GREATER)
    ALPHABLENDENABLE=TRUE  SRCBLEND=SRCALPHA  DESTBLEND=INVSRCALPHA  ZWRITE=TRUE
```

Resolving the register flow (`TEMP` is consumed by **stage 2 `COLORARG2`**, and
the vertex color enters at **stage 3 `COLORARG2=DIFFUSE`**):

```
TEMP        = tex(base256 , worldUV / p0).rgb           // worldart 0x02..(odd)  albedo, tiles every p0 cells
CURRENT.a   = tex(mask    , worldUV / p1).a             // worldart 0x01..       red mask alpha = blend weight
CURRENT.rgb = lerp( TEMP , tex(part512, worldUV/p2).rgb , CURRENT.a )   // blend base↔partner albedo
out.rgb     = CURRENT.rgb * vertexColor.rgb             // × per-vertex lighting (DIFFUSE)
out.a       = (layer==0) ? 1.0 : tex(coverage, chunkUV).a               // splat coverage
```

then **alpha-blend** (`SRCALPHA/INVSRCALPHA`) with alpha-test discarding only
`a==0`. Tilings observed for the grass chunk: `p0≈4` (base), `p1≈32` (mask),
`p2≈10` (partner) — these are the `1/layer_param` scales from P1.

> **Note for the coder:** `mask`, `base256`, `part512` above are exactly the
> `TerrainDefinition[texMap]` `TextureInfo` slots resolved through the string
> dictionary (Q3): `base` = slot1 `_B`, `partner` = slot0 `_A`/`_C`, `mask` =
> slot2 `noise_alpha`; `p0/p1/p2` = each entry's `repetition`. Read them at load
> from `TerrainDefinition.uop` + `string_dictionary.uop` (Q3 "How to pull the
> textures at runtime") — no trace, no CSV needed.

**Net corrections to earlier sections:**
- **t0/t2 are worldart albedo (a base/partner pair), not `TerrainTexture` atlases.**
- **t1 is a worldart `noise_alpha` blend-mask; only its alpha is used (lerp weight), not a “detail color”.**
- **Stage 3 modulates by the per-vertex DIFFUSE color (lighting); the stage-3 texture (t3) contributes alpha only (coverage), not color.** (M2’s "vertex color = lighting" is confirmed — and it is what tints the final pixel.)
- **`TerrainTexture.uop` is not the terrain albedo source; `Texture.uop`/`build/worldart` is.**
- **The texMap→texture mapping is fully static** (`TerrainDefinition.TextureInfo
  → string_dictionary → WorldArt filename); no runtime/resource-cache dump needed.

## Reproduction artifacts
- The `texMap → {shader, slot, repetition, worldart_id}` lookup is **built at
  runtime** from `TerrainDefinition.uop` + `string_dictionary.uop` — see Q3 "How
  to pull the textures at runtime". (No file is shipped; re-derive it at load so
  it tracks game patches.)
- `tools/ec_research/out/terraintexture_contact.png` — all 38 atlases (Q1).
- `tools/ec_research/out/terrain_textures_decoded.png` — decoded real terrain textures (grass + red mask).
- Blob→worldart match + BC1/BC3 decoder: ad-hoc scripts over `UOSA.trace` blobs
  (`apitrace dump --blobs`), byte-compared to `Texture.uop`/`TerrainTexture.uop`;
  hash→name via UOReader `Dictionary.dic`.

---

# TRANSITION BLEND — decoded

> ## ⚠ CORRECTION (2026-06 — verified against the RAW decompiles of `FUN_00461110` + `FUN_004618b0`)
> The original A–D text below (written before `FUN_00461110` was exported)
> claimed the feather is **gated per-edge by the facet delimiter** (`self ==
> neighbourRing[dir]`). **That is WRONG.** Reading the actual `FUN_00461110.c`
> (now in `ec_dbg/ghidra/`):
>
> 1. **Feather gating is PER-LAYER, not per-edge.** `FUN_00461110`'s `param_3`
>    (featherStrength) comes from the layer's blend scalar (`FUN_004618b0` line
>    58: `if ((float)param_1[0xe] == 0.0)` → opaque, else feathered). A terrain
>    type *either* feathers into everything *or* doesn't. There is **no per-edge
>    delimiter test** anywhere in the interior.
> 2. **The feather dilates the layer's terrain ONE cell into ALL adjacent
>    non-member cells** — pure membership adjacency (`FUN_00461110` pass-2 lines
>    131–158: a `cVar2==0` texel horizontally/vertically-between or diagonally-
>    contacting a `255` member gets the random feather alpha). It is NOT limited
>    to delimiter-authored edges.
> 3. **The 8-neighbour ring slots (`+0x24…+0x44`) are read ONLY at chunk
>    borders** (`FUN_00461110` pass-1 lines 43–86: the `iVar7==0/0x1f` and
>    `iVar3==0/0x1f` branches) to clip membership so a terrain only feathers
>    across a chunk seam where the adjacent chunk also has it. Interior cells use
>    `bVar8 = self-only` (`LAB_00461224`). The ring is **chunk-seam membership
>    clipping, not interior feather gating.**
> 4. **The layer key (`cell.self` at `+0x18`) is the BYTE terrain-TYPE id**
>    (the TerrainDefinition record index / "newId"; `FUN_00461bc0` line 160 reads
>    a byte). So every CC graphic that maps to the same newId is ONE layer — all
>    grass variants merge, no spurious internal boundaries.
> 5. The random feather alpha is `round(rand()*255)` — **`local_410`/`local_414`,
>    ONE pair of values per mask** (`FUN_00461110` lines 113–116), reused for the
>    whole ring; bilinear filtering of the 32×32 (1 texel/cell) texture turns the
>    1-cell ring into the soft edge.
>
> **Consequence for the port:** "crisp vs blend" is decided by the per-terrain
> blend scalar (≈ a blendable flag: grass/dirt/sand feather, brick/stone/pavers
> don't — `param_1[0xe]==0`), NOT by per-edge delimiters. Key layers by newId.
> The grass↔dirt softness is the per-layer 1-cell dilation × bilinear. The
> sections below (A "delimiters", §3 of "WRONG") describe the delimiter theory
> that the raw code does not support — kept for history but superseded by this box.

> **This section answers A–D (selection / coverage geometry / draw-state /
> delimiter direction) by decoding the actual functions, superseding the "P2
> strong inference".** The cross-terrain transition is NOT extra edge geometry
> and NOT per-vertex alpha. It is the **per-layer t3 coverage mask**, generated
> on the CPU in `FUN_00461110` from the per-cell terrain grid + an 8-neighbour
> ring (the expanded facet delimiters), with a 1-pixel feathered (randomised)
> border. Evidence is cited by function offset and the relevant decompiled
> lines. Source files: `ec_dbg/ghidra/FUN_00461bc0.c`, `FUN_00461790.c`,
> `FUN_004604a0.c`; pulled callees `FUN_004618b0`, `FUN_00461110`, `FUN_0043b3c0`,
> `FUN_0043b2e0`, `FUN_00460d20`, `FUN_00691d20`, `FUN_0068fc00`.

## Overview — one mesh, N layer-draws, coverage decided by the mask (not geometry)

The whole chunk is **one shared 32×32-cell vertex mesh** built once
(`FUN_00461bc0`, the `do…while (piStack_14c < 0x20)` double loop, lines
155–285). There is **no per-edge / per-delimiter geometry** anywhere — the loop
emits exactly 4 corner verts per cell and never branches on a neighbour. The
mesh is then drawn **once per terrain layer present in the chunk**. Each draw's
*spatial coverage* is supplied entirely by that layer's **t3 coverage mask**
(stage 3 alpha), which is a 32×32 RGBA texture baked per (chunk, layer) by
`FUN_00461110`. So: **selection + coverage live in the mask, not in geometry or
vertex color.** (Vertex `D3DCOLOR` is lighting only — confirmed: `FUN_00460d20`
computes it from per-corner heights × `0.12856454` cross-products = a normal/
shade, see M2.)

The per-chunk layer set is the std::map/list walked at
`param_1[5]+0x1600c` (FUN_00461bc0 lines 111–151 collect it; lines 407–538
re-walk it to attach one `UOTerrainTexturingProperty` per layer). For each
layer, `FUN_004618b0` is called (line 463) which (a) instantiates the layer's
shader object via `FUN_00461790` (`UODefaultTerrainLayer`/`UOWaterTerrainLayer`/
`UOBumpMapTerrainLayer`) and (b) **calls `FUN_00461110` (at `0x461936`) to bake
that layer's coverage mask.**

## A. Transition SELECTION — per-cell terrain id + 8-neighbour ring (the delimiters)

**Each cell carries its own terrain id AND a fixed 8-slot neighbour-terrain
ring** in an 88-byte (`0x58`) per-cell record. The facet's *variable* delimiter
list (`{direction, z, graphic}` per Facets.md) is **expanded at sector-load into
this fixed 8-neighbour table** so the renderer can test any compass direction in
O(1). Field map within the cell record (base = cell index × `0x58`, `+8` header;
proven by which offset `FUN_00461110` tests at each chunk boundary, and matched
by the elevation reader `FUN_00460d20` which walks the same `0x58` stride):

| offset | meaning | offset | meaning |
|-------:|---------|-------:|---------|
| `+0x18` | **self** terrain id (the layer key) | `+0x30` | **W** neighbour |
| `+0x24` | NW neighbour | `+0x38` | **E** neighbour |
| `+0x28` | **N** neighbour | `+0x3c` | SW neighbour |
| `+0x2c` | NE neighbour | `+0x40` | **S** neighbour |
|         |             | `+0x44` | SE neighbour |

(self at `+0x18` sits between W `+0x30` and E `+0x38` = the centre of a 3×3 ring
with the corners/edges at the 8 slots above.) Each slot holds the *terrain id of
the neighbour in that direction* — i.e. the delimiter's resolved terrain, or the
cell's own id where no delimiter exists.

**The blend test is pure equality:** a layer covers a cell iff that cell's
`+0x18 == layerId` (the membership), and the **feather into a neighbour cell is
allowed only where the neighbour's ring slot in that direction `== layerId`**
(FUN_00461110 boundary tests below). So *whether two terrains blend* is decided
by **`selfId == neighbourId` comparisons against the delimiter-expanded ring** —
NOT by a typeFlag and NOT by the shader class. Crisp boundaries (brick↔stone)
simply have **no delimiter** linking them, so the neighbour ring slot ≠ the other
terrain's id and the feather is suppressed (the mask stays a hard cell edge).

> Mechanism of "crisp vs blend": EC's facet authoring decides it. If the sector
> data emits a delimiter for that edge (neighbour graphic recorded in the ring),
> the mask feathers across; if not, the mask is a hard diamond edge. Brick/pavers
> are authored without grass/stone delimiters → crisp.

The layer object itself is fetched per terrain id from a red-black tree
(`FUN_0043b3c0` / `FUN_0043b2e0` = std::map lower-bound lookups keyed by the
terrain id `*param_2`); `FUN_00461bc0` line 163 `if (*piVar7 == puStack_144)`
gates whether a cell contributes verts to the *current* layer draw — i.e. the
membership half of selection happens at mesh-build time, the feather half at
mask-bake time.

## B. COVERAGE GEOMETRY — it is a 32×32 RGBA mask, CPU-baked, 1px feathered

`FUN_00461110(param_1=out, param_2=cellGridBase, param_3=featherStrength)`
builds the mask in two passes:

**Pass 1 — membership grid** (`local_408[0x400]` = a 32×32 byte grid). For each
cell `(iVar7=row, iVar3=col)`:
```
bVar8 = (cell[+0x18] == layerId);            // self membership
if (param_3 > 0) bVar8 &= neighbourTest;     // edge/corner: require the ring slot == layerId
```
`neighbourTest` selects the ring slot by which chunk edge the cell is on:
- top row (`iVar7==0`): inner→`+0x28`(N); corners also require `+0x24/+0x2c` etc.
- bottom row (`iVar7==0x1f`): `+0x40`(S) (+ `+0x3c/+0x44` at corners)
- left col (`iVar3==0`): `+0x30`(W); right col (`iVar3==0x1f`): `+0x38`(E)
- interior cells: `bVar8 = self only` (goto LAB_00461224, no neighbour test).

So **at chunk borders the membership is clipped to where the adjacent chunk also
has this terrain** (prevents double-feather across chunk seams). If
`param_3 <= 0` (feather disabled) it is pure self-membership.

**Pass 2 — rasterise + feather to the 32×32 texture** (the nested
`do…while(iVar3<0x400)` loop). For each texel it writes **all 4 RGBA bytes = the
same coverage value** `cVar2` (so the texture is RGBA8, alpha == rgb == coverage;
`FUN_00691d20(...,0x20,0x20,&DAT_00de4570,1,1)` = 32×32, then
`FUN_0068fc00` wraps it as a `NiSourceTexture`). The value is:
```
cVar2 = (membership[i] != 0) ? 0xFF : 0;                 // solid interior / exterior
// feather: a cell that is NOT a member but is 4-adjacent (and/or diagonally) to
// members gets an INTERMEDIATE value instead of 0:
if (cVar2==0 && <horizontally between two members OR vertically between two members
                 OR a diagonal-only contact>) cVar2 = local_410;   // = feather alpha
// and a member cell touching the grid edge can be pulled to local_414 (border alpha)
```
where **`local_410` and `local_414` are RANDOMISED per-mask feather alphas**:
when `param_3 > 0` they are `round( rand() * 255 )` (`FUN_00bdbbf0` = the FP RNG,
× 255.0 — lines `local_410 = round(rand*255); local_414 = round(rand*255)`).
When `param_3 <= 0` they are 0 (no feather).

**Net: the feather is exactly ONE pixel wide** (one cell ring around the
membership), with a **randomised partial alpha** rather than a fixed ramp — this
is what gives the EC transition its soft, slightly noisy edge. There is **no
multi-pixel gradient and no distance field**; the smoothness you see is *1-cell
feather × bilinear texture filtering* (the mask is sampled at chunk-UV 0..1 over
32 cells, so each of the 32×32 texels stretches across one whole cell and
bilinear interpolation ramps the alpha smoothly between the 0 / feather / 255
texels).

`param_3` (featherStrength) comes from the layer: in `FUN_004618b0` the
branch `if ((float)param_1[0xe] == 0.0)` (the layer's blend/`global_param`
scalar, see M1 `global_param`) selects opaque-vs-feathered; that same scalar is
passed as `FUN_00461110`'s `param_3`. **Layer 0 / param==0 ⇒ no feather (opaque
base); overlay layers with a non-zero blend param ⇒ feathered mask.**

## C. LAYER DRAW ORDER & BLEND STATE (confirmed vs trace, Q4)

- **Draw order = the layer list order** (the std::map walk; base/most-common
  terrain first, overlays after). Painter's order, all at equal Z.
- **Per-cell membership** (mesh verts emitted only for `cell.self==layerId`,
  FUN_00461bc0 L163) means each layer only rasterises its own cells + the
  feathered border the mask adds.
- **Blend state** (from the cumulative state, Q4): `ALPHABLENDENABLE=TRUE`,
  `SRCBLEND=SRCALPHA`, `DESTBLEND=INVSRCALPHA`, `ALPHATESTENABLE=TRUE` (ref 0,
  GREATER — discards only `a==0`), `ZWRITE=TRUE`, `ZENABLE` on, `LIGHTING=FALSE`.
- **Stage-3 alpha source:** layer 0 = `D3DTA_DIFFUSE` (vertex a=1 ⇒ opaque base);
  overlays = `D3DTA_TEXTURE` = the t3 mask alpha. So overlays are
  **alpha-BLENDED** by the mask's feathered alpha (not merely alpha-tested) —
  the alpha-test only kills fully-uncovered texels. This is the corrected M3:
  earlier "alpha-test stamping, blend off" was from the trimmed trace; the full
  trace shows blend ON. The 1px feather alpha therefore composites smoothly.
- **NiAlphaProperty** is attached to the TriShape (`FUN_00461bc0` lines 561–566
  set `NiAlphaProperty::vftable` with flag word `…|0x12ed`), confirming the
  terrain mesh carries an alpha-blend+alpha-test property, consistent with the
  above.

## D. DELIMITER DIRECTION ENCODING

From the ring-slot offsets `FUN_00461110` tests at each chunk edge, the facet
delimiter `direction` byte (which the loader expands into the `+0x24…+0x44` ring)
maps to the 8 iso neighbours as: **N=`+0x28`, S=`+0x40`, W=`+0x30`, E=`+0x38`,
NW=`+0x24`, NE=`+0x2c`, SW=`+0x3c`, SE=`+0x44`** (in struct order
NW,N,NE,W,[self],E,SW,S,SE = the natural row-major 3×3 ring, self omitted). The
4 cardinal directions are the primary edge-transition markers; the diagonals are
used at chunk corners and for the diagonal-only feather-contact case in pass 2.
(The raw on-disk `direction` byte's 0/1/2/3 → which cardinal is the one residual
unknown — read the sector-loader's delimiter-expansion switch to pin it; the
*ring* offsets above are what the renderer consumes and are certain.)

## What your current approach gets WRONG vs the real client

Your approach: opaque self-diamond + per-edge OVERLAY diamonds of the neighbour
terrain, per-corner alpha = fraction-of-4-touching-cells, normal-blended. The
real EC differs in **four** ways:

1. **Coverage source is a baked 32×32 per-(chunk,layer) RGBA mask, not extra
   overlay diamonds.** EC draws *the layer's own terrain* (not the neighbour's)
   wherever the mask alpha > 0, and the mask's feather **pulls that layer's
   texture OUT past its cells by exactly one cell**, with bilinear filtering
   ramping it. You are drawing the *neighbour's* terrain inward; EC draws *each
   layer outward* and lets the lower layers show through the feather. Visually
   that is "each terrain dilates ~1 cell into its neighbours and they cross-fade",
   not "neighbour bleeds in along the edge".
2. **Feather is 1 cell wide with a RANDOMISED alpha** (`round(rand()*255)`),
   then **bilinear-smoothed** — not a deterministic corner-fraction. Your
   per-corner fraction gives a clean linear ramp; EC's is a noisy 1-px ring that
   reads softer because of the bilinear stretch (1 texel ≈ 1 cell). To match:
   bake a per-chunk A8/RGBA mask at cell resolution = {255 inside, 0 outside,
   random∈(0,255) on the 1-cell border ring where the neighbour-ring slot ==
   this layer}, sample bilinear at chunk-UV.
3. **Selection is `self==neighbourRing[dir]` equality**, gated by whether the
   facet emitted a delimiter for that edge — so non-delimited edges (brick↔stone)
   produce **no feather ring at all** (hard mask edge). Your "in the delimiter
   list AND terrain differs" is close, but you must suppress the feather (not
   just skip the overlay) and you must use the **expanded 8-ring** including
   diagonals for corners.
4. **Composite is the per-layer mesh re-drawn with SRCALPHA/INVSRCALPHA blend +
   alpha-test ref0**, painter-ordered by the layer list, equal Z, ZWRITE on — and
   the per-pixel color is `lerp(baseAlbedo, partnerAlbedo, noiseMask.a) ×
   vertexLight` (Q4), THEN masked by the coverage alpha. You should drive the
   transition with the coverage alpha in the blend, with the albedo lerp/light
   unchanged per layer.

### Minimal implementation recipe
Per chunk, per terrain layer L present:
1. Build a 32×32 coverage byte grid: `cov[c] = (cell.self==L) ? 255 : 0`.
2. If L's blend param > 0, **feather**: for every `cov[c]==0` cell that is
   4-adjacent to a `255` cell **and** whose ring slot toward that member ==
   L (i.e. a delimiter authorised the blend), set `cov[c] = rand()∈1..255`
   (one random value per mask is what EC does; a fixed ~128, or a small
   per-texel random, both approximate it). Clip the ring at chunk borders to
   where the neighbour chunk also has L (pass-1 boundary tests).
3. Upload as a 32×32 texture (alpha = cov), sample **bilinear** at chunk-UV.
4. Draw the shared chunk mesh with this layer's albedo (`lerp(base,partner,
   noise.a)×vertexLight`), `out.a = (L==base)?1:cov.a`, blend
   SRCALPHA/INVSRCALPHA, alpha-test GREATER ref 0, ZWRITE on, painter order.
No per-edge geometry, no neighbour-terrain overlays.
