"""Scan every entry in tileart.uop and measure how many resolve to a DDS in
Texture.uop or LegacyTexture.uop via our current sprite-id decoder.

Outputs aggregate stats so we can decide: is the decoder wrong, or are we
just looking at a sparse area of the world?
"""
from __future__ import annotations

import struct
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def sub_9_7_offset(payload: bytes) -> int | None:
    try:
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
            else:
                return None
        sitting = payload[p]; p += 1
        if sitting != 0: p += 16
        p += 4
        return p
    except Exception:
        return None


def parse_groups(payload: bytes, off: int):
    """Return per-group list of sprite ids using the (8-byte entry, b>>16) layout."""
    groups = {"WorldArt": [], "TileArtLegacy": [], "TileArtEnhanced": [], "Textures": []}
    p = off
    for gname in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
        try:
            cnt = payload[p]; p += 1
            for _ in range(cnt):
                # 8 bytes per entry
                if p + 8 > len(payload):
                    return groups
                u32_b = struct.unpack_from("<I", payload, p + 4)[0]
                groups[gname].append(u32_b >> 16)
                p += 8
        except Exception:
            return groups
    return groups


def main():
    tileart = UopArchive(EC / "tileart.uop")
    legacy = UopArchive(EC / "LegacyTexture.uop")
    hd = UopArchive(EC / "Texture.uop")

    # Build hash sets for fast lookup.
    legacy_set = set(legacy.by_hash.keys())
    hd_set = set(hd.by_hash.keys())
    legacy.close(); hd.close()

    total = 0
    no_header = 0
    no_sub_9_7 = 0
    no_refs = 0
    hd_hits = 0
    legacy_hits = 0
    any_hit = 0
    miss = 0
    # Distribution of sprite_id values for misses (to see if they cluster).
    miss_ids: Counter = Counter()

    for entry in tileart.entries:
        total += 1
        payload = tileart.read(entry)
        if len(payload) < 0x80:
            no_header += 1
            continue
        off = sub_9_7_offset(payload)
        if off is None:
            no_sub_9_7 += 1
            continue
        groups = parse_groups(payload, off)
        ids = []
        for v in groups.values():
            ids.extend(v)
        if not ids:
            no_refs += 1
            continue

        hit = False
        for sid in ids:
            if hash_name(f"build/worldart/{sid:08}.dds") in hd_set:
                hd_hits += 1; hit = True; break
            if hash_name(f"build/tileartlegacy/{sid:08}.dds") in legacy_set:
                legacy_hits += 1; hit = True; break
        if hit:
            any_hit += 1
        else:
            miss += 1
            for sid in ids:
                miss_ids[sid // 1000 * 1000] += 1  # bucket by thousand
    tileart.close()

    print(f"Total entries scanned: {total}")
    print(f"  no header:         {no_header}")
    print(f"  no SUB_9_7 offset: {no_sub_9_7}")
    print(f"  no refs in record: {no_refs}")
    print(f"  any hit:           {any_hit:6d}  ({100 * any_hit / total:.1f}%)")
    print(f"    via HD:          {hd_hits}")
    print(f"    via Legacy:      {legacy_hits}")
    print(f"  miss (had refs):   {miss}")
    print()
    print("Top 12 miss sprite-id buckets (by hundreds):")
    for bucket, count in miss_ids.most_common(12):
        print(f"  {bucket:>6}..{bucket+999}: {count}")


if __name__ == "__main__":
    main()
