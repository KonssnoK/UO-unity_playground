"""Wider parallel chase: try variant suffixes for legacy holdouts and explore
gumpartmask with no-pad / different numeric formats.

Also try the 'icon%06d' family from the binary for GumpArtMask.
"""
import os
import sys
import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16

_REG: dict[str, set[int]] = {}
def _init(p):
    global _REG; _REG = pickle.loads(p)


def _scan(args):
    arc, pat, lo, hi = args
    s = _REG[arc]
    return arc, pat, sum(1 for i in range(lo, hi) if hash_name(pat.format(i)) in s)


def main():
    archives = ["LegacyTexture.uop", "Texture.uop", "GumpArtMask.uop"]
    reg = {}; sizes = {}
    for n in archives:
        a = UopArchive(EC / n); reg[n] = set(a.by_hash.keys()); sizes[n] = len(reg[n]); a.close()
    pickled = pickle.dumps(reg)

    folders = [
        "tileartlegacy", "tileartenhanced", "worldart", "worldart/ref",
        "gumpartmask", "gumpart", "icon",
        "tileart", "art", "legacyart", "ref",
        "landart", "landtexture", "terrainart",
    ]
    num_fmts = ["{0:08}", "{0:06}", "{0:04}", "{0:d}", "0{0:d}", "icon{0:06}"]
    suffixes = ["", "_disabled", "_legacy", "_legacytileart", "_tileart", "_texture", "_gumpart", "_l", "_e"]
    exts = [".dds", ".tga", ".png"]

    pats = []
    for f in folders:
        for nfmt in num_fmts:
            for sfx in suffixes:
                for e in exts:
                    pats.append(f"build/{f}/{nfmt}{sfx}{e}")
    # Also unprefixed numeric icon* style
    pats += [f"build/gumpartmask/icon{{0:06}}{sfx}.dds" for sfx in ["", "_disabled"]]
    pats += [f"build/gumpartmask/icon{{0:06}}{sfx}.tga" for sfx in ["", "_disabled"]]
    pats = sorted(set(pats))
    print(f"patterns: {len(pats)}")

    PROBE = 200_000
    CHUNK = 5_000

    tasks = []
    for arc in archives:
        for pat in pats:
            for s in range(0, PROBE, CHUNK):
                tasks.append((arc, pat, s, min(s + CHUNK, PROBE)))

    print(f"workers={NCPU} tasks={len(tasks)}")
    totals: dict[tuple[str, str], int] = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(pickled,)) as pool:
        for arc, pat, n in pool.map(_scan, tasks, chunksize=16):
            totals[(arc, pat)] = totals.get((arc, pat), 0) + n
    print(f"Done in {time.time()-t0:.1f}s")

    for arc in archives:
        rows = sorted(((p, n) for (a, p), n in totals.items() if a == arc), key=lambda kv: -kv[1])
        print(f"\n--- {arc} ({sizes[arc]}) top non-zero ---")
        for pat, n in rows[:8]:
            if n > 0:
                pct = 100 * n / sizes[arc]
                print(f"  ** {n:7d}/{sizes[arc]} ({pct:5.1f}%) :: {pat!r}")


if __name__ == "__main__":
    main()
