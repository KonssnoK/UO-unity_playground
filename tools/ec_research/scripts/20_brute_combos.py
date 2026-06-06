"""Final brute-force sweep: case x separator x suffix x extension on legacy/texture/animation."""
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


def gen_patterns(folders, suffixes, exts, num_fmts):
    out = []
    for sep in ['/', '\\']:
        for prefix in ['Build', 'build', '']:
            for folder in folders:
                for suffix in suffixes:
                    for ext in exts:
                        for nf in num_fmts:
                            pre = f"{prefix}{sep}" if prefix else ""
                            sfx = f"_{suffix}" if suffix else ""
                            out.append(f"{pre}{folder}{sep}{nf}{sfx}{ext}")
    return list(set(out))


legacy_folders = ['LegacyTexture', 'legacytexture', 'LegacyTileArt', 'legacytileart', 'LegacyArt', 'legacyart']
legacy_suffixes = ['LegacyTileArt', 'legacytileart', 'Texture', 'texture', '']
texture_folders = ['Texture', 'texture', 'TileArt', 'tileart']
texture_suffixes = ['TileArt', 'tileart', 'Texture', 'texture', '']
exts = ['.dds', '.DDS', '.tex', '']
num_fmts = ['{0:08}', '{0:08X}', '{0:08x}', '{0:06}', '{0:d}', '{0}']

af1_folders = ['AnimationFrame1', 'animationframe1', 'AnimationFrame', 'animationframe', 'Animation', 'animation']
af1_suffixes = ['AnimationFrame', 'animationframe', 'Animation', 'animation', 'Frame', 'frame', '']
af1_exts = ['.bin', '.amou', '.dds', '']

legacy_pats = gen_patterns(legacy_folders, legacy_suffixes, exts, num_fmts)
texture_pats = gen_patterns(texture_folders, texture_suffixes, exts, num_fmts)
af1_pats = gen_patterns(af1_folders, af1_suffixes, af1_exts, num_fmts)

print(f"legacy: {len(legacy_pats)}, texture: {len(texture_pats)}, af1: {len(af1_pats)}")

_HASH_SET: set[int] = set()
def _init(p):
    global _HASH_SET
    _HASH_SET = pickle.loads(p)


def _scan(args):
    pat, lo, hi = args
    hits = 0
    for i in range(lo, hi):
        if hash_name(pat.format(i)) in _HASH_SET:
            hits += 1
    return pat, hits


def run(arc_name, patterns, probe_max):
    arc = UopArchive(EC / arc_name)
    hash_set = set(arc.by_hash.keys())
    arc.close()
    print(f"\n=== {arc_name}: {len(hash_set)} entries, {len(patterns)} patterns × [0,{probe_max}) ===")
    p = pickle.dumps(hash_set)
    chunk = max(2000, probe_max // (NCPU * 2))
    tasks = [(pat, s, min(s + chunk, probe_max)) for pat in patterns for s in range(0, probe_max, chunk)]
    totals: dict[str, int] = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(p,)) as pool:
        for pat, hits in pool.map(_scan, tasks, chunksize=16):
            totals[pat] = totals.get(pat, 0) + hits
    for pat, hits in sorted(totals.items(), key=lambda kv: -kv[1])[:5]:
        if hits > 0:
            print(f"  HITS {hits}/{len(hash_set)}: {pat!r}")
    if max(totals.values(), default=0) == 0:
        print("  no hits.")
    print(f"  {time.time()-t0:.1f}s")


if __name__ == "__main__":
    run("LegacyTexture.uop", legacy_pats, probe_max=70_000)
    run("Texture.uop", texture_pats, probe_max=20_000)
    run("AnimationFrame1.uop", af1_pats, probe_max=20_000)
