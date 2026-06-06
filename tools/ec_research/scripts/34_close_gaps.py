"""Final gap-closing sweep using prefixes discovered in the dictionary itself."""
import os
import sys
import time
import pickle
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name
from ec.dic import load_dictionary

DIC = HERE / "Dictionary.dic"
EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16


def list_prefixes(mapping):
    """List directory prefixes seen in dictionary names."""
    c: Counter = Counter()
    for n in mapping.values():
        if not n:
            continue
        parts = n.split("/")
        # keep first 3 components if any
        for k in range(1, min(4, len(parts))):
            c["/".join(parts[:k]) + "/"] += 1
    return c


_HS: dict[str, set[int]] = {}
def _init(p):
    global _HS; _HS = pickle.loads(p)


def _scan(args):
    arc, pat, lo, hi = args
    s = _HS[arc]
    out = []
    for i in range(lo, hi):
        h = hash_name(pat.format(i))
        if h in s:
            out.append((i, pat.format(i)))
    return arc, pat, out


def _scan2d(args):
    arc, pat, a_lo, a_hi, b_max = args
    s = _HS[arc]
    hits = 0
    for a in range(a_lo, a_hi):
        for b in range(b_max):
            if hash_name(pat.format(a, b)) in s:
                hits += 1
    return arc, pat, hits


def main():
    mapping = load_dictionary(DIC)
    named = {h: v for h, v in mapping.items() if v}
    pref = list_prefixes(named)
    print("Top 30 prefixes in dictionary:")
    for p, c in pref.most_common(30):
        print(f"  {c:6d}  {p}")

    holdouts = [
        "GumpArtMask.uop",
        "gumpartLegacyMUL.uop",
        "LegacyTexture.uop",
        "LegacyTerrain.uop",
        "Texture.uop",
        "Audio.uop",
        "EffectTexture.uop",
        "Interface.uop",
        "Shaders.uop",
        "SystemTextures.uop",
        "GameData.uop",
        "MainMisc.uop",
    ]

    reg = {}
    sizes = {}
    for n in holdouts:
        try:
            arc = UopArchive(EC / n)
            reg[n] = set(arc.by_hash.keys())
            sizes[n] = len(reg[n])
            arc.close()
        except FileNotFoundError:
            pass
    pickled = pickle.dumps(reg)

    # Candidate patterns to test against the holdouts
    pats_1d = [
        # gump variants
        "build/gumpartmask/{0:08}.dds",
        "build/gumpartlegacymul/{0:08}.tga",
        "build/gumpartmask/{0:08}.tga",
        "build/gumpartmask/{0:08}.bin",
        "build/gumpart/{0:08}.dds",
        "build/gumpartlegacymul/{0:08}.dds",
        "build/gumpartlegacy/{0:08}.tga",
        "build/gumpartlegacy/{0:08}.dds",
        # legacy holdouts variants (.tga instead of .dds, or different folder)
        "build/tileartlegacy/{0:08}.tga",
        "build/tileartlegacy/{0:08}.bin",
        "build/landtexture/{0:08}.dds",
        "build/legacy/{0:08}.dds",
        # terrain holdouts
        "build/legacyterrain/{0:08}.bin",
        "build/legacyterrain/{0:08}.xml",
        "build/terraindata/{0:08}.bin",
        # texture holdouts
        "build/worldart/{0:08}.tga",
        "build/worldart/{0:08}.bin",
        "build/worldart/ref/{0:08}.dds",
        # audio
        "data/audio/sounds/{0:08}.wav",
        "data/audio/music/{0:08}.mp3",
        "data/audio/{0:08}.wav",
        # effect texture
        "data/effects/{0:08}.dds",
        "data/effects/{0:08}.tga",
        # system textures
        "data/systemtextures/{0:08}.tga",
    ]

    PROBE = 200_000
    CHUNK = 10_000
    tasks = []
    for arc in holdouts:
        if arc not in reg:
            continue
        for pat in pats_1d:
            for s in range(0, PROBE, CHUNK):
                tasks.append((arc, pat, s, min(s + CHUNK, PROBE)))

    print(f"\nworkers={NCPU} tasks={len(tasks)}")
    totals: dict[tuple[str, str], list] = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(pickled,)) as pool:
        for arc, pat, hits in pool.map(_scan, tasks, chunksize=8):
            key = (arc, pat)
            totals.setdefault(key, []).extend(hits)
    print(f"done in {time.time()-t0:.1f}s")

    for arc in holdouts:
        if arc not in reg:
            continue
        rows = []
        for (a, pat), hits in totals.items():
            if a == arc and hits:
                rows.append((pat, len(hits)))
        rows.sort(key=lambda kv: -kv[1])
        if rows:
            print(f"\n{arc} ({sizes[arc]} entries):")
            for pat, n in rows[:5]:
                pct = 100 * n / sizes[arc]
                print(f"  HIT {n:6d}/{sizes[arc]} ({pct:5.1f}%) :: {pat!r}")


if __name__ == "__main__":
    main()
