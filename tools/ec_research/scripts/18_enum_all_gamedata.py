"""Try to enumerate all 79 GameData entries by probing every printable string
from UOSA.exe as a potential key."""
import os
import re
import sys
import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16

# Build a master pool of strings from both executables and selected UOPs.
data = (EC / "UOSA.exe").read_bytes() + (EC / "UOSA_TC.exe").read_bytes()
strings = sorted({m.decode('latin-1') for m in re.findall(rb"[\x20-\x7E]{4,}", data)})
print(f"unique strings: {len(strings)}")

# Also include lowercased and add some path variants
variants: set[str] = set()
for s in strings:
    if len(s) < 4 or len(s) > 200:
        continue
    variants.add(s)
    variants.add(s.lower())
    # Convert Windows-style to forward slash
    if "\\" in s:
        variants.add(s.replace("\\", "/"))
        variants.add(s.replace("\\", "/").lower())
print(f"variants: {len(variants)}")

variants_list = list(variants)


_HASH_SET: set[int] = set()
def _init(p):
    global _HASH_SET
    _HASH_SET = pickle.loads(p)


def _hash_batch(names):
    return [(n, hash_name(n)) for n in names if hash_name(n) in _HASH_SET]


def check_archive(arc_name: str):
    arc = UopArchive(EC / arc_name)
    seen = arc.by_hash
    arc.close()
    print(f"\n=== {arc_name} ({len(seen)} entries) ===")
    p = pickle.dumps(seen.keys() if False else set(seen.keys()))
    # Shard names into chunks
    chunk = 50_000
    shards = [variants_list[i:i+chunk] for i in range(0, len(variants_list), chunk)]
    t0 = time.time()
    hits: list[tuple[str, int]] = []
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(p,)) as pool:
        for results in pool.map(_hash_batch, shards):
            hits.extend(results)
    print(f"  scanned {len(variants_list)} names in {time.time()-t0:.1f}s, {len(hits)} hits")
    for n, h in hits[:60]:
        print(f"    {n!r}")


if __name__ == "__main__":
    for arc in ["GameData.uop", "LegacyTexture.uop", "Texture.uop",
                "AnimationFrame1.uop", "GumpArtMask.uop"]:
        check_archive(arc)
