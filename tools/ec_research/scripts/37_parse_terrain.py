"""Parse LegacyTerrain XML + TerrainDefinition binary records + legacyterrainmap.csv.

Build a unified per-CC-land-tile mapping:
  legacy_id -> (ec_terrain_id, terrain_definition_record, ec_terrain_name)
"""
import csv
import struct
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = HERE.parent / "out" / "terrain"
OUT.mkdir(parents=True, exist_ok=True)


def parse_legacy_terrainmap():
    """Map CC legacy land tile id -> (newId, newSubType)."""
    arc = UopArchive(EC / "GameData.uop")
    data = arc.get_by_name("data/gamedata/legacyterrainmap.csv").decode("latin-1")
    arc.close()
    out = {}
    for row in csv.DictReader(data.splitlines()):
        out[int(row["legacyId"])] = (int(row["newId"]), int(row["newSubType"]))
    return out


def parse_legacy_terrain_xml():
    """Iterate ALL LegacyTerrain.uop entries (XML) and collect their data."""
    arc = UopArchive(EC / "LegacyTerrain.uop")
    out = []
    skipped = 0
    for entry, payload in arc.iter_decompressed():
        try:
            text = payload.decode("utf-8", errors="strict")
            root = ET.fromstring(text)
            for tt in root.findall("terrainType"):
                rec = {
                    "id": int(tt.get("id")),
                    "name": tt.get("name", ""),
                    "texMap": int(tt.get("texMap", -1)),
                    "flags": [c.tag for c in tt.find("typeFlags") or []],
                }
                out.append(rec)
        except Exception:
            skipped += 1
    arc.close()
    return out, skipped


def parse_terrain_definition():
    """Decompose each binary record (variable size) of TerrainDefinition.uop."""
    arc = UopArchive(EC / "TerrainDefinition.uop")
    rows = []
    for entry, payload in arc.iter_decompressed():
        # First DWORD is the asset id of this definition
        if len(payload) < 4:
            continue
        rec_id = struct.unpack_from("<I", payload, 0)[0]
        rows.append({
            "name_hash": entry.hash,
            "decompressed_size": entry.decompressed_size,
            "rec_id": rec_id,
            "head_hex": payload[:32].hex(),
        })
    arc.close()
    return rows


def main():
    print("=== legacyterrainmap.csv ===")
    lmap = parse_legacy_terrainmap()
    print(f"  {len(lmap)} legacy ids mapped to new EC terrain ids")
    print(f"  sample: 1 -> {lmap.get(1)}, 100 -> {lmap.get(100)}, 4096 -> {lmap.get(4096)}")

    print("\n=== LegacyTerrain.uop XML ===")
    terrain_types, skipped = parse_legacy_terrain_xml()
    print(f"  {len(terrain_types)} terrainType records  (skipped={skipped})")
    if terrain_types:
        print(f"  sample: {terrain_types[0]}")
        print(f"  sample: {terrain_types[100]}")
        # group by texMap usage to know how often each TerrainTexture is referenced
        by_texmap = defaultdict(int)
        for t in terrain_types:
            by_texmap[t["texMap"]] += 1
        print(f"  unique texMap values referenced: {len(by_texmap)}")
        print(f"  top 5 most-referenced texMaps: {sorted(by_texmap.items(), key=lambda kv: -kv[1])[:5]}")

    print("\n=== TerrainDefinition.uop ===")
    td = parse_terrain_definition()
    print(f"  {len(td)} records")
    print(f"  size hist (first 10): {[r['decompressed_size'] for r in td[:10]]}")
    print(f"  sample rec_ids: {[r['rec_id'] for r in td[:5]]}")

    # Save consolidated mapping
    out_csv = OUT / "land_chain.csv"
    with out_csv.open("w", encoding="utf-8") as f:
        f.write("legacyId,newId,newSubType\n")
        for k, (nid, sub) in sorted(lmap.items()):
            f.write(f"{k},{nid},{sub}\n")
    print(f"\nSaved land_chain.csv -> {out_csv}")

    out_xml = OUT / "terrain_types.csv"
    with out_xml.open("w", encoding="utf-8") as f:
        f.write("id,name,texMap,flags\n")
        for t in terrain_types:
            flags = "|".join(t["flags"])
            f.write(f"{t['id']},{t['name']},{t['texMap']},{flags}\n")
    print(f"Saved terrain_types.csv -> {out_xml}")


if __name__ == "__main__":
    main()
