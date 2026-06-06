# Misc EC archives (containers / standard formats)

Short reference for the remaining `.uop` archives that are plain asset
containers or standard file formats — named, identified, no further decode
needed for the ClassicUO EC path.

| Archive | Naming | Entries | Format / contents |
|---------|--------|--------:|-------------------|
| **Paperdoll.uop** | `build/paperdoll/{body:06}/{action:02}.bin` | 2 | **AMOU** frames (same format as `AnimationFrame` — see [AnimationFrame_AMOU.md](AnimationFrame_AMOU.md)). Gargoyle paperdoll bodies. |
| **EffectTexture.uop** | `data/effects/{id:08}_{name}.nif` | 829 (323 named) | **Gamebryo NIF** files (3D effect meshes/textures). Referenced by `EffectDefinitionCollection`. |
| **SystemTextures.uop** | `data/systemtextures/{name}.tga` | 7 | TGA UI/system textures (e.g. `anim_missing2.tga`). |
| **MainMisc.uop** | `data/{name}` (e.g. `data/speech.csv`, `wearables.xml`) | 4 | CSV/XML game-data blobs. |
| **waypoint.uop** | `build/sectors/waypoint.bin` | 1 | Pathfinding waypoint graph (binary). |
| **Audio.uop** | (audio paths) | — | Sound bank blobs (~303 MB). Out of scope for rendering. |
| **Interface.uop** | (interface paths) | — | UI textures/layouts (~243 MB). |
| **gumpartLegacyMUL.uop** | `build/gumpartlegacy/{id:08}.dds` | — | Legacy gump art as DDS (~47 MB). EC counterpart to CC `gumpart`. |
| **LocalizedStrings.uop** | (cliloc) | — | Localized strings (cliloc equivalent, ~12 MB). |
| **Shaders.uop** | (shader paths) | — | HLSL/asm shader sources (`.vsh`/`.psh`). Some extracted in `scripts/92_extract_shaders.py`. |

## Notes
- All naming above is confirmed via the **UOReader 0.8.7 `Dictionary.dic`** (more
  complete than the shipped EC dic) and/or direct format magic.
- **Paperdoll** reuses the verified AMOU decoder — no separate work.
- **EffectTexture** is Gamebryo NIF (`"Gamebryo File Format, Version …"` magic);
  decoding NIF is a separate, large effort and only needed for HD world effects.
- The big art containers (`Audio`, `Interface`, `gumpartLegacyMUL`,
  `LocalizedStrings`) are standard blobs; ClassicUO uses the CC equivalents.
