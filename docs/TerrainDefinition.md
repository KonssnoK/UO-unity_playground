# TerrainDefinition.uop

**Internal registry slot pair:** 20 / 21.

## What it contains

249 binary records of variable size (~50–200 B each). Each record begins with the **EC terrain id** as the first DWORD, then a series of int/float fields that parameterise the `AtlasTerrainShader` for that terrain type.

Empirical dump of `TerrainDefinition[0]` head:
```
2C CD 01 00   <- 0x0001CD2C = 118572  (rec_id, EC terrain id)
00 00 00 00   00 00 00 00   00 00 00 00   00 00 00 00
02 00 00 00   00 00 00 00   02 00 00 00   00 00 01 00   (flags / 2-component vec / etc)
02 00 00 00   01 00 00 00   00 00 00 00   40 00 00 00   (more params; 0x40 = 64)
02 00 00 00   01 00 2D CD   01 00 03 2E   CD 01 00 00   (struct references to ids 0x0001CD2D, 0x0001CD2E)
00 00 00 41   ...                                       (0x41000000 = 8.0f single-precision)
...
```

Pattern: a header DWORD (`rec_id`), then small typed fields, then **references to neighbouring rec_ids** (the chained 0x0001CD2C, 2D, 2E, 2F sequence in the sample). The neighbour-ids form an adjacency / blend graph used by the atlas terrain shader.

Decompressed sizes for the first 10 records: 154, 170, 171, 155, 155, 138, 155, 138, 138, 138 bytes — small, fixed-shape records with optional extensions.

## Naming

```
build/terraindefinition/{id:08}.bin
```

- **78.7% coverage** (196 of 249 entries via Dictionary.dic).
- The 53 unknown-named entries probably use ids outside the simple 0..N range — possibly *also* with a +1,000,000 offset for shader/effect-related terrain definitions (same trick as `GumpArtMask`).

## Disassembly notes

- The factory class is `AVUOTerrainDefinitionBinaryFactory` (symbol `s_TerrainDefinition_00ca1e78` is the type name; xrefs are limited because the factory is instantiated via vftable).
- The shader that consumes this data is `UOStaticTerrainShader` (`s_UOStaticTerrainShader_00cb9610`); its render entry point is the function annotated at `00461bc0`. Reading it back-to-back with the data layout above is the right way to decode the binary record format.

## Notes for the C# port

- Parse each record at load time into a `TerrainDefinition` struct keyed by the first DWORD.
- Field layout still requires a careful read of `FUN_00461bc0` to nail down — the safe move is to dump the record interpreter once we name a few specific fields by tracing them through the shader inputs.
- Until the layout is fully decoded, treat this archive as opaque per-record byte blobs and supply them to the GPU as a constant-buffer block per chunk. The C# code can ship before the field-by-field decode is complete.
