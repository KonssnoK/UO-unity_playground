"""Extend the probe range and try sibling-folder names for Texture.uop / GumpArtMask.uop."""
import os
import sys
import time
import pickle
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16

_HASH_SET: set[int] = set()
def _init(p):
    global _HASH_SET
    _HASH_SET = pickle.loads(p)

def _scan(args):
    pat, lo, hi = args
    hits = []
    for i in range(lo, hi):
        if hash_name(pat.format(i)) in _HASH_SET:
            hits.append(i)
    return pat, len(hits), hits[:5], hits[-5:]


def run(arc_name, patterns, probe_max):
    arc = UopArchive(EC / arc_name)
    hs = set(arc.by_hash.keys())
    arc.close()
    print(f"\n=== {arc_name} ({len(hs)} entries) probe to {probe_max} on {len(patterns)} patterns ===")
    p = pickle.dumps(hs)
    chunk = max(2000, probe_max // (NCPU * 2))
    tasks = [(pat, s, min(s + chunk, probe_max)) for pat in patterns for s in range(0, probe_max, chunk)]
    totals = {p_: [0, None, None] for p_ in patterns}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(p,)) as pool:
        for pat, n, first, last in pool.map(_scan, tasks, chunksize=8):
            totals[pat][0] += n
            if first and totals[pat][1] is None:
                totals[pat][1] = first
            if last:
                totals[pat][2] = last
    for pat, (n, first, last) in sorted(totals.items(), key=lambda kv: -kv[1][0]):
        if n > 0:
            print(f"  {n:7d}/{len(hs)} hits :: {pat!r}  first={first} last={last}")
    print(f"  ({time.time()-t0:.1f}s)")


legacy_pats = [
    "build/tileartlegacy/{0:08}.dds",
]
# Try sibling folders and various spellings for the enhanced UOP
enhanced_pats = [
    "build/tileart/{0:08}.dds",
    "build/tileartenhanced/{0:08}.dds",
    "build/tileartenh/{0:08}.dds",
    "build/enhancedtileart/{0:08}.dds",
    "build/tileart_enhanced/{0:08}.dds",
    "build/texture/{0:08}.dds",
    "build/enhancedtexture/{0:08}.dds",
    "build/tileartlegacy/{0:08}.dds",   # maybe Texture is just a subset of LegacyTexture
]
gump_pats = [
    "build/gumpartmask/{0:08}.dds",
    "build/gumpart/{0:08}.dds",
    "build/gumpartlegacy/{0:08}.dds",
    "build/gumpartmask/0{0:d}.dds",
    "build/gumpartmask/0{0}.dds",
]


if __name__ == "__main__":
    run("LegacyTexture.uop", legacy_pats, 200_000)
    run("Texture.uop", enhanced_pats, 200_000)
    run("GumpArtMask.uop", gump_pats, 200_000)
