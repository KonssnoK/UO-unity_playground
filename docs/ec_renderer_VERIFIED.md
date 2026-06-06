# EC Renderer — verified via APItrace + Ghidra

This document captures everything we learned about how EC's `UOSA.exe`
actually renders tiles, based on a real D3D9 trace (`UOSA.trace`, 318 MB,
5657 frames) plus a full-binary Ghidra dump (47,877 functions, 52 MB
JSONL) of the binary.

## Capture setup

- Tool: [APItrace 14.0](https://apitrace.github.io/) win32 build, portable.
- Method: dropped the APItrace `d3d9.dll` wrapper next to `UOSA.exe`
  (`C:\Games\Electronic Arts\Ultima Online Enhanced\d3d9.dll`). Windows
  DLL search order loads it instead of `System32\d3d9.dll`, transparently
  logging every D3D9 call.
- Output: 5657 frames at startup → in-game → slate roof / water → exit.
- Trimmed-trace tooling: `apitrace trim --frames=5627-5657 -o
  UOSA_lastframes.trace UOSA.trace` for fast inspection.

RenderDoc did NOT work for EC. EC is a Gamebryo-based engine
(`NiFloatsExtraData` and other `Ni*` strings appear throughout the
Ghidra dump). Gamebryo creates the D3D device from inside a late-loaded
DLL, and RenderDoc's launch-time hook never sees the device init —
`API: None` in the launcher. APItrace's DLL-search-order proxy bypasses
that entirely.

## Top-level architecture

EC's world view is **not** a sprite-batched renderer like CC/CUO. It's
a 3D mesh renderer that happens to use an iso-projection camera. Three
distinct paths can be seen in the trace:

| Path | Vertex stride | Verts/draw | Texture stages | Used for |
|---|---|---|---|---|
| **Terrain chunked mesh** | 32 B | **4096** (32×32 cells × 4 unique verts/cell) | **4** | Land, surface statics (floors, water, slate roofs) |
| Sprite batch (small) | 52 B | 4–240 (4/quad) | 1–2 | Standalone statics (walls, items, decorations) |
| Sprite batch (HUD) | varies | small | 1–2 | UI, gumps, paperdoll |

CC/CUO conflates everything into the "sprite batch" path. EC routes
surface tiles into the chunked-mesh path that we've been seeing in
RenderDoc traces.

## The terrain chunked-mesh path (verified end-to-end)

### Vertex buffer

Created with:
```
CreateVertexBuffer(Length = 131072, Usage = D3DUSAGE_WRITEONLY,
                   FVF = 0, Pool = D3DPOOL_MANAGED) -> 0x1eafd9e0
Lock(...) ; memcpy(blob(131072)) ; Unlock()
```
131 072 B = 4096 verts × 32 B/vert. **Static** (`D3DPOOL_MANAGED` +
`D3DUSAGE_WRITEONLY`, no `D3DUSAGE_DYNAMIC`) — filled once when the
camera moves to a new area, then reused across many draws of the same
chunk.

### Vertex layout (decoded from the dumped blob)

Per-vertex stride **32 B**:

| Offset | Type | Field |
|---|---|---|
| 0x00 | float×3 | **POSITION** in **world space** (x, y_elevation, z) |
| 0x0C | D3DCOLOR/u32 | per-vertex color (4 B, packed) |
| 0x10 | float×2 | **TEXCOORD0** — sprite UV |
| 0x18 | float×2 | **TEXCOORD1** — "world-space UV" (tile-fill) |

Verified vertex 0 from the dump:
```
pos = (1312.00, -0.20, -1472.01)     // real UO map coords + tiny Y elevation
uv0 = (0.000, 0.000)
v1: pos = (1313.00, -0.16, -1472.00) // x+1 in world
    uv0 = (0.031, 0.000)             // = 1/32 step
v4: pos = (1313.00, -0.20, -1472.01) // SAME position as v1
    uv0 = (0.031, 0.000)             // SAME uv as v1
```

Findings:

1. **Positions are real UO map coordinates**, not screen-space. The iso
   projection is applied in the vertex shader via `worldTransform ×
   viewProjMatrix`, NOT pre-baked into vertex positions.
2. **Cell vertices are NOT shared** with neighbors. Each cell carries 4
   unique vertices (so 1024 cells × 4 = 4096 verts).
3. **UV.x step per cell along X is `1/32`** (`0.03125`). Across the
   chunk's 32-cell width, UVs go `0 → 1` — i.e. the master texture
   tiles **once per 32 cells** along each axis.
4. Y stores **terrain elevation** as a small float (-0.20 .. -0.26 in
   the sample). Real-world height affects projected screen Y.

### Per-draw state pattern

Every chunked draw follows this state setup (from the trim, calls
24-62):

```
SetTextureStageState(0, COLOROP, SELECTARG1)
SetTextureStageState(0, COLORARG1, TEXTURE)
SetTextureStageState(0, TEXTURETRANSFORMFLAGS, COUNT2)
SetTextureStageState(0, RESULTARG, TEMP)        ; stage 0 -> TEMP register

SetTextureStageState(1, COLOROP, SELECTARG1)    ; stage 1 = hue palette
SetTextureStageState(1, ALPHAOP, SELECTARG1)
SetTextureStageState(1, ALPHAARG1, TEXTURE)
SetTextureStageState(1, TEXCOORDINDEX, 0)

SetTextureStageState(2, COLOROP, BLENDCURRENTALPHA)   ; stage 2 = blend
SetTextureStageState(2, COLORARG1, TEXTURE)
SetTextureStageState(2, ALPHAOP, SELECTARG1)
SetTextureStageState(2, ALPHAARG1, TEXTURE)
SetTextureStageState(2, TEXCOORDINDEX, 0)

SetTextureStageState(3, COLOROP, MODULATE)            ; stage 3 = modulate
SetTextureStageState(3, ALPHAOP, SELECTARG1)
SetTextureStageState(3, ALPHAARG1, DIFFUSE)           ; sometimes TEXTURE
SetTextureStageState(3, TEXCOORDINDEX, 1)             ; uses UV1!

SetTexture(stage=0, pTexture=...primary color...)
SetTexture(stage=1, pTexture=...hue palette...)
SetTexture(stage=2, pTexture=...secondary blend texture...)
SetTexture(stage=3, pTexture=...modulation/diffuse texture...)

SetStreamSource(stream=0, pStreamData=0x1eafd9e0, stride=32)
SetVertexDeclaration(0x1dfe93e0)
DrawIndexedPrimitive(TRIANGLELIST, NumVertices=4096, primCount=2048)
```

What the texture stages do (deduced from `D3DTOP_*` opcodes):

- **Stage 0**: sample tile-fill master at TEXCOORD0 → write to TEMP.
- **Stage 1**: provide the hue palette + per-cell hue index from the
  diffuse color (TEXCOORD2 in sprite shader / per-vertex color in
  terrain shader).
- **Stage 2**: sample a **second color/detail texture** at TEXCOORD0;
  uses `BLENDCURRENTALPHA` to blend on top of stage 0 based on alpha.
  Likely a per-cell variation or normal/light map.
- **Stage 3**: modulate with **TEXCOORD1** (the world-space UV). With
  `MODULATE` + `ALPHAARG = DIFFUSE`, this applies a wide-area modulation
  pattern — probably the per-chunk "stone-vs-grass" mask that determines
  which cells of the chunk actually show the primary texture.

So a single mesh is drawn once **per primary texture**, and the masks
in stages 2/3 selectively reveal that primary texture only on cells
that use it. This is why we saw ~14 consecutive 4096-vert draws in a
row at the start of each frame — each draw "lays down" a different
terrain texture layer over the same mesh.

### CC equivalent

CC has no analogue. Each surface tile is a 44×44 pre-projected diamond
TGA in `art.mul`, drawn axis-aligned at the cell's screen position.
The diamond shape is baked into the alpha mask.

## How this influences statics rendering in CUO

This is the gap between "what we do" and "what EC does":

| Tile class (CC flag) | CUO today | EC actual |
|---|---|---|
| Land (top-down diamond) | Per-tile sprite via `WriteQuadAt` / `DrawStretchedLand` | Single chunked mesh, stage-0 = terrain texture |
| **Surface static** (IsSurface, slate roof, floor, water) | Per-tile sprite (or our `WriteIsoDiamondAt`) | **Same chunked mesh as land** — surface statics blend into the terrain layer |
| Roof (IsRoof) | Per-tile sprite | Per-tile sprite **with alpha** (e.g. palm-frond at 24 % opaque). EC sprite path |
| Wall, item, foliage | Per-tile sprite (alpha-trim HD) | Per-tile sprite, ~52 B vertex stride |
| Wet (IsWet) | Per-tile sprite or animated water effect | Chunked mesh + `MythicNewWaterShader` (separate DRAW with water-specific stage setup) |

Concretely, what the trace tells us about our current CUO approach:

1. **Surface statics** (slate roof / floor / water) **cannot be made
   pixel-identical to EC without a chunked-mesh renderer.** EC samples
   `1/32` of the master per cell using world-space UV continuity
   (`uv.x = world_x / 32`). Adjacent cells share the texture pattern
   seamlessly because their UVs literally pick up where the neighbor
   left off. A per-cell sprite approach can only approximate this by:
   - Picking a single tiny patch of the master and warping it into the
     cell — what `WriteIsoDiamondAt` does. Adjacent cells get the same
     patch, so the pattern *repeats* per cell rather than *continues*.
   - Doing world-position-modulo UVs per cell — which works only if the
     sampler wraps (CUO's static-batch sampler is `PointClamp`, so UVs
     beyond 1 clamp instead of wrap).
2. **Non-surface statics** (walls, items, foliage, roofs with alpha)
   ARE drawn as sprites in EC, with a 52 B vertex stride (POS + NORMAL
   + COLOR + 3 UV streams). Our per-sprite path can match these
   reasonably well — the HD master, alpha-trim, and CC-anchor pipeline
   we have today is the right architecture.
3. **The "stones look more compressed in CUO than in CC"** symptom is
   a direct consequence of point 1: we crop 44×44 of the source and
   stretch it into the diamond; EC samples only 8×8 worth of source
   (1/32 of a 256-wide master) and tiles it across 32 cells. Per-cell
   that gives EC ~5× larger features visible.

## Current implementation (shipped)

CUO now uses **option B**: surface tiles whose group master is fully
opaque fall back to the per-tile legacy DDS (CC-equivalent diamond),
keeping the HD path only for tiles whose masters have alpha (walls,
items, foliage). Detection lives in
``EcArt.TryGet`` using
`IsFullyOpaqueDds` on the master DDS — DXT1 is always opaque (no alpha
channel by spec), DXT5 is detected by scanning every block's
`a0/a1 = 255` endpoints.

Trade-off accepted:
- Surface tiles (slate roof, water, floors) render with CC-equivalent
  legacy art — pixel-identical to CC mode, but no HD detail.
- Non-surface statics still use EC's HD masters → user gets HD walls,
  items, foliage as designed.
- No new shaders, no architectural refactor.

## Future work — chunked-mesh terrain renderer

To match EC's surface-tile fidelity (HD textures with proper iso
projection + seamless tiling across cells) we need a new render path:

1. Group cells by sector. For each visible sector, build (or fetch
   from cache) a 32×32-cell mesh in world space with the 32 B vertex
   layout decoded from the trace: POS3 + COLOR(D3DCOLOR) + UV0 + UV1.
   World-space UVs use the formula `uv = world_xz / 32`.
2. Per primary texture, draw the full mesh with 4 texture stages
   (color / hue palette / detail+blend / world-UV modulation).
3. Apply the iso projection in a vertex shader via a `worldTransform ×
   viewProjMatrix` uniform pair — this turns the world-space mesh into
   on-screen diamonds.
4. Coordinate the depth buffer with the existing sprite renderer so
   walls/items composite correctly with the terrain mesh.

The biggest unknowns are the stage-3 modulation mask (per-chunk "where
does this texture appear?" map) and how EC builds the dynamic
per-camera mesh — both are doable but require sustained focus.

Reference vertex layout (sampled from the trace):
```
v0:  pos = (1312.00, -0.20, -1472.01)   uv0 = (0.000, 0.000)
v1:  pos = (1313.00, -0.16, -1472.00)   uv0 = (0.031, 0.000)   // +1 X = +1/32 U
v2:  pos = (1312.00, -0.16, -1473.01)   uv0 = (0.000, 0.031)   // +1 Z = +1/32 V
v4:  pos = (1313.00, -0.20, -1472.01)   uv0 = (0.031, 0.000)   // new cell, picks
                                                                 // up where v1 ended
```
Per-cell vertices are NOT shared with neighbours; each cell ships its
own 4 verts. Total mesh = 32×32 cells × 4 verts = 4096 verts × 32 B =
131072 B per chunk vertex buffer (matches the trace).

## Sprite render path details (verified)

For completeness: the 52 B sprite path used by walls/items/etc.

```
SetStreamSource(stream=0, pStreamData=<dynamic VB>, stride=52)
SetVertexDeclaration(...)
SetTexture(stage=0, pTexture=<sprite>)
SetTexture(stage=1, pTexture=<hue palette = 0x1d80de60>)   ; constant
DrawIndexedPrimitive(TRIANGLELIST, NumVertices=4N, primCount=2N)
```

Stride 52 B = `float3 POS + float3 NORMAL + COLOR + float2 UV0 + float2
UV1 + float2 UV2 = 12+12+4+8+8+8 = 52`. Matches `Shaders.uop`
shader_01's VS_INPUT exactly:

```hlsl
float4 position : POSITION
float2 texCoord0: TEXCOORD0   // sprite uv
float2 texCoord1: TEXCOORD1   // world-space uv
float2 texCoord2: TEXCOORD2   // offset into hue texture
float4 color    : COLOR0
```

Each sprite consumes 4 verts. EC batches N sprites into a single draw
when they share the same primary texture, producing draws of size
4, 16, 40, 80, 240 verts etc.

## CUO integration — current state

The C# port in `src/ClassicUO.Renderer/Arts/EcArt.cs` and
`src/ClassicUO.Renderer/Animations/EcAnimation.cs` exposes three
**tileart modes** via the `EcArtMode` enum, switchable in-game with F11:

| Mode | Source | Anchor math | Mask | Notes |
|---|---|---|---|---|
| `ClassicMul` (0) | `art.mul` / `artLegacyMUL.uop` | CC native | — | Default; renderer skips EC entirely |
| `UopKR` (1) | `Texture.uop` HD master + `EcImage` crop | bottom-center on cell + dx/dy + scale `1/1.5` | Partial-hue (`tileartlegacy/{1000000+id}.dds`) | Kingdom-Reborn-era big upscaled sprites; falls back to legacy DDS when no HD entry |
| `UopEC` (2) | `LegacyTexture.uop` `tileartlegacy/{id}.dds` | CC anchor (`artInfo.UV`) on full POT-padded DDS | — | What the actual Enhanced Client uses for statics |

EC **animations** are wired in via a separate F10 toggle (boolean —
on/off, no tristate). When enabled:

- `EcAnimationLoader` opens `AnimationFrame{1..6}.uop` and finds entries
  by hash of `build/animationframe/{body:D6}/{action:D2}.bin`.
- `EcAnimation` decodes the AMOU stream and builds a per-frame canvas
  matching the file's MainBbox (so the body anchor stays stable across
  frames).
- `Animation.TryBuildEcFrames` translates CC's per-body-group action
  number to AMOU's universal `HighAnimationGroup` numbering, respecting
  the `CalculateOffsetLowGroupExtended` flag on Animal bodies (see
  `AnimationDefinition.md` for the full action remap table).
- Substituted into the existing `GetAnimationFrames` path; the atlas
  uploads decoded pixels at the same point CC frames would.

### Settings persistence

- `tileart_mode` (int 0/1/2) in `settings.json` — survives restarts.
- `use_ec_animations` (bool) — same.
- `use_enhanced_art` legacy boolean is shim'd through for older
  settings files.

### Outstanding work

- **EC animation playback speed** — characters animate "too fast" when
  EC AMOU is active. AMOU has **5 directions packed per action file**, so the
  per-action frame total is 5× a single direction; if playback iterates all
  frames it runs 5× too fast. Slice to one direction (`frames/5`) before
  stepping. (AMOU has no timing field — the old "0x28 mystery" was just
  palette[0]; see [AnimationFrame_AMOU.md](AnimationFrame_AMOU.md).)
- **Chunked-mesh terrain renderer** — the big architectural item.
  Right now EC-mode terrain falls through to CC's sprite-batched land
  renderer (fully-opaque HD masters get bypassed via the
  `IsFullyOpaqueDds` short-circuit). A proper port would add a second
  render path matching EC's 32×32 mesh with world-position UVs.

## Files / where evidence lives

- Full D3D9 trace: `C:\Users\konss\Desktop\UOSA.trace` (318 MB)
- Last-frame trim: `C:\Users\konss\Desktop\UOSA_lastframes.trace` (2 MB)
- Decoded vertex buffer blob: `C:\Users\konss\Desktop\apitrace_blobs\blob_call14840372.bin` (128 KB, 4096 verts)
- Full Ghidra decompile: `tools/ghidra/ghidra_full.jsonl` (52 MB, 47877 fns)
- HLSL shaders: `tools/ec_research/dump_shaders/*.hlsl` (12 generic shaders — terrain shader is NOT in `Shaders.uop`; it's compiled into the binary as effect bytecode)
