"""Full chain: tileart.uop -> SUB_9_7 sd_off -> dictionary string containing
that offset -> derive sprite id from filename -> hash into the right archive.
"""
from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def load_sd_index() -> list[tuple[int, int, str]]:
    """Walk string_dictionary.bin once and return a list of (start, end, content)."""
    arc = UopArchive(EC / "string_dictionary.uop")
    sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
    arc.close()
    out = []
    p = 16
    while p + 2 <= len(sd):
        length = struct.unpack_from("<H", sd, p)[0]
        if length == 0 or length > 500:
            break
        content_start = p + 2
        content_end = content_start + length
        if content_end > len(sd):
            break
        out.append((content_start, content_end,
                    sd[content_start: content_end].decode("ascii", errors="replace")))
        p = content_end
    return out


def find_containing(index, offset):
    # binary search by start
    lo, hi = 0, len(index)
    while lo < hi:
        mid = (lo + hi) // 2
        s, e, _ = index[mid]
        if offset < s:
            hi = mid
        elif offset >= e:
            lo = mid + 1
        else:
            return index[mid]
    return None


def parse_sub_9_7(payload, p):
    groups = {}
    for gname in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
        entries = []
        val = payload[p]; p += 1
        if val == 0:
            groups[gname] = entries; continue
        _b = payload[p]; p += 1
        _shader = struct.unpack_from("<I", payload, p)[0]; p += 4
        count = payload[p]; p += 1
        for _ in range(count):
            sd_off = struct.unpack_from("<I", payload, p)[0]; p += 4
            _b2 = payload[p]; p += 1
            tex_rep = struct.unpack_from("<f", payload, p)[0]; p += 4
            _d1 = struct.unpack_from("<I", payload, p)[0]; p += 4
            _d2 = struct.unpack_from("<I", payload, p)[0]; p += 4
            entries.append((sd_off, tex_rep))
        c2 = struct.unpack_from("<I", payload, p)[0]; p += 4 + c2 * 4
        c3 = struct.unpack_from("<I", payload, p)[0]; p += 4 + c3 * 4
        groups[gname] = entries
    return groups


def sub_9_7_offset(payload):
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
            else: return None
        sitting = payload[p]; p += 1
        if sitting != 0: p += 16
        p += 4
        return p
    except Exception:
        return None


# regexes for the three known namespaces
RX_WORLD = re.compile(r'Data\\WorldArt\\(\d+)(?:_[^.]*)?\.tga', re.I)
RX_LEGACY = re.compile(r'Data\\TileArtLegacy\\(\d+)\.tga', re.I)
RX_ENHANCED = re.compile(r'Data\\TileArtEnhanced\\(\d+)\.tga', re.I)


def derive_uop_key(filename: str) -> tuple[str, int, str] | None:
    """Return (archive_label, sprite_id, hash_path) or None."""
    m = RX_WORLD.match(filename)
    if m:
        sid = int(m.group(1))
        return ("WorldArt -> Texture.uop", sid, f"build/worldart/{sid:08}.dds")
    m = RX_LEGACY.match(filename)
    if m:
        sid = int(m.group(1))
        return ("TileArtLegacy -> LegacyTexture.uop", sid, f"build/tileartlegacy/{sid:08}.dds")
    m = RX_ENHANCED.match(filename)
    if m:
        sid = int(m.group(1))
        return ("TileArtEnhanced -> (not shipped)", sid, f"build/tileartenhanced/{sid:08}.dds")
    return None


def main():
    print("Loading dictionary index...")
    sd_index = load_sd_index()
    print(f"  {len(sd_index)} entries loaded")

    print("\nOpening UOP archives...")
    tileart = UopArchive(EC / "tileart.uop")
    legacy = UopArchive(EC / "LegacyTexture.uop")
    hd = UopArchive(EC / "Texture.uop")

    legacy_set = set(legacy.by_hash.keys())
    hd_set = set(hd.by_hash.keys())

    test_tiles = [16384, 16385, 16386, 16387, 16388, 16640, 22137, 19674, 8251, 5903]
    for tid in test_tiles:
        h = hash_name(f"build/tileart/{tid:08}.bin")
        e = tileart.by_hash.get(h)
        if e is None:
            print(f"\n--- tile {tid}: MISS in tileart")
            continue
        payload = tileart.read(e)
        off = sub_9_7_offset(payload)
        if off is None:
            print(f"\n--- tile {tid}: SUB_9_7 parse failed")
            continue
        try:
            groups = parse_sub_9_7(payload, off)
        except Exception as ex:
            print(f"\n--- tile {tid}: parse error: {ex}")
            continue
        print(f"\n--- tile {tid} ---")
        for gname, entries in groups.items():
            if not entries: continue
            for i, (sd_off, tex_rep) in enumerate(entries):
                ent = find_containing(sd_index, sd_off)
                if ent is None:
                    print(f"  [{gname}] #{i}: sd_off={sd_off} -> NOT FOUND")
                    continue
                s, e, content = ent
                derived = derive_uop_key(content)
                if derived:
                    arc_label, sid, path = derived
                    in_legacy = hash_name(path) in legacy_set
                    in_hd = hash_name(path) in hd_set
                    found = "LEGACY" if in_legacy else ("HD" if in_hd else "NONE")
                    print(f"  [{gname}] #{i}: sd_off={sd_off:>6} pos={sd_off-s:>3}/{e-s:>3} "
                          f"-> {content!r}  sid={sid}  -> {arc_label}  found={found}")
                else:
                    print(f"  [{gname}] #{i}: sd_off={sd_off:>6} -> {content!r}  (no namespace match)")

    tileart.close(); legacy.close(); hd.close()


if __name__ == "__main__":
    main()
