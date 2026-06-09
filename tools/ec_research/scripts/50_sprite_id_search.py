"""Search ALL EC UOPs (not just Texture/LegacyTexture) for hashes of the
missing tree sprite ids, to find which archive (if any) holds them.

Candidate patterns to test for each sprite_id:
  build/<folder>/{id:08}.{ext}
where <folder> spans every UOP-stem we know about, and ext is .dds/.tga/.bin.
"""
from __future__ import annotations

import os
import sys
import pickle
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16

# Sprite ids from user's view that didn't resolve.
TREE_SPRITES = [54565, 54557, 54522, 54601, 54589]

# Try every archive in the EC folder
ARCHIVES = [p.name for p in EC.glob("*.uop")]

# Folder prefixes — UOP stem lowercased, plus the few aliases we've seen.
PATTERNS = [
    "build/worldart/{id:08}.dds",
    "build/tileartlegacy/{id:08}.dds",
    "build/tileartenhanced/{id:08}.dds",
    "build/texture/{id:08}.dds",
    "build/enhancedtexture/{id:08}.dds",
    "build/effecttexture/{id:08}.dds",
    "build/radarmaptexture/{id:08}.dds",
    "build/paperdoll/{id:06}/{action:02}.bin",   # for sanity
    "build/animationframe/{id:06}/{action:02}.bin",
    # Generic naming guesses
    "build/tileart/{id:08}.bin",
    "build/{folder}/{id:08}.dds",
]

_REG: dict[str, set[int]] = {}

def _init(p):
    global _REG; _REG = pickle.loads(p)


def _scan(args):
    arc_name, ids, fmt = args
    s = _REG[arc_name]
    out = []
    for sid in ids:
        # special-case for 2D nested
        if "{action:02}" in fmt:
            for action in range(48):
                name = fmt.format(id=sid, action=action)
                if hash_name(name) in s:
                    out.append((sid, action, name))
            continue
        name = fmt.format(id=sid)
        if hash_name(name) in s:
            out.append((sid, None, name))
    return arc_name, fmt, out


def main():
    reg = {}
    for n in ARCHIVES:
        try:
            arc = UopArchive(EC / n)
            reg[n] = set(arc.by_hash.keys())
            arc.close()
        except Exception as e:
            print(f"  skip {n}: {e}")
    print(f"loaded {len(reg)} archives")
    pickled = pickle.dumps(reg)

    tasks = []
    for arc_name in reg:
        for fmt in PATTERNS:
            if "{folder}" in fmt: continue
            tasks.append((arc_name, TREE_SPRITES, fmt))

    print(f"workers={NCPU}  tasks={len(tasks)}")
    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(pickled,)) as pool:
        for arc_name, fmt, hits in pool.map(_scan, tasks):
            if hits:
                print(f"\nARCHIVE {arc_name} pattern {fmt!r}:")
                for h in hits:
                    print(f"   HIT {h}")

    print("\n(if no archive printed above, none of the patterns hash to any tree sprite id)")


if __name__ == "__main__":
    main()
