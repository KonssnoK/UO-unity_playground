"""Targeted last sweep for GumpArtMask / LegacyTerrain / LegacyTexture holdouts."""
import os
import sys
import time
import pickle
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16

_HS: dict[str, set[int]] = {}
def _init(p):
    global _HS; _HS = pickle.loads(p)

def _scan(args):
    arc, pat, lo, hi = args
    s = _HS[arc]
    return arc, pat, sum(1 for i in range(lo, hi) if hash_name(pat.format(i)) in s)


def main():
    targets = ["GumpArtMask.uop", "LegacyTerrain.uop", "LegacyTexture.uop", "Texture.uop"]
    reg = {}; sizes = {}
    for n in targets:
        arc = UopArchive(EC / n); reg[n] = set(arc.by_hash.keys()); sizes[n] = len(reg[n]); arc.close()
    p = pickle.dumps(reg)

    folders_gump = [
        "gumpartlegacymul", "gumpartmask", "gumpart", "gumpartlegacy",
        "gump", "gumps", "uigumps",
    ]
    suffix_gump = ["", "_mask", "_alpha", "_a", "_m", "mask"]
    ext_gump = [".tga", ".dds", ".bin"]
    pats_gump = sorted({f"build/{f}/{{0:08}}{s}{e}" for f in folders_gump for s in suffix_gump for e in ext_gump})

    folders_terrain = [
        "legacyterrain", "legacyterraindata", "terraindefinition", "terraindata",
        "terrain", "legacy/terrain", "terraindef",
    ]
    pats_terrain = [f"build/{f}/{{0:08}}.bin" for f in folders_terrain]
    pats_terrain += [f"build/{f}/{{0:08}}.xml" for f in folders_terrain]
    pats_terrain += [f"build/{f}/{{0:08}}.dds" for f in folders_terrain]

    # LegacyTexture holdouts — perhaps different format
    pats_legacytex = [
        "build/tileartlegacy/{0:08}.tga",
        "build/tileartlegacymul/{0:08}.dds",
        "build/tileartlegacymul/{0:08}.tga",
        "build/tileartlegacy/{0:08}_alpha.dds",
        "build/tileartlegacy/{0:08}_mask.dds",
        "build/tileart/{0:08}.dds",
    ]
    # Texture holdouts
    pats_tex = [
        "build/worldart/{0:08}.tga",
        "build/worldartmask/{0:08}.dds",
        "build/worldart/{0:08}_alpha.dds",
        "build/worldart/{0:08}_a.dds",
        "build/worldart/{0:08}_mask.dds",
    ]

    PROBE = 200_000
    CHUNK = 10_000

    tasks = []
    for pat in pats_gump:
        for s in range(0, PROBE, CHUNK):
            tasks.append(("GumpArtMask.uop", pat, s, min(s + CHUNK, PROBE)))
    for pat in pats_terrain:
        for s in range(0, PROBE, CHUNK):
            tasks.append(("LegacyTerrain.uop", pat, s, min(s + CHUNK, PROBE)))
    for pat in pats_legacytex:
        for s in range(0, PROBE, CHUNK):
            tasks.append(("LegacyTexture.uop", pat, s, min(s + CHUNK, PROBE)))
    for pat in pats_tex:
        for s in range(0, PROBE, CHUNK):
            tasks.append(("Texture.uop", pat, s, min(s + CHUNK, PROBE)))

    print(f"workers={NCPU} tasks={len(tasks)}")
    totals: dict[tuple[str, str], int] = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(p,)) as pool:
        for arc, pat, n in pool.map(_scan, tasks, chunksize=8):
            totals[(arc, pat)] = totals.get((arc, pat), 0) + n
    print(f"done in {time.time()-t0:.1f}s")

    for target in targets:
        rows = sorted(((p, n) for (a, p), n in totals.items() if a == target), key=lambda kv: -kv[1])
        print(f"\n{target} ({sizes[target]}):")
        any_hit = False
        for pat, n in rows[:6]:
            if n > 0:
                any_hit = True
                pct = 100 * n / sizes[target]
                print(f"  HIT {n:6d}/{sizes[target]} ({pct:5.1f}%) :: {pat!r}")
        if not any_hit:
            print("  no hits")


if __name__ == "__main__":
    main()
