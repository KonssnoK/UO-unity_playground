"""Triage tools/ghidra/ghidra_dump.json into per-topic markdown drops."""
import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DUMP = HERE.parent.parent / "ghidra" / "ghidra_dump.json"
DOCS = HERE.parent / "docs" / "_raw"
DOCS.mkdir(parents=True, exist_ok=True)

data = json.loads(DUMP.read_text(encoding="utf-8"))
print(f"strings: {data['matched_symbols_count']}  fns: {data['decompiled_function_count']}")

fns = {f["entry"]: f for f in data["decompiled_functions"]}
str_to_fns = data["string_to_referring_functions"]

# Group functions by their triggering strings (topic buckets).
TOPICS = {
    "tileart_legacy": ["TileArtLegacy", "%08d_LegacyTileArt", "tileartlegacy", "LegacyTileArt"],
    "tileart_enhanced": ["TileArtEnhanced", "%08d_TileArt", "WorldArt", "worldart", "tileartenhanced"],
    "gumpartmask": ["GumpArtMask", "gumpartmask", "GumpArtMaskData"],
    "terrain": ["Terrain", "AtlasTerrain", "GameTerrain", "UOStaticTerrain",
                "LegacyTerrain", "TerrainDefinition", "TerrainTexture",
                "UOTerrainCollision", "UOTerrainTexturingProperty",
                "UOWaterTerrainLayer", "UODefaultTerrainLayer", "UOBumpMapTerrainLayer"],
    "animation": ["MobAnim", "AnimationFrame", "AnimationLegacyFrameSet"],
    "sectors": ["Sector"],
    "shaders": ["MythicBaseShader", "MythicShader", "MythicDirectionalLight",
                "MythicPointLight", "MythicShadowGenerator", "MythicAmbientLight"],
}

# For each function: which topics does it belong to?
fn_topics: dict[str, set[str]] = defaultdict(set)
fn_triggers: dict[str, list[str]] = {}
for fn in data["decompiled_functions"]:
    triggers = fn["trigger_strings"]
    fn_triggers[fn["entry"]] = triggers
    for trig in triggers:
        for topic, kws in TOPICS.items():
            if any(k in trig for k in kws):
                fn_topics[fn["entry"]].add(topic)

# Stats
topic_counts = defaultdict(int)
for s in fn_topics.values():
    for t in s:
        topic_counts[t] += 1
print("\nFunctions per topic:")
for t, c in sorted(topic_counts.items(), key=lambda kv: -kv[1]):
    print(f"  {t:20s} {c}")

# Emit one .md per topic
def emit_topic(topic: str):
    rows = [(entry, fns[entry]) for entry, topics in fn_topics.items() if topic in topics]
    rows.sort(key=lambda kv: kv[0])
    out = DOCS / f"{topic}.md"
    with out.open("w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n")
        f.write(f"Auto-generated from `tools/ghidra/ghidra_dump.json`.\n\n")
        f.write(f"Functions discovered via xrefs from strings matching: "
                f"`{', '.join(TOPICS[topic])}`\n\n")
        f.write(f"Total: {len(rows)} unique decompiled functions.\n\n")
        f.write("---\n\n")
        for entry, fn in rows:
            f.write(f"## `{fn['name']}` @ {entry}\n\n")
            f.write(f"- **signature**: `{fn['signature']}`\n")
            f.write(f"- **triggered by strings**:\n")
            for t in fn.get("trigger_strings", []):
                f.write(f"  - `{t}`\n")
            f.write("\n```c\n")
            f.write(fn["decompiled"])
            f.write("```\n\n---\n\n")
    print(f"  wrote {out} ({len(rows)} fns)")

for topic in TOPICS:
    emit_topic(topic)

# Cross-reference index: for each interesting string, list functions
idx_path = DOCS / "_string_xref_index.md"
with idx_path.open("w", encoding="utf-8") as f:
    f.write("# String -> functions xref index\n\n")
    for s in sorted(str_to_fns.keys()):
        addrs = str_to_fns[s]
        if not addrs:
            continue
        f.write(f"- `{s}` -> {len(set(addrs))} fns: ")
        f.write(", ".join(f"`{a}`" for a in sorted(set(addrs))))
        f.write("\n")
print(f"  wrote {idx_path}")
