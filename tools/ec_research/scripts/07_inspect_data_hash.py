"""Inspect the per-entry data_hash field in UOP indices.

Each UOP entry has both a name-hash and a data_hash. We've been ignoring
data_hash. If EC stuffed asset IDs there, it'd be visible as a small numeric
range with structure (e.g. monotonic per-file).
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def read_data_hashes(path: Path):
    fh = open(path, 'rb')
    magic, version, _ts, next_block, _bs, _ch = struct.unpack("<IIIqIi", fh.read(28))
    assert magic == 0x50594D
    out = []
    fh.seek(next_block)
    while True:
        (filesCount,) = struct.unpack("<i", fh.read(4))
        (next_block,) = struct.unpack("<q", fh.read(8))
        for _ in range(filesCount):
            off, hl, csize, dsize, h, dh, flag = struct.unpack("<qiiiQIh", fh.read(34))
            if off == 0: continue
            out.append((h, dh, csize, dsize))
        if next_block == 0: break
        fh.seek(next_block)
    fh.close()
    return out


EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

for name in ["LegacyTexture.uop", "Texture.uop", "AnimationFrame1.uop",
             "LegacyTerrain.uop", "TerrainTexture.uop", "TerrainDefinition.uop",
             "AnimationDefinition.uop", "AnimationSequence.uop"]:
    rows = read_data_hashes(EC / name)
    print(f"\n=== {name}: {len(rows)} entries ===")
    dhs = [r[1] for r in rows]
    print(f"  data_hash range: min=0x{min(dhs):X} max=0x{max(dhs):X}  uniq={len(set(dhs))}")
    print(f"  first 8 (name_hash, data_hash, csize, dsize):")
    for r in rows[:8]:
        print(f"    name=0x{r[0]:016X}  data=0x{r[1]:08X}  csize={r[2]}  dsize={r[3]}")
