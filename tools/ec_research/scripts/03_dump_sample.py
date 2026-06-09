"""Dump readable samples of decompressed payloads to inspect formats."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = Path(__file__).resolve().parent.parent / "out"
OUT.mkdir(exist_ok=True)


def dump_text(name: str, count: int = 5):
    arc = UopArchive(EC / name)
    out = OUT / name.replace(".uop", "")
    out.mkdir(exist_ok=True)
    for i, (e, payload) in enumerate(arc.iter_decompressed()):
        if i >= count:
            break
        (out / f"{i:04}.bin").write_bytes(payload)
    print(f"  dumped {min(count, len(arc.entries))} entries from {name} -> {out}")
    arc.close()


def search_known_names(name: str, candidate_names: list[str]):
    arc = UopArchive(EC / name)
    seen = arc.by_hash
    print(f"\n--- searching {name} ({len(seen)} entries) for known candidate names ---")
    hits = 0
    for n in candidate_names:
        if hash_name(n) in seen:
            print(f"  HIT: {n!r}")
            hits += 1
    print(f"  total {hits}/{len(candidate_names)} hits")
    arc.close()


if __name__ == "__main__":
    dump_text("LegacyTerrain.uop", 5)
    dump_text("TerrainDefinition.uop", 3)
    dump_text("GameData.uop", 8)
    dump_text("AnimationDefinition.uop", 5)
    dump_text("AnimationSequence.uop", 3)

    # Try candidate names suggested by GameData references
    creature_names = [
        "Bear.dds", "Imp.dds", "Dragon_Asian.dds", "Bear_Polar.dds",
        "build/Animations/Bear.dds",
        "build/animations/Bear.dds",
        "Animations/Bear.dds",
        "animations/Bear.dds",
        "build/legacytexture/Bear.dds",
        "build/texture/Bear.dds",
    ]
    for arc_name in ["Texture.uop", "LegacyTexture.uop", "AnimationFrame1.uop",
                     "AnimationFrame2.uop", "AnimationFrame3.uop"]:
        search_known_names(arc_name, creature_names)
