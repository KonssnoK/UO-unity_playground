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

Each layer's *colour* is a blend of two terrain-atlas textures (world-tiled) via
a shared detail mask; the per-vertex colour is **lighting**, not splat weight.

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
2. **`layer_rec_id → (atlas#, sub-rect)`** resolution and **`layer_param`**
   weight-vs-tiling — read the TerrainDefinition deserializer
   (`FUN_004cc3f0 → FUN_00a7222c`) and the `TerrainTexture.uop` 38-atlas index.
3. **t1/t3 mask textures** — where the per-chunk coverage masks (t3) come from
   (generated from the cell terrain-type grid? a per-chunk render target?) — the
   46 distinct t3 textures are created outside the captured frames; capture
   `CreateTexture`/`UpdateTexture` for them in the full trace to confirm
   dimensions (expected ~32² A8) and source.
