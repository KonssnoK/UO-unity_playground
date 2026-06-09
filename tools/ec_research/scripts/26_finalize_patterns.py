"""Confirm every UOP naming pattern in a single fully-parallel sweep.

Dispatches all (archive, pattern, range-shard) tuples to a 32-worker pool so
the full discovery survey finishes in seconds, not minutes.
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

# Per-worker hash-set registry: arc_name -> set[int]
_REG: dict[str, set[int]] = {}


def _init_reg(pickled: bytes):
    global _REG
    _REG = pickle.loads(pickled)


def _scan1d(args):
    arc, pat, lo, hi = args
    s = _REG[arc]
    hits = 0
    for i in range(lo, hi):
        if hash_name(pat.format(i)) in s:
            hits += 1
    return arc, pat, hits


def _scan2d(args):
    arc, pat, a_lo, a_hi, b_max = args
    s = _REG[arc]
    hits = 0
    for a in range(a_lo, a_hi):
        for b in range(b_max):
            if hash_name(pat.format(a, b)) in s:
                hits += 1
    return arc, pat, hits


def main():
    archives = [
        "LegacyTexture.uop",
        "Texture.uop",
        "GumpArtMask.uop",
        "AnimationFrame1.uop",
        "AnimationFrame2.uop",
        "AnimationFrame3.uop",
        "AnimationFrame4.uop",
        "AnimationFrame5.uop",
        "AnimationFrame6.uop",
    ]

    # Load each archive's hash set
    reg: dict[str, set[int]] = {}
    sizes: dict[str, int] = {}
    for name in archives:
        a = UopArchive(EC / name)
        reg[name] = set(a.by_hash.keys())
        sizes[name] = len(reg[name])
        a.close()
    pickled = pickle.dumps(reg)

    # Build the task list
    PROBE_1D = 200_000
    CHUNK_1D = 5_000  # tuned to keep tasks balanced across 32 workers
    A_MAX = 3000
    B_MAX = 80
    CHUNK_2D = 50

    pats_1d: dict[str, list[str]] = {
        "LegacyTexture.uop": [
            "build/tileartlegacy/{0:08}.dds",
            "build/worldart/{0:08}.dds",
            "build/tileartenhanced/{0:08}.dds",
        ],
        "Texture.uop": [
            "build/worldart/{0:08}.dds",
            "build/tileartenhanced/{0:08}.dds",
            "build/tileartlegacy/{0:08}.dds",
            "build/worldart/ref/{0:08}.dds",
        ],
        "GumpArtMask.uop": [
            "build/gumpartmask/0{0:d}.dds",
            "build/gumpartmask/{0:08}.dds",
            "build/gumpartmask/{0:d}.dds",
            "build/gumpart/0{0:d}.dds",
            "build/gumpart/{0:08}.dds",
            "build/gumpartmask/0{0}.dds",
        ],
    }
    pats_2d_anim = "build/animationframe/{0:06}/{1:02}.bin"

    tasks_1d = []
    for arc, pats in pats_1d.items():
        for pat in pats:
            for s in range(0, PROBE_1D, CHUNK_1D):
                tasks_1d.append((arc, pat, s, min(s + CHUNK_1D, PROBE_1D)))

    tasks_2d = []
    for arc in archives:
        if not arc.startswith("AnimationFrame"):
            continue
        for s in range(0, A_MAX, CHUNK_2D):
            tasks_2d.append((arc, pats_2d_anim, s, min(s + CHUNK_2D, A_MAX), B_MAX))

    print(f"workers={NCPU} tasks_1d={len(tasks_1d)} tasks_2d={len(tasks_2d)}")
    t0 = time.time()
    totals: dict[tuple[str, str], int] = {}

    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init_reg, initargs=(pickled,)) as pool:
        # 1D and 2D are different shapes — submit separately, drain together
        for arc, pat, hits in pool.map(_scan1d, tasks_1d, chunksize=8):
            totals[(arc, pat)] = totals.get((arc, pat), 0) + hits
        for arc, pat, hits in pool.map(_scan2d, tasks_2d, chunksize=4):
            totals[(arc, pat)] = totals.get((arc, pat), 0) + hits

    dt = time.time() - t0
    print(f"\nDone in {dt:.1f}s\n")
    # Report best per archive
    by_arc: dict[str, list[tuple[str, int]]] = {}
    for (arc, pat), n in totals.items():
        by_arc.setdefault(arc, []).append((pat, n))

    for arc in archives:
        rows = sorted(by_arc.get(arc, []), key=lambda kv: -kv[1])
        if not rows:
            continue
        print(f"--- {arc} ({sizes[arc]} entries) ---")
        for pat, n in rows[:5]:
            pct = n / sizes[arc] * 100
            mark = "**" if n > 0 else "  "
            print(f"  {mark} {n:7d}/{sizes[arc]} ({pct:5.1f}%) :: {pat!r}")


if __name__ == "__main__":
    main()
