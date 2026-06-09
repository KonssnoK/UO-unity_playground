# Texture.uop

**Internal registry slot pair:** 26 / 27.

## What it contains

The **high-resolution (Enhanced Client) static art** — replacement DDS textures for a subset of classic statics. Sizes range up to 256×256 (DXT-compressed). Not all classic statics have HD replacements; this archive is a strict subset of `LegacyTexture.uop`'s id space.

**It also holds the EC terrain textures** (the actual ground albedo/mask/cube maps), in a dedicated id range — see below.

## Also holds: the EC terrain textures (`0x01/0x02/0x03xxxxxx`)

The chunked-mesh terrain renderer pulls **all** its textures from here (not from
`TerrainTexture.uop`). They occupy high id bands and the string-dictionary path
encodes a human name: `Data\WorldArt\{id:08x}_{Name}.tga`, packed as
`build/worldart/{id:08x}.dds`.

| id band | role | examples |
|--------|------|----------|
| `0x01xxxxxx` | masks / noise / cubemaps (alpha-only or reflection) | `01000003_noise_alpha`, `01000004_noise_alpha_sharp`, `01000013_water_alpha`, `01000014_cube0`, `01000017_cube3` |
| `0x02xxxxxx` | **terrain albedo**, in `_A`/`_B` pairs per material (even=512² partner, odd=256² base) | `02000010_Grass_C`/`02000011_Grass_B`, `02000070_Sand_A`/`02000071_Sand_B` |
| `0x03xxxxxx` | extra per-material overlays | `03000121`, `03000251`, … |

These are **referenced by name** from [`TerrainDefinition.uop`](TerrainDefinition.md)
via [`string_dictionary.uop`](string_dictionary.md) (the worldart id is the
8-hex-digit filename prefix), and decoded as ordinary DXT (DXT1 = opaque albedo,
DXT5 = carries the mask alpha). Full chain + composition:
[EC_Terrain_Renderer_Findings.md](EC_Terrain_Renderer_Findings.md) → P1 CORRECTION.

## Naming

```
build/worldart/{id:08}.dds
```

- The disassembly (`FUN_0058e330`) shows the EC asset manager will accept *both* `WorldArt`, `WorldArt\ref`, and `TileArtEnhanced` prefixes when looking up sprites by short name, but the **actual UOP hash convention uses `worldart/`** (verified empirically — 96.0% match).
- File-location code (from `FUN_0058e1a0`): **0x1a (26)** for `TileArtEnhanced\` requests.
- The HD-texture printf format from `FUN_0051af20` is `"%08d_TileArt"` (vs. `"%08d_LegacyTileArt"` for the legacy bucket).

## Empirical coverage

- **Entries in archive:** 9,798.
- **Mapped by `build/worldart/{id:08}.dds`:** 9,410 (96.0%).
- **Unmapped holdouts:** 388. Likely use `build/worldart/ref/{id:08}.dds` or a `_alpha`/`_mask` suffix — Dictionary.dic doesn't list them yet.

## Disassembly notes

- `FUN_0058e330` is the **prefix classifier** for sprite paths: if the path starts with `"WorldArt"`, it accepts it (and `WorldArt\ref` as alternate); otherwise it tries `Textures\`, `TileArtLegacy`, `TileArtEnhanced`, `GumpArtMask` in turn.
- The dual-naming (`WorldArt` ↔ `TileArtEnhanced`) is an EC artifact: internally the engine remembers `WorldArt`, but the user-facing modding API exposes the friendlier `TileArtEnhanced` name. The hash convention took the `WorldArt` side.
- `FUN_0051e1d0` registers Lua hooks: `RequestTileArt`, `ReleaseTileArt`, `RequestTexture`, `ReleaseTexture`.

## Notes for the C# port

- Same loader as `LegacyTexture.uop`; just a different folder name in the hash and a different fallback policy (use the LegacyTexture variant when HD is missing).
- Selection rule: at draw time, prefer `Texture.uop[id]` if it exists, fall back to `LegacyTexture.uop[id]`, then to CC art.
- The dimensions are bigger than the CC's 44×N — the renderer must scale or repack tiles to match.
