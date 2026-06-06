# LegacyTerrain.uop

**Internal registry slot pair:** 44 / 45.

## What it contains

4,108 small payloads, each is **a UTF-8 XML record** of the form:

```xml
<legacyTerrain>
    <terrainType id="10169" name="TerrainFallback" texMap="10169">
        <typeFlags>
            <wet />
            <surface />
        </typeFlags>
    </terrainType>
</legacyTerrain>
```

`id` and `texMap` are EC-internal terrain type ids (5-digit range observed: 10067 .. ~14000), **not** the CC land-tile id. `texMap` is the asset id that links into `TerrainDefinition.uop` records (which are keyed by the same 5-digit range — see "rec_id" in script 37).

`typeFlags` enumerates flags like `<wet/>`, `<surface/>`, etc. — these are the EC equivalent of the CC's `TileFlag` bits.

The class name `LegacyTerrainDefinition` appears at `s_LegacyTerrainDefinition_00ca1de8`.

## Naming

**Unknown.** The 4,108 entries are not in `Dictionary.dic` and don't match any `build/legacyterrain/...` brute-force pattern we tried. Plausible names (untested): something like `build/legacyterrain/<terrainType.id>.xml`, but neither lowercased numeric ids nor the explicit XML name strings hit.

**The naming barely matters for use.** The XML records contain their own id, so:

> You can iterate every entry in this UOP at load time, parse the XML, and build `Dictionary<int, TerrainType>` keyed on the parsed `id` attribute.

That is what the EC engine almost certainly does internally too.

## Connection to other archives

| Source                                       | Provides                                  |
|----------------------------------------------|-------------------------------------------|
| `data/gamedata/legacyterrainmap.csv`         | CC land tile id → EC `newId` (4,162 rows) |
| `LegacyTerrain.uop` (this file)              | EC terrain `id` → name + flags + texMap   |
| `TerrainDefinition.uop`                      | `rec_id` (= texMap) → binary parameters   |
| `TerrainTexture.uop`                         | 38 atlases the parameters sample          |

End-to-end chain: `cc_land_id → newId → terrainType (XML) → texMap → TerrainDefinition record → atlas slices`.

## Disassembly notes

- The factory class is `LegacyTerrainDefinition` — a string symbol but no decompiled body in our dump (no xrefs from the symbol; the class is likely instantiated via a vtable address rather than the string).
- The string `LegacyTerrain.uop` appears in the registry init (`FUN_00a70e5a`) confirming this file is loaded into slot pair 44/45.

## Notes for the C# port

- Parse all 4,108 XML records up front; build `Dictionary<int, TerrainType>` (about 4 KB of in-memory metadata).
- Wire this map into the `MapLoader` so when the world reports a CC land tile id, the renderer can resolve to the EC terrain type.
