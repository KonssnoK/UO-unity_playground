"""Test the hypothesis that the 16-bit value at offset+8 of each SUB_9_7
texture-group entry is the sprite id used to hash into LegacyTexture/Texture.
"""
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def test():
    tileart = UopArchive(EC / "tileart.uop")
    legacy_tex = UopArchive(EC / "LegacyTexture.uop")
    enhanced_tex = UopArchive(EC / "Texture.uop")

    print(f"LegacyTexture entries: {len(legacy_tex.entries)} (unique hashes: {len(legacy_tex.by_hash)})")
    print(f"Texture entries:        {len(enhanced_tex.entries)} (unique hashes: {len(enhanced_tex.by_hash)})")

    # For each tile we examined: pull bytes 8..9 of the SUB_9_7 region as a
    # candidate sprite_id, then probe.
    sample_ids = [19674, 19672, 19661, 19683, 19680, 16384, 16640, 22137, 8251, 5903]

    # We need to skip header + SUB_9..SUB_9_6 (same logic as before).
    def sub_9_7_offset(payload: bytes) -> int:
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
                break
        sitting = payload[p]; p += 1
        if sitting != 0: p += 16
        p += 4  # SUB_9_6 RGBA
        return p

    for tid in sample_ids:
        h = hash_name(f"build/tileart/{tid:08}.bin")
        e = tileart.by_hash.get(h)
        if e is None: continue
        payload = tileart.read(e)
        off = sub_9_7_offset(payload)
        region = payload[off: off + 64]
        print(f"\n--- tile {tid} (size={len(payload)}, sub_9_7 @ 0x{off:X}) ---")
        # bytes 8-9 of the SUB_9_7 region (assuming WorldArt or first non-empty group)
        # We need to find the group that has count=1 and extract its u16 at offset 8 of the entry.
        # Layout: WorldArt cnt @ region[0], then if cnt>0 8-byte entries; TileArtLegacy cnt at the next position; etc.
        p = 0
        groups = []
        for name in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
            cnt = region[p]; p += 1
            entry_bytes = []
            for _ in range(cnt):
                entry_bytes.append(region[p: p + 8])
                p += 8
            groups.append((name, entry_bytes))

        for gname, ents in groups:
            for ei, eb in enumerate(ents):
                # Candidate interpretations of the 8-byte entry
                u16_at_6 = struct.unpack_from("<H", eb, 6)[0]  # bytes 6-7 → low half of b
                u16_at_4 = struct.unpack_from("<H", eb, 4)[0]
                u32_a    = struct.unpack_from("<I", eb, 0)[0]
                u32_b    = struct.unpack_from("<I", eb, 4)[0]
                # Bytes 8-9 of SUB_9_7 region were `25 d5` -> entry offset 6-7 holds the candidate.
                cands = {
                    "u16 at entry+6": u16_at_6,
                    "u16 at entry+4": u16_at_4,
                    "u32 a":          u32_a,
                    "u32 b":          u32_b,
                    "u32 b >> 16":    u32_b >> 16,
                    "u32 b & 0xFFFF": u32_b & 0xFFFF,
                }
                print(f"  [{gname}] entry{ei}: bytes={eb.hex(' ')}  cands={cands}")
                for cl, cv in cands.items():
                    if cv < 0 or cv > 200_000: continue
                    name = f"build/tileartlegacy/{cv:08}.dds"
                    if hash_name(name) in legacy_tex.by_hash:
                        print(f"      HIT LegacyTexture: {cl} = {cv}  -> {name}")
                    name = f"build/worldart/{cv:08}.dds"
                    if hash_name(name) in enhanced_tex.by_hash:
                        print(f"      HIT Texture:       {cl} = {cv}  -> {name}")

    tileart.close()
    legacy_tex.close()
    enhanced_tex.close()


if __name__ == "__main__":
    test()
