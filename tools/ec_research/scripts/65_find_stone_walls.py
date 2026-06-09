"""Find which CC tile_ids point to sprite 200 (Mage_Stone_Walls) and list nearby
stone-wall sprites — to figure out what the EC client actually shows for what
CC calls 'tile 200 stone wall'."""
import re, struct, sys
from pathlib import Path
from multiprocessing import Pool

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

arc = UopArchive(EC / "string_dictionary.uop")
sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
arc.close()

# Index dict using PREFIX-based range (matches the C# fix)
entries = []
p = 16
while p + 2 <= len(sd):
    length = struct.unpack_from("<H", sd, p)[0]
    if length == 0 or length > 500: break
    cs = p + 2; ce = cs + length
    if ce > len(sd): break
    entries.append((p, ce, sd[cs:ce].decode("ascii", errors="replace")))
    p = ce

print(f"{len(entries)} entries; using prefix-inclusive range")

# Print all "stone" entries
print("\n--- All 'stone' entries ---")
for ps, pe, s in entries:
    if "stone" in s.lower() and "wall" in s.lower():
        print(f"  {ps:>6}..{pe:>6}  {s!r}")

def find_string(off):
    lo, hi = 0, len(entries)
    while lo < hi:
        mid = (lo+hi)//2
        if off < entries[mid][0]: hi = mid
        elif off >= entries[mid][1]: lo = mid+1
        else: return entries[mid][2]
    return None

# Walk ALL tileart records and find any whose resolved string mentions sprite 200
tileart = UopArchive(EC / "tileart.uop")
print(f"\nScanning {len(tileart.entries)} tileart records...")

# Reuse sub_9_7_offset
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


def parse_record(payload):
    try:
        tid = struct.unpack_from("<I", payload, 6)[0]
        off = sub_9_7_offset(payload)
        if off is None: return tid, []
        p = off
        refs = []
        for gname in ("WorldArt","TileArtLegacy","TileArtEnhanced","Textures"):
            val = payload[p]; p += 1
            if val == 0: continue
            p += 1                                  # unk
            p += 4                                  # shader
            count = payload[p]; p += 1
            for _ in range(count):
                sd_off = struct.unpack_from("<I", payload, p)[0]; p += 17
                refs.append((gname, sd_off))
            c2 = struct.unpack_from("<I", payload, p)[0]; p += 4 + c2*4
            c3 = struct.unpack_from("<I", payload, p)[0]; p += 4 + c3*4
        return tid, refs
    except Exception:
        return None, []


count_scanned = 0
tile200_owners = []
stone_wall_owners = []  # tiles resolving to any sprite with 'stone' and 'wall'
art200_record = None
all_records = []
for e in tileart.entries[:30000]:
    try:
        payload = tileart.read(e)
    except Exception:
        continue
    tid, refs = parse_record(payload)
    if tid is None: continue
    count_scanned += 1
    for gname, sd_off in refs:
        s = find_string(sd_off)
        if not s: continue
        if "00000200_" in s:
            tile200_owners.append((tid, gname, sd_off, s))
        if "stone" in s.lower() and "wall" in s.lower():
            stone_wall_owners.append((tid, gname, sd_off, s))

tileart.close()

print(f"\nScanned {count_scanned} records")
print(f"\n--- CC tiles whose tileart points to sprite 200 (Mage_Stone_Walls) ---")
for tid, g, off, s in tile200_owners[:20]:
    cc_id = tid - 0x4000 if tid >= 0x4000 else tid
    print(f"  art_id={tid} (cc_id={cc_id})  group={g}  sd_off={off}  {s!r}")
print(f"  ... ({len(tile200_owners)} total)")

print(f"\n--- All stone-wall references (first 30) ---")
seen_strings = set()
for tid, g, off, s in stone_wall_owners:
    if s in seen_strings: continue
    seen_strings.add(s)
    cc_id = tid - 0x4000 if tid >= 0x4000 else tid
    print(f"  art_id={tid} (cc_id={cc_id})  group={g}  -> {s!r}")
    if len(seen_strings) >= 30: break
