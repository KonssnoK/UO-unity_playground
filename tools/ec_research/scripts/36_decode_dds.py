"""Decode a handful of DDS payloads from each texture UOP to PNG, in parallel."""
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

from PIL import Image  # type: ignore

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = HERE.parent / "out" / "dds_samples"
OUT.mkdir(parents=True, exist_ok=True)
NCPU = os.cpu_count() or 16


def dump_dds(payload: bytes, dest_dds: Path, dest_png: Path):
    dest_dds.write_bytes(payload)
    try:
        img = Image.open(BytesIO(payload))
        img.load()
        img.save(dest_png)
        return dest_png.name, img.size, img.mode
    except Exception as ex:
        return dest_png.name, None, f"ERR: {ex}"


def _process(args):
    arc_name, pattern, ids = args
    arc = UopArchive(EC / arc_name)
    out_dir = OUT / arc_name.replace(".uop", "")
    out_dir.mkdir(exist_ok=True)
    results = []
    for i in ids:
        name = pattern.format(i)
        h = hash_name(name)
        if h not in arc.by_hash:
            continue
        payload = arc.read(arc.by_hash[h])
        dest_dds = out_dir / f"{i:08}.dds"
        dest_png = out_dir / f"{i:08}.png"
        n, size, mode = dump_dds(payload, dest_dds, dest_png)
        results.append((arc_name, i, size, mode))
    arc.close()
    return results


def main():
    samples = [
        ("LegacyTexture.uop", "build/tileartlegacy/{0:08}.dds", list(range(0, 8))),
        ("Texture.uop", "build/worldart/{0:08}.dds", list(range(0, 16))),
        ("TerrainTexture.uop", "build/terraintexture/{0:08}.dds", list(range(0, 4))),
    ]
    print(f"workers={NCPU}")
    with ProcessPoolExecutor(max_workers=NCPU) as pool:
        for batch in pool.map(_process, samples):
            for arc, i, size, mode in batch:
                print(f"  {arc}[{i:5d}]  size={size}  mode={mode}")
    print(f"\nDumped to {OUT}")


if __name__ == "__main__":
    main()
