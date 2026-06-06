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

**Unrecoverable (and confirmed so).** Exhausted every avenue:
1. Brute-force over id / sequential-index / name-based patterns × many roots/exts — **no hits**.
2. The EC binary has **no `build/legacyterrain` format string** (only the registry name `LegacyTerrain.uop`).
3. **EC `Dictionary.dic`** — 2,715/4,108 of the archive's hashes are present but stored with `has_name=0` (no name string); the other 1,393 aren't in the dic at all.
4. **UOReader 0.8.7's `Dictionary.dic`** (larger: 190,581 entries / 141,216 named) — has **15 `build/` roots and none for legacy terrain**, and **0/4,108** of the archive's hashes resolve. UOReader 0.8.7 predates this archive.

So the names were stripped from every shipped dictionary and can't be reconstructed without the build-time name list. This is moot for use — records self-identify via their XML `id`.

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
