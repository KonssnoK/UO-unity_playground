# tileart.uop

**Internal registry slot pair:** 14 / 15.

## What it contains

40,208 small binary records — one per **TileArtId** (CC static-art id). This is the EC equivalent of `tiledata.mul`'s static-tile section: it gives each item id its per-tile metadata (flags, height, anchor offset, hue, animation, multi-frame info, etc.).

**This file is required to render statics correctly** — without it, the EC DDS in `Texture.uop`/`LegacyTexture.uop` has no anchor offset and no z-height, so tiles will float, clip wrong, or stack incorrectly.

## Naming

```
build/tileart/{id:08}.bin
```

- **99.2% coverage** (39,881 / 40,208 entries via Dictionary.dic).
- `id` is the static art id, same key used by `LegacyTexture.uop` and `Texture.uop`.

## Payload format

**Decoded — see [tileart_VERIFIED.md](tileart_VERIFIED.md)** for the field-by-field
header layout. The trailing `TEXTURES()` block is a `TextureInfo` — the **same
struct** [`TerrainDefinition.uop`](TerrainDefinition.md) uses: each entry's
`textureIDX` is an **index into [`string_dictionary.uop`](string_dictionary.md)**
that resolves to a WorldArt/Legacy filename (the sprite reference is a string-dict
index, not a direct id). The original pre-decode plan is kept below for history:

1. Sample a handful with known semantics (e.g. id 0 = blank tile, id 0x4000+ = bottom of static range) and dump their bytes.
2. Cross-reference against the corresponding CC `StaticTile` record to identify common fields.
3. Run another Ghidra pass keyed on `"AVUOTileArtBinaryFactory"` / `"TileArt"` factory symbols to nail down the C++ struct.

## Disassembly notes

- The factory class for this UOP is referenced indirectly via `FUN_00a70e5a` line 548 (registers the file under slots 14/15). The actual *record parser* is one of the many anonymous `FUN_…` functions that consume `iStack_2c` after `FUN_00a70df8` returns; it would be reachable from the loader stub if we trace forward.
- A pending RE pass will resolve this. See "Gaps" in `README.md`.

## Notes for the C# port

- This is the missing piece for static rendering. Decode each record at startup into a `TileArtMetadata` struct: at minimum we need anchor offset (X, Y), height (z extent), and a flags bitmask. Hue and animation references come from the same record.
- Until the layout is fully decoded, fall back to CC `tiledata.mul` for metadata while loading the DDS pixels from EC. That gives ~95% visually-correct output (anchors are mostly the same between CC and EC); the wrong ~5% will be near-miss alignment issues that can be fixed in a follow-up pass.
