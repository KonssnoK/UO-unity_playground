"""Parallel hunt for the remaining unmapped entries.

LegacyTexture: 13196 entries not yet matched. Texture: 990. GumpArtMask: all.

Strategy: cross-test every observed folder pattern against every still-incomplete
archive, plus a 2D layout for GumpArtMask (since it appears to be the only
remaining one with no naming match).
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
def _init_reg(p):
    global _REG; _REG = pickle.loads(p)


def _scan1d(args):
    arc, pat, lo, hi = args
    s = _REG[arc]
    return arc, pat, sum(1 for i in range(lo, hi) if hash_name(pat.format(i)) in s)


def _scan2d(args):
    arc, pat, a_lo, a_hi, b_max = args
    s = _REG[arc]
    return arc, pat, sum(1 for a in range(a_lo, a_hi) for b in range(b_max) if hash_name(pat.format(a, b)) in s)


def main():
    archives = ["LegacyTexture.uop", "Texture.uop", "GumpArtMask.uop"]
    reg = {}; sizes = {}
    for n in archives:
        a = UopArchive(EC / n); reg[n] = set(a.by_hash.keys()); sizes[n] = len(reg[n]); a.close()
    pickled = pickle.dumps(reg)

    # Folder candidates pulled from binary strings + a wider net.
    folders = [
        "tileartlegacy", "tileartenhanced", "worldart", "worldart/ref",
        "gumpartmask", "gumpart", "systemtextures", "textures",
        "effecttexture", "paperdoll", "radarmaptexture", "interface",
        "tileart", "art", "legacyart", "ref",
        # combine known prefix with token suffixes
    ]
    num_fmts = ["{0:08}", "{0:d}", "{0:06}", "{0:04}"]
    exts = [".dds", ".tga", ".bin"]
    pats_1d = sorted({f"build/{f}/{n}{e}" for f in folders for n in num_fmts for e in exts})
    print(f"1D patterns: {len(pats_1d)}")

    PROBE = 200_000
    CHUNK = 5_000

    tasks = []
    for arc in archives:
        for pat in pats_1d:
            for s in range(0, PROBE, CHUNK):
                tasks.append((arc, pat, s, min(s + CHUNK, PROBE)))

    # Also 2D for GumpArtMask in case it's nested
    pats_2d = [
        "build/gumpartmask/{0:06}/{1:02}.dds",
        "build/gumpartmask/{0:04}/{1:04}.dds",
        "build/gumpart/{0:06}/{1:02}.dds",
    ]
    tasks2d = []
    for arc in archives:
        for pat in pats_2d:
            for a in range(0, 3000, 50):
                tasks2d.append((arc, pat, a, min(a + 50, 3000), 80))

    print(f"workers={NCPU} 1D tasks={len(tasks)} 2D tasks={len(tasks2d)}")
    totals: dict[tuple[str, str], int] = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init_reg, initargs=(pickled,)) as pool:
        for arc, pat, n in pool.map(_scan1d, tasks, chunksize=8):
            totals[(arc, pat)] = totals.get((arc, pat), 0) + n
        for arc, pat, n in pool.map(_scan2d, tasks2d, chunksize=4):
            totals[(arc, pat)] = totals.get((arc, pat), 0) + n
    print(f"\nDone in {time.time()-t0:.1f}s")

    for arc in archives:
        print(f"\n--- {arc} ({sizes[arc]}) top hits ---")
        rows = sorted(((p, n) for (a, p), n in totals.items() if a == arc), key=lambda kv: -kv[1])
        for pat, n in rows[:6]:
            if n > 0:
                print(f"  ** {n:7d}/{sizes[arc]} :: {pat!r}")


if __name__ == "__main__":
    main()
