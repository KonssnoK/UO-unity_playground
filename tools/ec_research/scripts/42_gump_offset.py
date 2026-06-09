"""Verify GumpArtMask uses id+1000000 offset based on disassembly find."""
import os
import sys
import pickle
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
NCPU = os.cpu_count() or 16

_HS: set[int] = set()


def _init(p):
    global _HS
    _HS = pickle.loads(p)


def _hit_plain(args):
    lo, hi = args
    return sum(1 for i in range(lo, hi)
               if hash_name(f"build/gumpartmask/0{i}.dds") in _HS)


def _hit_offset(args):
    lo, hi = args
    return sum(1 for i in range(lo, hi)
               if hash_name(f"build/gumpartmask/0{i + 1000000}.dds") in _HS)


def _hit_offset_e(args):
    lo, hi = args
    return sum(1 for i in range(lo, hi)
               if hash_name(f"build/gumpartmask/0{i + 1000000}.dds") in _HS or
                  hash_name(f"build/gumpartmask/{i + 1000000}.dds") in _HS)


if __name__ == "__main__":
    arc = UopArchive(EC / "GumpArtMask.uop")
    hs = set(arc.by_hash.keys())
    arc.close()
    print(f"GumpArtMask.uop: {len(hs)} entries")
    p = pickle.dumps(hs)

    PROBE = 200_000
    CHUNK = 5000
    tasks = [(s, min(s + CHUNK, PROBE)) for s in range(0, PROBE, CHUNK)]

    with ProcessPoolExecutor(max_workers=NCPU, initializer=_init, initargs=(p,)) as pool:
        a = sum(pool.map(_hit_plain, tasks))
        b = sum(pool.map(_hit_offset, tasks))

    print(f"  plain      'build/gumpartmask/0<id>.dds'            -> {a}/{len(hs)}")
    print(f"  +1M offset 'build/gumpartmask/0<id+1000000>.dds'    -> {b}/{len(hs)}")
