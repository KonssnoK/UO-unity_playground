# TerrainTexture.uop

**Internal registry slot pair:** 46 / 47.

## What it contains

38 large DDS texture atlases (256×256, mostly DXT-compressed). These are the **base material textures** that the EC terrain renderer samples through `AtlasTerrainShader`. Land tiles do *not* paint individual 44×44 diamonds the way the CC does; instead, every chunk samples one or more of these 38 atlases according to its `TerrainDefinition` record, then blends them in the shader.

## Naming

```
build/terraintexture/{id:08}.dds
```

- **100% coverage** (38 of 38 entries).
- The `id` here is **not** the CC land-tile id. It's an atlas index 0..37 used by the terrain shader.

## Disassembly notes

The decompiled `FUN_00461bc0` is the **`UOTerrainShader::Render`** routine. Highlights from a 600-line function:

- Iterates a 32×32 sector grid (`while ((int)piStack_14c < 0x20)`), 32 by 32 = 1024 chunks per facet sector.
- For each chunk, walks vertex strips and emits per-vertex calls that look like normal-map / colour samples (3-channel float bundles into 4-component vectors).
- The shader is `AtlasTerrainShader` (string `s_AtlasTerrainShader_00d00f58`) backed by `AtlasTerrain.vsh` / `AtlasTerrain.psh`.
- Other terrain shaders referenced: `UOStaticTerrainShader`, `GameTerrainShader`, plus `GameTerrain_Offscreen.{vsh,psh}`, `_VertexLighting`, `_HybridLighting` variants — these are render-mode variants (offscreen pre-pass vs in-place lighting).
- Terrain "layers" found: `UOWaterTerrainLayer`, `UODefaultTerrainLayer`, `UOBumpMapTerrainLayer`, `IUOTerrainLayer` — the EC layers materials per-vertex.

## Connection to the land-tile id

The CC land tile id maps to an EC terrain id via two indirections:

1. `data/gamedata/legacyterrainmap.csv` (in `GameData.uop`):
   `legacyId → (newId, newSubType)` for ~4,162 CC ids.
2. `LegacyTerrain.uop` contains one XML record per `newId` describing a `terrainType` with `texMap` references.
3. The shader then picks atlas slices from `TerrainTexture.uop` per the `TerrainDefinition.uop` record.

The exact slicing logic still requires more RE work — the 600-line `FUN_00461bc0` is the place to read it.

## Notes for the C# port

- DDS read is trivial; FNA hands you a `Texture2D` directly.
- The actual rendering is **NOT** a swap-in. The CC renderer paints per-tile 44×44 diamonds; the EC one streams 32×32-vertex meshes with per-vertex sampling from these 38 atlases and per-fragment blending. This is shader work, not a loader swap.
- For a first integration: prove DDS loading works; then design a `EcTerrainRenderer` from scratch, modelled on `AtlasTerrainShader`.
