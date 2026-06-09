# TerrainDefinition.uop

**Internal registry slot pair:** 20 / 21.

## What it contains

249 binary records (one per EC terrain type), file index = the terrain id
("texMap"). **Each record fully describes how to texture that terrain type** — a
shader-class name + a list of texture references (WorldArt files) with tiling and
slot role. It is **not** an opaque blob and it does **not** reference
`TerrainTexture.uop` atlases. See
[EC_Terrain_Renderer_Findings.md](EC_Terrain_Renderer_Findings.md) (P1 CORRECTION)
for the full render chain.

## Record format — DECODED ✅

(Confirmed against the UOReader `TerrainDefinition`/`TextureInfo` structs, raw
bytes, and the disassembly. `idx` fields are **indices into
[`string_dictionary.uop`](string_dictionary.md)**.)

```
u32  nameIDX        # → stringDict = terrain name, e.g. "grass", "sand", "water"
u32  index          # = the record/file index N = "texMap" (the terrain id)
u32  _unk3
u32  _unk4          # often 1.0f
u32  _unk5
u32  aliasCount
aliasCount × {      # 16 bytes each
    u32 countIndex
    u32 oldAlias
    u64 flags
}
TextureInfo textures        # the texture stack (see below)
```

**TextureInfo** (the same struct `tileart.uop` uses):
```
u8   texturePresent         # 0 → no textures, record ends
u8   _unk1
i32  shaderNameIDX          # → stringDict = layer class:
                            #   "UODefaultTerrainLayer" | "UOWaterTerrainLayer" | "UOBumpMapTerrainLayer"
u8   texturesCount
texturesCount × {           # 17 bytes each
    u32 textureIDX          # → stringDict = "{worldartId:08x}_{Name}.tga"
    u8  _unk
    f32 repetition          # tiling: texcoord scale = 1 / repetition
    i32 textureSlot         # role within the layer (see below)
    i32 _unk
}
u32  count2; count2 × i32    # usually 0
u32  count3; count3 × f32    # usually 0
```

**The worldart id is the 8-hex-digit prefix of the resolved filename string.**
`textureIDX → "02000011_Grass_B.tga" → worldart id 0x02000011 →
build/worldart/02000011.dds` in [Texture.uop](Texture.md).

### Slot roles (per shader class)
- **`UODefaultTerrainLayer`** (203/249): slot0 = `_A`/`_C` partner; slot1 = `_B`
  base; slot2 = `noise_alpha` blend mask (its **alpha** is the lerp weight). Some
  add slot4 = extra overlay.
- **`UOWaterTerrainLayer`** (8/249, water/lava): slot0 = `*_alpha` mask, slot1 =
  diffuse (`water`/`Lava_A`), slot2 = `cube3` reflection cubemap.
- **`UOBumpMapTerrainLayer`** (1/249, snow): the default three **plus** slot3 =
  `water_alpha`, slot4 = `cube0` normal/bump map.

### Worked example — `TerrainDefinition[1]` = "grass"
```
nameIDX → "grass"   shaderNameIDX → "UODefaultTerrainLayer"
slot0  rep10  02000010_Grass_C.tga   (worldart 0x02000010, 512²)  → D3D stage 2 (partner)
slot1  rep 4  02000011_Grass_B.tga   (worldart 0x02000011, 256²)  → D3D stage 0 (base→TEMP)
slot2  rep32  01000003_noise_alpha.tga (worldart 0x01000003)      → D3D stage 1 (mask alpha)
```
This reproduces, byte-for-byte, the textures the APItrace capture bound for a
grass chunk (stage scales 1/10, 1/4, 1/32).

## Naming — RESOLVED ✅

```
build/terraindefinition/{N}.bin       (N = non-zero-padded decimal = record index = texMap)
```

- **100% coverage** (249/249). `N` is the terrain *file/record* index (= `index`
  field), **not** the internal `rec_id` first DWORD (e.g. 0x1d3c9). Source: the
  UOReader 0.8.7 `Dictionary.dic`.

## How a map cell reaches a record

```
facet cell.landtileGraphic
  → data/gamedata/legacyterrainmap.csv  (in GameData.uop):  legacyId → (newId, newSubType)
  → TerrainDefinition[newId]            (newId = the record index N = texMap)
```
(See M6/M7 in the findings doc; `LegacyTerrain.uop` carries only `terrainType
id/name/texMap/typeFlags` — **no texture refs**.)

## Disassembly notes

- Factory class `AVUOTerrainDefinitionBinaryFactory`. The layer class is chosen by
  the `shaderNameIDX` string in `FUN_00461790`
  (`UODefaultTerrainLayer`/`UOWaterTerrainLayer`/`UOBumpMapTerrainLayer`); the
  mesh/draw is `FUN_00461bc0`. WorldArt textures are opened via `FUN_004604a0`
  (`Data\WorldArt\…`).

## Notes for the C# port

- Parse at load into `{ texMap, name, shaderClass, layers[] }` where each layer =
  `{ worldartId, repetition, slot }`. **Build this from the uops at startup** — do
  not ship a pre-generated table (it would go stale across patches). The exact
  load-time procedure is in the findings doc, Q3 "How to pull the textures at
  runtime".
- `repetition` → texcoord scale `1/repetition`. Bind slot1→base, slot0→partner,
  slot2→mask and compose per the Q4 recipe
  (`lerp(base, partner, mask.a) × vertexLight`, splat by coverage).
