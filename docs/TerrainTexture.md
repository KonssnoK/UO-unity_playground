# TerrainTexture.uop

**Internal registry slot pair:** 46 / 47.

## What it contains

38 DDS atlases (256×256, DXT5). **They are NOT the terrain ground textures.**
Decoding all 38 shows faint **cream/tan radial gradients, glows and soft brush
blobs, mostly transparent** (opaque coverage ≈1–20%). Byte-comparing them against
every texture the EC binds in its terrain draws (from an APItrace capture):
**none of the 38 is used by the terrain pass.** They are detail/glow/brush assets
for some other effect, not material albedo.

> ⚠ **Correction.** Earlier this doc (and the early terrain RE) claimed these were
> "the base material textures the terrain renderer samples through
> AtlasTerrainShader." **That was wrong.** The actual EC terrain albedo/mask
> textures live in [`Texture.uop`](Texture.md) (`build/worldart`), referenced by
> name from [`TerrainDefinition.uop`](TerrainDefinition.md) via
> [`string_dictionary.uop`](string_dictionary.md). See
> [EC_Terrain_Renderer_Findings.md](EC_Terrain_Renderer_Findings.md) → P1 CORRECTION.

## Naming

```
build/terraintexture/{id:08}.dds
```

- **100% coverage** (38 of 38; ids `[1..17, 20..40]`).
- The `id` is an atlas index, **not** a CC land-tile id, and **not** a `texMap`.

## Where the real terrain textures come from

```
TerrainDefinition[texMap].TextureInfo.texturesArray[].textureIDX
  → string_dictionary.values[idx] = "{worldartId:08x}_{Name}.tga"
  → build/worldart/{worldartId:08x}.dds   in Texture.uop
```
e.g. grass = `02000010_Grass_C` + `02000011_Grass_B` + `01000003_noise_alpha`.
The composition is a fixed-function 4-stage splat
(`lerp(base, partner, noiseMask.a) × vertexLight`, alpha-tested coverage) — full
details and the load-time procedure are in the findings doc.

## Notes for the C# port

- You can **ignore `TerrainTexture.uop` for terrain rendering.** Load terrain art
  from `Texture.uop`/`build/worldart` per `TerrainDefinition`.
- If a use for these 38 gradient atlases is later identified (likely a particle/
  decal/overlay effect), document it here; as of this writing nothing in the
  terrain pass references them.
