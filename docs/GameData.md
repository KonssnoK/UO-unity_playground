# GameData.uop

**Internal registry slot pair:** 40 / 41.

## What it contains

79 small files; mostly **CSVs** plus one OLE/Excel blob (entry 13 — header `D0CF11E0...`, probably an internal bug-report template).

These are the EC equivalent of CC's `tiledata.mul` plus a lot of EC-specific game tables: character customization (faces, hairstyles, pant styles, shirt styles, shoes per race/gender), abilities, skills, professions, recipes, house placement gump rows, etc.

## Naming

Literal paths under `data/gamedata/`. 53 of 79 entries map to known names from `Dictionary.dic`; the remaining 26 named entries we recovered empirically by reading the CSV content.

Complete CSV inventory (from script `38_parse_gamedata.py` output):

| File                                              | Key columns                                        |
|---------------------------------------------------|----------------------------------------------------|
| `abilities.csv`                                   | id, name, reagents, wordPower, …                   |
| `alchemy.csv`, `blacksmith.csv`, `carpentry.csv`, `cooking.csv`, `fletcher.csv`, `glassblowing.csv`, `inscribe.csv`, `mapmaking.csv`, `masonry.csv`, `tailor.csv`, `tinker.csv` | Crafting recipes (60-column int rows) |
| `buffdata.csv`                                    | `ID, Define, IconId, ServerId`                     |
| `bugreport.csv`                                   | Bug-report categorisation                          |
| `charactergender.csv`, `characterhues.csv`, `characterrace.csv`, `charactertemplates.csv` | Character creation tables |
| `classic_housedata.csv`, `housesign*.csv`, `foundationstyle.csv`, `twostory_cust_housedata.csv`, `threestory_cust_housedata.csv` | Housing |
| `equipconv.csv`                                   | Equipment conversion table                         |
| `elfhairhues.csv`, `elfskinhues.csv`              | Elf hue ranges                                     |
| `face*.csv`, `female*.csv`, `male*.csv`           | Face / hair / pants / shirt / shoes by race+gender |
| `legacycontainers.csv`                            | `gumpId, left, top, right, bottom, name`           |
| `legacyterrainmap.csv`                            | `legacyId, newId, newSubType` (CC→EC bridge)       |
| `mobart.csv`                                      | `BodyType, Filename, Description`                  |
| `playerstats.csv`                                 | Skill data presentation                            |
| `resourcetype.csv`                                | Resource-gathering rules                           |
| `skilldata.csv`                                   | Skills tab metadata                                |
| `starting_wearables_*.csv`                        | Default outfits per race/gender                    |
| `weaponability.csv`                               | `objectId, primaryAbility, secondaryAbility, …`    |

Three particularly important CSVs for the C# port:

1. **`legacyterrainmap.csv`** — bridges CC land tile id → EC terrain id. See `LegacyTerrain.md`.
2. **`mobart.csv`** — maps body id → animation filename (e.g. `1, Ogre.dds, ogre`). The filenames are **not** in any UOP we've inspected; mob animation lookups go through `AnimationDefinition`/`AnimationSequence` plus the AMOU frames.
3. **`legacycontainers.csv`** — gump container bounding rectangles for the CC UI bridge.

## Disassembly notes

The binary contains error messages of the form
`"ID [%d] exceeds limit range for data/gamedata/<name>.csv -- entry has been skipped."`
which is how we enumerated the CSV names without a fully populated dictionary.

## Notes for the C# port

- Load all CSVs at startup; build per-table `Dictionary<int, Record>` maps.
- Many table columns are `TileArtId` — they reference into `LegacyTexture.uop` / `Texture.uop` and the C# loader should be able to resolve them through the same Jenkins-hash lookup as the world art.
