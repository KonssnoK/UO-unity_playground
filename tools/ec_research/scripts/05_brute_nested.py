"""Try nested-directory and CC-compatible patterns for unmatched archives."""
from __future__ import annotations

import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16

_HASH_SET: set[int] = set()


def _init_worker(pickled: bytes):
    import pickle
    global _HASH_SET
    _HASH_SET = pickle.loads(pickled)


def _probe_2d(args):
    pat, a_start, a_stop, b_max = args
    hits = 0
    for a in range(a_start, a_stop):
        for b in range(b_max):
            if hash_name(pat.format(a, b)) in _HASH_SET:
                hits += 1
    return pat, hits


def _probe_1d(args):
    pat, start, stop = args
    hits = 0
    for i in range(start, stop):
        if hash_name(pat.format(i)) in _HASH_SET:
            hits += 1
    return pat, hits


def parallel_2d(arc_name: str, patterns: list[str], a_max: int, b_max: int, report_thresh: int = 1):
    arc = UopArchive(EC / arc_name)
    hash_set = set(arc.by_hash.keys())
    arc.close()
    print(f"\n=== {arc_name} ({len(hash_set)} entries; 2D probe {a_max}x{b_max} on {len(patterns)} patterns) ===")
    import pickle
    pickled = pickle.dumps(hash_set)
    chunk = max(50, a_max // (NCPU * 4))
    tasks = [(p, s, min(s + chunk, a_max), b_max) for p in patterns for s in range(0, a_max, chunk)]
    totals = {p: 0 for p in patterns}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init_worker, initargs=(pickled,)) as pool:
        for pat, hits in pool.map(_probe_2d, tasks, chunksize=4):
            totals[pat] += hits
    for pat, hits in sorted(totals.items(), key=lambda kv: -kv[1]):
        if hits >= report_thresh:
            print(f"  HITS {hits}/{len(hash_set)}: {pat!r}")
    print(f"  done in {time.time()-t0:.1f}s")


def parallel_1d(arc_name: str, patterns: list[str], probe_max: int, report_thresh: int = 1):
    arc = UopArchive(EC / arc_name)
    hash_set = set(arc.by_hash.keys())
    arc.close()
    print(f"\n=== {arc_name} ({len(hash_set)}; 1D probe to {probe_max} on {len(patterns)} patterns) ===")
    import pickle
    pickled = pickle.dumps(hash_set)
    chunk = max(2000, probe_max // (NCPU * 2))
    tasks = [(p, s, min(s + chunk, probe_max)) for p in patterns for s in range(0, probe_max, chunk)]
    totals = {p: 0 for p in patterns}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init_worker, initargs=(pickled,)) as pool:
        for pat, hits in pool.map(_probe_1d, tasks, chunksize=8):
            totals[pat] += hits
    for pat, hits in sorted(totals.items(), key=lambda kv: -kv[1]):
        if hits >= report_thresh:
            print(f"  HITS {hits}/{len(hash_set)}: {pat!r}")
    print(f"  done in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    # CC-style names against EC bundles (maybe they kept CC paths)
    cc_compat = [
        "build/artlegacymul/{0:08}.tga",
        "build/artLegacyMUL/{0:08}.tga",
        "build/artlegacymul/{0:08}.dds",
        "build/art/{0:08}.dds",
        "build/art/{0:08}.tga",
        "build/legacy/{0:08}.dds",
        "build/legacy/art/{0:08}.dds",
    ]
    parallel_1d("LegacyTexture.uop", cc_compat, 70_000)
    parallel_1d("Texture.uop", cc_compat, 20_000)

    # 2D nested patterns
    nested_static = [
        "build/legacytexture/{0:06}/{1:02}.dds",
        "build/legacytexture/{0:04}/{1:04}.dds",
        "build/legacytexture/{0:03}/{1:05}.dds",
        "build/legacytexture/{0}/{1}.dds",
        "build/texture/{0:06}/{1:02}.dds",
        "build/artlegacymul/{0:06}/{1:02}.tga",
    ]
    parallel_2d("LegacyTexture.uop", nested_static, a_max=2000, b_max=100)
    parallel_2d("Texture.uop", nested_static, a_max=2000, b_max=100)

    # Animations: legacy convention is build/animationlegacyframe/{body:06}/{action:02}.bin
    nested_anim = [
        "build/animationframe1/{0:06}/{1:02}.bin",
        "build/animationframe1/{0:06}/{1:02}.amou",
        "build/animationframe/1/{0:06}/{1:02}.bin",
        "build/animationframe/{0:06}/{1:02}/1.bin",
        "build/animation/{0:06}/{1:02}.bin",
        "build/animationsequence/{0:06}/{1:02}.bin",
        "build/animation/frame1/{0:06}/{1:02}.bin",
        "build/anim/{0:06}/{1:02}.bin",
    ]
    parallel_2d("AnimationFrame1.uop", nested_anim, a_max=2000, b_max=80)
