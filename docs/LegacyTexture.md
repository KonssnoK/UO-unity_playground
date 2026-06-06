# LegacyTexture.uop

**Internal registry slot pair:** 60 / 61 (registered late in `FUN_00a70e5a`).

## What it contains

Classic-format Ultima Online statics art **re-encoded as DDS** (DXT-compressed) instead of the original ARGB1555 pixel runs. Land tiles (id < 0x4000) at 64×64 DXT5 = 4096 B + 128 B DDS header = 4224 B per file. Statics (id >= 0x4000) are typically 64×N DXT1/DXT5, up to a few KB each.

## Naming

```
build/tileartlegacy/{id:08}.dds
```

- Convention lowercased; forward slashes; Jenkins one-at-a-time hash.
- `id` is the classic UO static-art id (0 .. ~65000). The empirical maximum id seen in our archive is 46,091.
- Hashing the above with `ec.uop.hash_name` reproduces the entry hash bit-exactly.

Folder name `TileArtLegacy\` is confirmed in the binary at `s_TileArtLegacy\_00cb8a08` and identified as file-location code **0x16 (22)** by `FUN_0058e1a0`.

## Empirical coverage

- **Entries in archive:** 52,181.
- **Mapped by the pattern above:** 39,514 (75.7%).
- **Unmapped holdouts:** 12,667 entries with names not in Dictionary.dic and not matching this pattern. We don't yet know what they are; candidates include alt-format DDS variants, palette-coloured swatches, or special-purpose textures with literal names.

## Disassembly notes

- `FUN_0051af20` is the **legacy tile-art loader**: when a `TileArtId` cannot be fetched directly, it sprintfs the cache key `"%08d_LegacyTileArt"` and asks the texture manager for it.
- `FUN_0051e1d0` registers Lua hooks: `RequestLegacyTileArt`, `ReleaseLegacyTileArt`, mirroring the `RequestTileArt` pair used for the HD `Texture.uop`.

## Notes for the C# port

- Read DDS payloads directly via `Texture2D.FromStream` (FNA supports DXT1/3/5/BC4/BC5).
- Maintain a `(static_id) → UopEntry` map at startup; the UopArchive iterator and `hash_name()` give this for free.
- Render: blit at the entry's DDS dimensions; do **not** assume 44×44 — these are square 64×N atlases. Anchor offsets need to come from `tileart.uop` (`build/tileart/{id:08}.bin`).
- Trade-off: 25% of entries will fall back to the CC art path until the holdout pattern is decoded. Acceptable for first cut.
