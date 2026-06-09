"""Compare SUB_9_7 raw bytes between tile 200 (broken) and tile 16384 (verified working).
Look at how the parser walks each, what count it reads, and whether the entries are valid."""
import struct, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
tileart = UopArchive(EC / "tileart.uop")


def sub_9_7_offset(payload):
    p = 0x7D
    cnt = payload[p]; p += 1 + cnt * 5
    cnt = payload[p]; p += 1 + cnt * 5
    cnt = struct.unpack_from("<I", payload, p)[0]; p += 4 + cnt * 8
    cnt = struct.unpack_from("<I", payload, p)[0]; p += 4
    for _ in range(cnt):
        val = payload[p]; p += 1
        if val == 0:
            sub = struct.unpack_from("<I", payload, p)[0]; p += 4 + sub * 8
        elif val == 1:
            p += 5
        else: return None
    sitting = payload[p]; p += 1
    if sitting != 0: p += 16
    p += 4
    return p


def dump_sub_9_7(art_id, label):
    print(f"\n========= {label} (art_id {art_id}) =========")
    h = hash_name(f"build/tileart/{art_id:08}.bin")
    e = tileart.by_hash.get(h)
    if e is None:
        print(f"  no record")
        return
    payload = tileart.read(e)
    off = sub_9_7_offset(payload)
    print(f"  total bytes={len(payload)}, SUB_9_7@0x{off:X}")
    p = off
    for gname in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
        val = payload[p]
        print(f"\n  [{gname}] @0x{p:X}  val={val}")
        p += 1
        if val == 0: continue
        unk = payload[p]; p += 1
        shader = struct.unpack_from("<I", payload, p)[0]; p += 4
        count = payload[p]; p += 1
        print(f"    unk={unk}  shader=0x{shader:X}  count={count}")
        # dump raw bytes for `count` chunks of 17 bytes
        for i in range(count):
            entry = payload[p:p+17]
            sd_off = struct.unpack_from("<I", entry, 0)[0]
            b      = entry[4]
            rep    = struct.unpack_from("<f", entry, 5)[0]
            d1     = struct.unpack_from("<I", entry, 9)[0]
            d2     = struct.unpack_from("<I", entry, 13)[0]
            print(f"    #{i}@0x{p:X} hex={entry.hex()}  sd_off={sd_off} b={b} rep={rep} d1={d1} d2={d2}")
            p += 17
        c2 = struct.unpack_from("<I", payload, p)[0]; p += 4
        print(f"    secondaryCount={c2}  (next 8 bytes hex: {payload[p:p+8].hex()})")
        for _ in range(c2): p += 4
        c3 = struct.unpack_from("<I", payload, p)[0]; p += 4
        print(f"    tertiaryCount={c3}  (next 8 bytes hex: {payload[p:p+8].hex()})")
        for _ in range(c3): p += 4


# Verified working
dump_sub_9_7(16384, "VERIFIED tile 16384 (461 Rattan_Wall)")
# Broken
dump_sub_9_7(200 + 0x4000, "BROKEN tile 200 (expected 200 Mage_Stone_Walls)")
tileart.close()
