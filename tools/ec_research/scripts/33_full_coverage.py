"""Combine Dictionary.dic with computed hashes from known patterns.

Patterns confirmed so far:
  build/tileartlegacy/{id:08}.dds
  build/worldart/{id:08}.dds
  build/animationframe/{body:06}/{action:02}.bin
  build/animationsequence/{id:08}.bin
  build/animationdefinition/{id:08}.bin
  build/terraintexture/{id:08}.dds
  build/terraindefinition/{id:08}.bin
  build/sectors/{id:08}.bin
  build/multicollection/{id:06}.bin
  build/paperdoll/{body:06}/{action:02}.bin
  build/tileart/{id:08}.bin       (from tileart.uop survey)
  build/effectdefinitioncollection/{id:08}.bin
  data/* literal files

Anything still missing after dict + computed-hash union gets reported.
"""
import os
import sys
import time
import pickle
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name
from ec.dic import load_dictionary

DIC = HERE / "Dictionary.dic"
EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16


# Patterns are (pattern, kind, range_spec) where kind is "1d" or "2d"
PATTERNS_1D = [
    "build/tileartlegacy/{0:08}.dds",
    "build/worldart/{0:08}.dds",
    "build/animationsequence/{0:08}.bin",
    "build/animationdefinition/{0:08}.bin",
    "build/terraintexture/{0:08}.dds",
    "build/terraindefinition/{0:08}.bin",
    "build/multicollection/{0:06}.bin",
    "build/effectdefinitioncollection/{0:08}.bin",
    "build/tileart/{0:08}.bin",
    "build/tileart/{0:08}.dds",
    "build/hues/{0:08}.bin",
    "build/sectors/{0:08}.bin",
]
PATTERNS_2D = [
    "build/animationframe/{0:06}/{1:02}.bin",
    "build/paperdoll/{0:06}/{1:02}.bin",
]


def _gen_1d(args):
    pat, lo, hi = args
    return [(hash_name(pat.format(i)), pat.format(i)) for i in range(lo, hi)]


def _gen_2d(args):
    pat, a_lo, a_hi, b_max = args
    out = []
    for a in range(a_lo, a_hi):
        for b in range(b_max):
            n = pat.format(a, b)
            out.append((hash_name(n), n))
    return out


def main():
    mapping = load_dictionary(DIC)
    mapping = {h: v for h, v in mapping.items() if v}
    print(f"Dictionary (named): {len(mapping)}")

    # Build parallel tasks to enumerate every hash from known patterns.
    PROBE_1D = 200_000
    CHUNK_1D = 10_000
    A_MAX = 3000
    CHUNK_2D = 100
    B_MAX = 80

    tasks_1d = []
    for pat in PATTERNS_1D:
        for s in range(0, PROBE_1D, CHUNK_1D):
            tasks_1d.append((pat, s, min(s + CHUNK_1D, PROBE_1D)))
    tasks_2d = []
    for pat in PATTERNS_2D:
        for a in range(0, A_MAX, CHUNK_2D):
            tasks_2d.append((pat, a, min(a + CHUNK_2D, A_MAX), B_MAX))

    print(f"workers={NCPU} 1D tasks={len(tasks_1d)}, 2D tasks={len(tasks_2d)}")
    computed: dict[int, str] = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU) as pool:
        for batch in pool.map(_gen_1d, tasks_1d, chunksize=4):
            for h, n in batch:
                computed.setdefault(h, n)
        for batch in pool.map(_gen_2d, tasks_2d, chunksize=4):
            for h, n in batch:
                computed.setdefault(h, n)
    print(f"computed {len(computed)} candidate names in {time.time()-t0:.1f}s")

    # Merge: dict wins (it has confirmed full paths including non-numeric ones)
    merged = dict(computed)
    merged.update(mapping)

    # Coverage per UOP
    archives = sorted(p.name for p in EC.glob("*.uop"))
    grand_total = grand_known = 0
    print()
    for arc_name in archives:
        try:
            arc = UopArchive(EC / arc_name)
        except Exception:
            continue
        total = len(arc.by_hash)
        known = sum(1 for h in arc.by_hash.keys() if h in merged)
        arc.close()
        grand_total += total
        grand_known += known
        pct = 100 * known / total if total else 0
        marker = "  " if pct >= 99 else ("* " if pct >= 50 else "**")
        print(f"  {marker}{arc_name:32s} {known:6d}/{total:6d} ({pct:5.1f}%)")
    pct = 100 * grand_known / grand_total
    print(f"\nGRAND TOTAL: {grand_known}/{grand_total} ({pct:.1f}%)")

    # Save merged catalog
    out_path = HERE.parent / "out" / "name_catalog.tsv"
    out_path.parent.mkdir(exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        f.write("hash\tname\tsource\n")
        for h, n in sorted(merged.items()):
            src = "dict" if h in mapping else "computed"
            f.write(f"{h:016X}\t{n}\t{src}\n")
    print(f"\nSaved catalog -> {out_path}  ({len(merged)} entries)")


if __name__ == "__main__":
    main()
