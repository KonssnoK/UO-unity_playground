"""Dump per-entry header bytes that sit between index and payload.

In UOFileUop.FillEntries, the entry's `offset` is added with `headerLength` to
skip past per-entry header bytes. If EC embedded literal filenames in those
headers, we recover the naming convention for free.
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, UOP_MAGIC


def re_read_with_headers(path):
    """Re-read UOP and capture per-entry headerLength too."""
    fh = open(path, 'rb')
    fh.seek(0)
    magic, version, _ts, next_block, _bs, _ch = struct.unpack("<IIIqIi", fh.read(28))
    assert magic == UOP_MAGIC
    entries = []
    fh.seek(next_block)
    while True:
        (filesCount,) = struct.unpack("<i", fh.read(4))
        (next_block,) = struct.unpack("<q", fh.read(8))
        for _ in range(filesCount):
            off, hl, csize, dsize, h, _dh, flag = struct.unpack("<qiiiQIh", fh.read(34))
            if off == 0:
                continue
            entries.append((off, hl, csize, dsize, h, flag))
        if next_block == 0:
            break
        fh.seek(next_block)
    return fh, entries


def dump_header(path: Path, n: int = 5):
    print(f"\n=== {path.name} ===")
    fh, entries = re_read_with_headers(path)
    for i in range(min(n, len(entries))):
        off, hl, csize, dsize, h, flag = entries[i]
        fh.seek(off)
        header = fh.read(hl) if hl > 0 else b""
        # Try ascii
        safe_ascii = ''.join(chr(b) if 32 <= b < 127 else '.' for b in header)
        print(f"  [{i}] hl={hl} hash=0x{h:016X} flag={flag} dsize={dsize}")
        if header:
            print(f"      header hex: {header.hex(' ')}")
            print(f"      header chr: {safe_ascii}")
        else:
            print("      (no header)")
    fh.close()


EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

for name in [
    "LegacyTexture.uop", "Texture.uop", "AnimationFrame1.uop",
    "LegacyTerrain.uop", "TerrainTexture.uop", "TerrainDefinition.uop",
    "GameData.uop", "AnimationDefinition.uop",
]:
    dump_header(EC / name)
