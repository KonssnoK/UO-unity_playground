"""Canonical Enhanced-Client UOP naming patterns and file-format facts.

This is the **single source of truth** for the C# port. Update it here, then
regenerate ``out/uop_patterns.json`` (script 40_emit_patterns.py).

Conventions confirmed empirically:
  - Names are lowercased before hashing.
  - Forward slashes only (path separators inside the UOP).
  - Most archives use `build/<folder>/<index>.<ext>`. A few use 2-level nested
    `build/<folder>/<a:06>/<b:02>.bin` for body+action keying.
  - GameData/Data/etc. archives use literal `data/<path>.<ext>` names.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class UopSpec:
    archive: str                # filename of the UOP archive in the EC folder
    pattern: Optional[str]      # Python str.format pattern, or None if naming unknown
    kind: str                   # "1d" | "2d" | "literal" | "unknown"
    keys: tuple[str, ...] = ()  # human label per format slot (e.g. ("id",) or ("body","action"))
    coverage: float = 0.0       # fraction of entries we can name with this pattern
    payload: str = ""           # short description of payload format
    notes: str = ""             # additional remarks


SPECS: list[UopSpec] = [
    # --- statics / textures ---
    UopSpec("LegacyTexture.uop", "build/tileartlegacy/{0:08}.dds",
            "1d", ("id",), 0.757,
            payload="DXT-compressed DDS (64x64 DXT5 land tiles, 64xN DXT1/5 statics)",
            notes="13.2k entries (~25%) use a yet-unknown naming variant."),
    UopSpec("Texture.uop", "build/worldart/{0:08}.dds",
            "1d", ("id",), 0.960,
            payload="DXT DDS, high-res replacements (up to 256x256)"),
    UopSpec("tileart.uop", "build/tileart/{0:08}.bin",
            "1d", ("id",), 0.992,
            payload="Binary tile-art metadata (WORD/DWORD records)"),

    # --- gumps ---
    UopSpec("gumpartLegacyMUL.uop", "build/gumpartlegacymul/{0:08}.tga",
            "1d", ("id",), 1.0,
            payload="TGA images (classic-format gump art, re-packaged)"),
    UopSpec("GumpArtMask.uop", "build/gumpartmask/0{0:d}.dds",
            "1d", ("id_plus_1000000",), 1.0,
            payload="DDS mask textures used as alpha layers for legacy gumps.",
            notes="Disassembly (FUN_005960f0): name is built via "
                  "sprintf(\"Build\\\\GumpArtMask\\\\0%d.dds\", id + 1000000). "
                  "The leading '0' is LITERAL, then the unpadded id offset by +1,000,000. "
                  "Lowercased + forward slash for hashing."),

    # --- animations ---
    UopSpec("AnimationFrame1.uop", "build/animationframe/{0:06}/{1:02}.bin",
            "2d", ("body", "action"), 1.0,
            payload="AMOU-magic frame data; 32-byte header then encoded atlas",
            notes="Header: u32 magic 'AMOU', u32 version=1, u32 dsize, u32 unk, "
                  "int16x4 anchor bbox, u16 width(=256), u16, u32 height(=40)."),
    UopSpec("AnimationFrame2.uop", "build/animationframe/{0:06}/{1:02}.bin",
            "2d", ("body", "action"), 1.0, payload="(same as AnimationFrame1)"),
    UopSpec("AnimationFrame3.uop", "build/animationframe/{0:06}/{1:02}.bin",
            "2d", ("body", "action"), 1.0, payload="(same)"),
    UopSpec("AnimationFrame4.uop", "build/animationframe/{0:06}/{1:02}.bin",
            "2d", ("body", "action"), 1.0, payload="(same)"),
    UopSpec("AnimationFrame5.uop", "build/animationframe/{0:06}/{1:02}.bin",
            "2d", ("body", "action"), 1.0, payload="(same)"),
    UopSpec("AnimationFrame6.uop", "build/animationframe/{0:06}/{1:02}.bin",
            "2d", ("body", "action"), 1.0, payload="(same)"),
    UopSpec("AnimationDefinition.uop", "build/animationdefinition/{0:08}.bin",
            "1d", ("id",), 1.0,
            payload="46- or 66-byte binary records per body (id + action table)"),
    UopSpec("AnimationSequence.uop", "build/animationsequence/{0:08}.bin",
            "1d", ("id",), 1.0,
            payload="2.4-2.5 KB binary per body (action-sequence table)"),
    UopSpec("Paperdoll.uop", "build/paperdoll/{0:06}/{1:02}.bin",
            "2d", ("id", "slot"), 1.0,
            payload="Paperdoll layer; only 2 entries in this build"),

    # --- terrain ---
    UopSpec("TerrainTexture.uop", "build/terraintexture/{0:08}.dds",
            "1d", ("id",), 1.0,
            payload="256x256 DXT DDS texture atlases (38 of them)"),
    UopSpec("TerrainDefinition.uop", "build/terraindefinition/{0:08}.bin",
            "1d", ("id",), 0.787,
            payload="Variable-size binary records keyed by asset id (first DWORD)"),
    UopSpec("LegacyTerrain.uop", None,
            "unknown", (), 0.0,
            payload="UTF-8 XML records `<legacyTerrain><terrainType id name texMap>`",
            notes="4108 entries, naming not in dict; payload IS the metadata so the "
                  "name might just not matter for usage — iterate all and key by id."),

    # --- map sectors ---
    UopSpec("facet0.uop", "build/sectors/facet_00/{0:08}.bin",
            "1d", ("sector",), 1.0, payload="Per-sector map data (binary)"),
    UopSpec("facet1.uop", "build/sectors/facet_01/{0:08}.bin",
            "1d", ("sector",), 1.0, payload="(same per-facet pattern)"),
    UopSpec("facet2.uop", "build/sectors/facet_02/{0:08}.bin",
            "1d", ("sector",), 1.0, payload="(same)"),
    UopSpec("facet3.uop", "build/sectors/facet_03/{0:08}.bin",
            "1d", ("sector",), 1.0, payload="(same)"),
    UopSpec("facet4.uop", "build/sectors/facet_04/{0:08}.bin",
            "1d", ("sector",), 1.0, payload="(same)"),
    UopSpec("facet5.uop", "build/sectors/facet_05/{0:08}.bin",
            "1d", ("sector",), 1.0, payload="(same)"),
    UopSpec("facet0x.uop", "build/sectors/facet_00/{0:08}.bin",
            "1d", ("sector",), 1.0, payload="(same; 'x' variant = patches)"),
    UopSpec("facet1x.uop", "build/sectors/facet_01/{0:08}.bin",
            "1d", ("sector",), 1.0),
    UopSpec("facet2x.uop", "build/sectors/facet_02/{0:08}.bin",
            "1d", ("sector",), 1.0),
    UopSpec("facet5x.uop", "build/sectors/facet_05/{0:08}.bin",
            "1d", ("sector",), 1.0),

    # --- other ---
    UopSpec("MultiCollection.uop", "build/multicollection/{0:06}.bin",
            "1d", ("id",), 1.0,
            payload="Multi-item collection (housing, etc.)"),
    UopSpec("EffectDefinitionCollection.uop", "build/effectdefinitioncollection/{0:08}.bin",
            "1d", ("id",), 0.993),
    UopSpec("Hues.uop", "data/definitions/hues/hue{0:04}.bmp",
            "1d", ("hue",), 1.0,
            payload="Hue palette images",
            notes="Naming uses 4-digit pad, NOT 8; lowercase as always."),
    UopSpec("LocalizedStrings.uop", "data/localizedstrings/<literal>",
            "literal", (), 1.0,
            payload="Localized string files by language code"),
    UopSpec("MainMisc.uop", "data/<literal>",
            "literal", (), 0.75,
            payload="Misc loose data files (assetmap.xml, wearables.xml, speech.csv)"),
    UopSpec("string_dictionary.uop", "build/stringdictionary/string_dictionary.bin",
            "literal", (), 1.0),
    UopSpec("waypoint.uop", "build/sectors/waypoint.bin",
            "literal", (), 1.0),
    UopSpec("facets.uop", None, "unknown", (), 0.0,
            notes="7 entries, no dict matches; relate to facet manifests."),

    # --- partially / mostly literal ---
    UopSpec("Audio.uop", "data/audio/{sounds|music}/<name>",
            "literal", (), 0.413,
            payload="WAV/MP3 audio assets",
            notes="~58% missing from dict — names follow data/audio/sounds/* and "
                  "data/audio/music/* with mixed audio_filelist.csv lookups."),
    UopSpec("EffectTexture.uop", "data/effects/<literal>",
            "literal", (), 0.283,
            payload="Effect textures (sparkles, glows, etc.)"),
    UopSpec("Interface.uop", "data/interface/<literal>",
            "literal", (), 0.125,
            payload="UI textures, fonts, icons"),
    UopSpec("Shaders.uop", "data/shaders/<literal>",
            "literal", (), 0.333),
    UopSpec("SystemTextures.uop", "data/systemtextures/<literal>",
            "literal", (), 0.143),
    UopSpec("GameData.uop", "data/gamedata/<literal>.csv",
            "literal", (), 0.671,
            payload="CSV tables: mobart, legacyterrainmap, legacycontainers, "
                    "abilities, skilldata, weaponability, bugreport, and many "
                    "char-customization tables (TileArtId-keyed)."),
]


# Convenience: known GameData CSVs that drive the EC↔CC bridge.
GAMEDATA_CRITICAL_CSVS = {
    "legacyterrainmap.csv": "Maps CC land-tile-id -> (newId, newSubType) where "
                            "newId indexes into LegacyTerrain.uop terrainType records.",
    "mobart.csv":           "Maps BodyType -> '<name>.dds' filename (mob anim texture).",
    "legacycontainers.csv": "Maps gumpId -> (left,top,right,bottom,name) for container "
                            "UI bounds.",
}


# Hash convention reminder
HASH_CONVENTION = """
EC uses Jenkins One-At-A-Time (UO variant) over ASCII bytes.
Inputs MUST be lowercased and use forward slashes. The C# implementation
already lives in src/ClassicUO.IO/UOFileUop.cs::CreateHash — port the input
normalization, not the hash itself.
"""


# In-memory layout of an EC tile-art object (from Ghidra, FUN_0051a840).
# Populated at runtime from a parsed tileart.uop record.
TILEART_RUNTIME_STRUCT = """
struct EcTileArt {
    float x0;                  // bounds min X
    float y0;                  // bounds min Y
    float x1;                  // bounds max X (width  = x1 - x0)
    float y1;                  // bounds max Y (height = y1 - y0)
    float pixels_x_offset;     // anchor X within the texture
    float pixels_y_offset;     // anchor Y within the texture
    // ...handle / interface pointers follow at offset >= 24
};
"""


# File-location codes discovered via FUN_0058e1a0 (texture file-location classifier).
TEXTURE_FOLDER_CODES = {
    "Textures\\":        8,
    "TileArtLegacy\\":  22,   # 0x16
    "TileArtEnhanced\\": 26,   # 0x1a
    "GumpArtMask\\":    27,   # 0x1b
}


# Numeric registration slots from FUN_00a70e5a — each UOP gets two consecutive ids.
UOP_REGISTRY_SLOTS = [
    ("facet0.uop",                       (0, 1)),
    ("facet1.uop",                       (2, 3)),
    ("facet2.uop",                       (4, 5)),
    ("facet3.uop",                       (6, 7)),
    ("facet4.uop",                       (8, 9)),
    ("facet5.uop",                       (10, 11)),
    ("facet6.uop",                       (12, 13)),  # not shipped
    ("tileart.uop",                      (14, 15)),
    ("string_dictionary.uop",            (16, 17)),
    ("AnimationDefinition.uop",          (18, 19)),
    ("TerrainDefinition.uop",            (20, 21)),
    ("EffectDefinitionCollection.uop",   (22, 23)),
    ("AnimationSequence.uop",            (24, 25)),
    ("Texture.uop",                      (26, 27)),
    ("Audio.uop",                        (28, 29)),
    ("EffectTexture.uop",                (30, 31)),
    ("LocalizedStrings.uop",             (32, 33)),
    ("TerrainChunk.uop",                 (34, 35)),
    ("RadarMapTexture.uop",              (36, 37)),
    ("Interface.uop",                    (38, 39)),
    ("GameData.uop",                     (40, 41)),
    ("MainMisc.uop",                     (42, 43)),
    ("LegacyTerrain.uop",                (44, 45)),
    ("TerrainTexture.uop",               (46, 47)),
    ("SystemTextures.uop",               (48, 49)),
    ("Paperdoll.uop",                    (50, 51)),
    ("Hues.uop",                         (52, 53)),
    ("MultiCollection.uop",              (54, 55)),
    ("Shaders.uop",                      (56, 57)),
    ("Waypoint.uop",                     (58, 59)),
    ("LegacyTexture.uop",                (60, 61)),
    ("facets.uop",                       (62, 63)),
    ("EnhancedTexture.uop",              (64, 65)),  # registered but not shipped
    ("GumpArtMask.uop",                  (66, 67)),
]
