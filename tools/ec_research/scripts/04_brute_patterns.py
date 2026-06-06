"""Parallel brute-force of hash naming patterns for unmatched UOP archives.

Strategy:
  - Build a Cartesian grid of plausible patterns (prefix x folder x sep x numfmt x ext).
  - For each archive, fan out (pattern, range-shard) work items to a process pool.
  - A worker hashes its range and intersects against the archive's hash set.
  - Anything above a small threshold is reported.

The hash is pure Python int math, but on 32 logical cores we can probe billions
of names in reasonable time.
"""
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


# Worker globals (set per-process)
_HASH_SET: set[int] = set()


def _init_worker(hash_set_pickle: bytes):
    import pickle
    global _HASH_SET
    _HASH_SET = pickle.loads(hash_set_pickle)


def _probe_chunk(args):
    pat, start, stop = args
    hits = 0
    for i in range(start, stop):
        if hash_name(pat.format(i)) in _HASH_SET:
            hits += 1
    return pat, hits


def parallel_probe(arc_name: str, patterns: list[str], probe_max: int, report_thresh: int):
    arc = UopArchive(EC / arc_name)
    hash_set = set(arc.by_hash.keys())
    arc.close()
    print(f"\n=== {arc_name} ({len(hash_set)} entries, probing {len(patterns)} patterns x [0,{probe_max})) ===")

    import pickle
    pickled = pickle.dumps(hash_set)
    # Shard: per (pattern, range_chunk) where chunk size keeps tasks balanced
    chunk = max(2_000, probe_max // (NCPU * 2))
    tasks = []
    for pat in patterns:
        for s in range(0, probe_max, chunk):
            tasks.append((pat, s, min(s + chunk, probe_max)))

    totals: dict[str, int] = {p: 0 for p in patterns}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init_worker, initargs=(pickled,)) as pool:
        for pat, hits in pool.map(_probe_chunk, tasks, chunksize=8):
            totals[pat] += hits
    dt = time.time() - t0

    for pat, hits in sorted(totals.items(), key=lambda kv: -kv[1]):
        if hits >= report_thresh:
            print(f"  HITS {hits}/{len(hash_set)}: {pat!r}")
    print(f"  done in {dt:.1f}s")


PREFIXES = ["build/", ""]
NUM_FMTS = ["{0:08}", "{0:07}", "{0:06}", "{0:05}", "{0:04}", "{0}", "{0:08x}", "{0:08X}", "{0:x}", "{0:X}"]
EXTS = [".dds", ".tga", ".bin", ".dat", ".png", ".raw", ".tex", ".tex2", ".gfx", ""]


def grid(folders, exts=EXTS, num_fmts=NUM_FMTS, prefixes=PREFIXES):
    pats = []
    for p in prefixes:
        for f in folders:
            for n in num_fmts:
                for ext in exts:
                    pats.append(f"{p}{f}/{n}{ext}")
    return pats


if __name__ == "__main__":
    fold_legacytex = [
        "legacytexture", "LegacyTexture", "legacy_texture", "legacytex",
        "legacyart", "legacyArt", "legacyarts", "art", "tex", "texture",
        "legacy/texture",
    ]
    fold_texture = [
        "texture", "Texture", "tex", "hd", "hdtexture", "hires", "newtexture",
        "textures", "art", "texture/hd",
    ]
    fold_anim = [
        "animationframe1", "AnimationFrame1", "animation_frame_1",
        "animationframe", "animationframes", "animation", "anim", "frame",
        "animations/1", "animation/1", "animationframe/1",
    ]

    parallel_probe("LegacyTexture.uop", grid(fold_legacytex), probe_max=70_000, report_thresh=1)
    parallel_probe("Texture.uop", grid(fold_texture), probe_max=20_000, report_thresh=1)
    parallel_probe("AnimationFrame1.uop", grid(fold_anim), probe_max=20_000, report_thresh=1)
