"""Parse Dictionary.dic from MPE and map every UOP entry to its real name."""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

DIC = Path(r"C:\Users\konss\Desktop\Dictionary.dic")
EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def parse_dic(path: Path) -> dict[int, str]:
    data = path.read_bytes()
    assert data[:4] == b"DIC\0", data[:4]
    # Skip header: 11 bytes after magic (DIC\0 + 11 = offset 0x0F where first '01' marker begins)
    i = 0x0F
    out: dict[int, str] = {}
    bad_first = 0
    n_records = 0
    while i + 10 <= len(data):
        marker = data[i]
        if marker != 0x01:
            bad_first += 1
            i += 1
            continue
        length = data[i + 1]
        if length == 0 or i + 2 + length + 8 > len(data):
            break
        name = data[i + 2: i + 2 + length].decode('ascii', errors='replace')
        h = struct.unpack_from("<Q", data, i + 2 + length)[0]
        out[h] = name
        i += 2 + length + 8
        n_records += 1
    print(f"  parsed {n_records} records  (skipped={bad_first}, end offset=0x{i:X})")
    return out


def cover(arc_name: str, mapping: dict[int, str]):
    arc = UopArchive(EC / arc_name)
    total = len(arc.by_hash)
    matched = 0
    sample: list[str] = []
    hash_mismatches = 0
    for h, e in arc.by_hash.items():
        if h in mapping:
            matched += 1
            n = mapping[h]
            if hash_name(n) != h:
                hash_mismatches += 1
            if len(sample) < 5:
                sample.append(n)
    print(f"\n{arc_name}: {matched}/{total} ({100*matched/total:.1f}%) — hash-mismatch={hash_mismatches}")
    for s in sample:
        print(f"  e.g. {s!r}")
    arc.close()


if __name__ == "__main__":
    mapping = parse_dic(DIC)
    print(f"Dictionary entries (unique hashes): {len(mapping)}")
    sample_items = list(mapping.items())[:5]
    for h, n in sample_items:
        recomputed = hash_name(n)
        ok = "OK " if recomputed == h else "BAD"
        print(f"  {ok}  {n!r}  stored=0x{h:016X}  jenkins=0x{recomputed:016X}")

    for arc in [
        "LegacyTexture.uop", "Texture.uop", "GumpArtMask.uop",
        "AnimationFrame1.uop", "AnimationFrame2.uop",
        "Paperdoll.uop", "MultiCollection.uop", "Interface.uop",
        "EffectTexture.uop", "MainMisc.uop",
        "SystemTextures.uop", "Hues.uop", "Shaders.uop",
        "TerrainDefinition.uop", "AnimationDefinition.uop",
    ]:
        try:
            cover(arc, mapping)
        except FileNotFoundError as e:
            print(f"{arc}: not found")
