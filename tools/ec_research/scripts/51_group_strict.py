"""Measure resolution rate using GROUP-STRICT lookup:
  WorldArt group       -> build/worldart/<id:08>.dds in Texture.uop only
  TileArtLegacy group  -> build/tileartlegacy/<id:08>.dds in LegacyTexture.uop only
  TileArtEnhanced grp  -> build/tileartenhanced/<id:08>.dds (target archive unknown)
  Textures grp         -> reserved for lights

We need to know whether group-strict lookup gives a HIGH true-positive rate
(meaning sprite_ids only belong to their declared archive). If yes, the
"wrong sprite" issue goes away.
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


def parse_groups(payload: bytes, off: int) -> dict[str, list[int]]:
    groups = {"WorldArt": [], "TileArtLegacy": [], "TileArtEnhanced": [], "Textures": []}
    p = off
    for gname in groups:
        try:
            cnt = payload[p]; p += 1
            for _ in range(cnt):
                if p + 8 > len(payload):
                    return groups
                b = struct.unpack_from("<I", payload, p + 4)[0]
                groups[gname].append(b >> 16)
                p += 8
        except Exception:
            return groups
    return groups


def main():
    tileart = UopArchive(EC / "tileart.uop")
    legacy = UopArchive(EC / "LegacyTexture.uop")
    texture = UopArchive(EC / "Texture.uop")
    legacy_set = set(legacy.by_hash.keys())
    texture_set = set(texture.by_hash.keys())
    legacy.close(); texture.close()

    total = 0
    strict_hit = 0
    strict_hit_via_world = 0
    strict_hit_via_legacy = 0
    strict_hit_via_enhanced = 0
    strict_miss = 0
    no_groups = 0

    # Compare with cross-archive lookup
    cross_hit = 0
    only_cross_hit = 0   # cross says yes, strict says no — these are the "wrong sprite" cases

    cross_buckets: Counter = Counter()

    for entry in tileart.entries:
        total += 1
        payload = tileart.read(entry)
        if len(payload) < 0x80:
            continue
        off = sub_9_7_offset(payload)
        if off is None:
            continue
        groups = parse_groups(payload, off)
        all_ids = []
        for v in groups.values():
            all_ids.extend(v)
        if not all_ids:
            no_groups += 1
            continue

        # Strict resolution
        strict_resolved = False
        for sid in groups["WorldArt"]:
            if hash_name(f"build/worldart/{sid:08}.dds") in texture_set:
                strict_resolved = True; strict_hit_via_world += 1; break
        if not strict_resolved:
            for sid in groups["TileArtLegacy"]:
                if hash_name(f"build/tileartlegacy/{sid:08}.dds") in legacy_set:
                    strict_resolved = True; strict_hit_via_legacy += 1; break
        if not strict_resolved:
            for sid in groups["TileArtEnhanced"]:
                # Try both possible prefixes for the enhanced archive
                if hash_name(f"build/tileartenhanced/{sid:08}.dds") in texture_set:
                    strict_resolved = True; strict_hit_via_enhanced += 1; break
                if hash_name(f"build/worldart/{sid:08}.dds") in texture_set:
                    strict_resolved = True; strict_hit_via_enhanced += 1; break

        if strict_resolved:
            strict_hit += 1
        else:
            strict_miss += 1

        # Cross-archive (loose) resolution — what my current C# code does
        cross_resolved = False
        for sid in all_ids:
            if hash_name(f"build/worldart/{sid:08}.dds") in texture_set:
                cross_resolved = True; break
            if hash_name(f"build/tileartlegacy/{sid:08}.dds") in legacy_set:
                cross_resolved = True; break

        if cross_resolved:
            cross_hit += 1
            if not strict_resolved:
                only_cross_hit += 1   # these are the "wrong sprite" tiles!

    tileart.close()

    print(f"Total tileart records: {total}")
    print(f"  no groups (parse fail or empty): {no_groups}")
    print()
    print(f"STRICT resolution (group -> matching archive only):")
    print(f"  hits:   {strict_hit:6d}  ({100*strict_hit/total:.1f}%)")
    print(f"    via WorldArt -> Texture.uop:        {strict_hit_via_world}")
    print(f"    via TileArtLegacy -> LegacyTex:     {strict_hit_via_legacy}")
    print(f"    via TileArtEnhanced -> Texture.uop: {strict_hit_via_enhanced}")
    print(f"  misses: {strict_miss}")
    print()
    print(f"CROSS resolution (any group -> any archive):")
    print(f"  hits:   {cross_hit:6d}  ({100*cross_hit/total:.1f}%)")
    print()
    print(f"=> 'wrong sprite' suspects (cross hit but strict miss): {only_cross_hit}")
    print(f"    these are tiles my current C# code substitutes WRONGLY.")


if __name__ == "__main__":
    main()
