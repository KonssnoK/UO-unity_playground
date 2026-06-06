# Enhanced Client UOP files — per-file documentation

Each `<UopName>.md` here synthesises three sources of truth:

1. **Empirical**: what we read directly from the file (entry counts, payload magic, dimensions).
2. **Dictionary.dic** (Mythic Package Editor): the authoritative hash→name table, partially populated upstream.
3. **Disassembly of `UOSA.exe`** (Ghidra 12.1, project at `tools/ghidra/project/`). Raw decompilation lives in the `*_raw.md` topic files; the per-UOP docs summarise the **concrete** facts those decompiled functions reveal.

The complete name-resolution pipeline (a hand-built C# struct map for the C# port) is in [`ec/patterns.py`](../ec/patterns.py) and its JSON twin at [`../out/uop_patterns.json`](../out/uop_patterns.json).

## Quick coverage table

| UOP                              | Entries | Naming pattern                                              | Note                                  |
|----------------------------------|--------:|--------------------------------------------------------------|---------------------------------------|
| [LegacyTexture.uop](LegacyTexture.md)          | 52,181 | `build/tileartlegacy/{id:08}.dds`                          | DXT-DDS; 13,196 entries unmapped     |
| [Texture.uop](Texture.md)                      |  9,798 | `build/worldart/{id:08}.dds`                               | HD DXT-DDS; 388 entries unmapped     |
| [tileart.uop](tileart.md)                      | 40,208 | `build/tileart/{id:08}.bin`                                | Tile metadata (binary)                |
| [gumpartLegacyMUL.uop](gumpartLegacyMUL.md)    |  4,376 | `build/gumpartlegacymul/{id:08}.tga`                       | Classic-format gumps (TGA)            |
| [GumpArtMask.uop](GumpArtMask.md)              |  4,597 | `build/gumpartmask/0{id+1000000:d}.dds`                    | **Cracked via disassembly**           |
| [TerrainTexture.uop](TerrainTexture.md)        |     38 | `build/terraintexture/{id:08}.dds`                         | 256×256 atlases                       |
| [TerrainDefinition.uop](TerrainDefinition.md)  |    249 | `build/terraindefinition/{id:08}.bin`                      | Per-terrain definition records        |
| [LegacyTerrain.uop](LegacyTerrain.md)          |  4,108 | unknown (XML payload)                                       | Naming unknown, payload IS the data   |
| [AnimationFrame{1..6}.uop](AnimationFrame.md)  | 34,129 | `build/animationframe/{body:06}/{action:02}.bin`           | AMOU format frames                    |
| [AnimationDefinition.uop](AnimationDefinition.md) | 1,197 | `build/animationdefinition/{id:08}.bin`                  | Per-body action definitions           |
| [AnimationSequence.uop](AnimationSequence.md)  |    388 | `build/animationsequence/{id:08}.bin`                      | Per-body sequence tables              |
| [Paperdoll.uop](Paperdoll.md)                  |      2 | `build/paperdoll/{id:06}/{slot:02}.bin`                    |                                       |
| [MultiCollection.uop](MultiCollection.md)      |    872 | `build/multicollection/{id:06}.bin`                        | Housing / multi-tile collections      |
| [Hues.uop](Hues.md)                            |  3,003 | `data/definitions/hues/hue{id:04}.bmp`                     | 4-digit pad, BMP                      |
| [GameData.uop](GameData.md)                    |     79 | `data/gamedata/<name>.csv` (literal)                       | CSV metadata tables                   |
| [facet{0..5}{,x}.uop](facets.md)               | ~36,000 | `build/sectors/facet_{NN}/{sector:08}.bin`                 | Per-sector map data                   |
| [EffectDefinitionCollection.uop](EffectDefinitionCollection.md) | 269 | `build/effectdefinitioncollection/{id:08}.bin` |                                       |
| Other small archives                           |  varies | mixed `data/<literal>` paths                                | See per-file docs                     |

## Internal IDs (from `FUN_00a70e5a`)

The EC client registers UOPs into an internal table in a deterministic order, assigning two consecutive numeric IDs per UOP. These are NOT the hash IDs of the *contents* — they are the slot numbers of the UOPs themselves inside the asset manager.

| Slot pair | UOP file                              |
|-----------|---------------------------------------|
| 0  / 1    | `facet0.uop`                          |
| 2  / 3    | `facet1.uop`                          |
| 4  / 5    | `facet2.uop`                          |
| 6  / 7    | `facet3.uop`                          |
| 8  / 9    | `facet4.uop`                          |
| 10 / 11   | `facet5.uop`                          |
| 12 / 13   | `facet6.uop` (not present on disk)    |
| 14 / 15   | `tileart.uop`                         |
| 16 / 17   | `string_dictionary.uop`               |
| 18 / 19   | `AnimationDefinition.uop`             |
| 20 / 21   | `TerrainDefinition.uop`               |
| 22 / 23   | `EffectDefinitionCollection.uop`      |
| 24 / 25   | `AnimationSequence.uop`               |
| 26 / 27   | `Texture.uop`                         |
| 28 / 29   | `Audio.uop`                           |
| 30 / 31   | `EffectTexture.uop`                   |
| 32 / 33   | `LocalizedStrings.uop`                |
| 34 / 35   | `TerrainChunk.uop`                    |
| 36 / 37   | `RadarMapTexture.uop`                 |
| 38 / 39   | `Interface.uop`                       |
| 40 / 41   | `GameData.uop`                        |
| 42 / 43   | `MainMisc.uop`                        |
| 44 / 45   | `LegacyTerrain.uop`                   |
| 46 / 47   | `TerrainTexture.uop`                  |
| 48 / 49   | `SystemTextures.uop`                  |
| 50 / 51   | `Paperdoll.uop`                       |
| 52 / 53   | `Hues.uop`                            |
| 54 / 55   | `MultiCollection.uop`                 |
| 56 / 57   | `Shaders.uop`                         |
| 58 / 59   | `Waypoint.uop`                        |
| 60 / 61   | `LegacyTexture.uop`                   |
| 62 / 63   | `facets.uop`                          |
| 64 / 65   | `EnhancedTexture.uop` (registered but not shipped) |
| 66 / 67   | `GumpArtMask.uop`                     |

## Texture-folder file-location codes (from `FUN_0058e1a0`)

When a sprite/texture is requested by *short name* (not by hash), the EC asset manager normalises the path prefix to one of four code-tagged folders:

| Folder prefix         | Type code |
|-----------------------|----------:|
| `Textures\`           | 8         |
| `TileArtLegacy\`      | 22 (0x16) |
| `TileArtEnhanced\`    | 26 (0x1a) |
| `GumpArtMask\`        | 27 (0x1b) |

These codes do not appear in the hash convention itself, but they show up as the 6th field of an EC `SpriteTextureFileLocation` struct (i.e., `obj[5]` in the decompilation), which suggests how the engine dispatches I/O internally.
