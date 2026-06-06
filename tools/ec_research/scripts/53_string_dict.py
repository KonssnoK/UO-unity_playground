"""Decode string_dictionary.uop and use it to resolve SUB_9_7 references.

Per the project owner's wiki Texture.creole, each SUB_9_7 texture entry
contains a DWORD that's a StringDictionary offset pointing to a TGA/DDS
filename. The full SUB_9_7 group layout is:

    BYTE Val (group enable flag)
    if Val != 0:
        BYTE
        DWORD Shader
        BYTE Count                                        <- num textures
        for _ in range(Count):
            DWORD StringDictionary offset (-> filename)
            BYTE
            DWORD float TextureRepetition
            DWORD
            DWORD                                          (17 bytes per tex)
        DWORD Count
        for _ in range(Count): DWORD
        DWORD Count
        for _ in range(Count): DWORD float
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def load_string_dictionary() -> bytes:
    arc = UopArchive(EC / "string_dictionary.uop")
    payload = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
    arc.close()
    return payload


def inspect_string_dict(blob: bytes):
    """Peek at the head/structure of string_dictionary.bin."""
    print(f"string_dictionary.bin size: {len(blob)}")
    print(f"first 32 bytes: {blob[:32].hex(' ')}")
    print(f"as text head:   {blob[:64]!r}")
    # Try to interpret as a series of length-prefixed strings, or
    # as a flat array of fixed-size records.


def read_string_at_offset(blob: bytes, offset: int) -> str | None:
    """Naive attempt — try a few layouts."""
    if offset < 0 or offset >= len(blob):
        return None
    # Option 1: null-terminated string at byte offset
    end = blob.find(b"\x00", offset)
    if end > offset and end - offset < 200:
        try:
            return blob[offset: end].decode("ascii")
        except Exception:
            pass
    return None


# Re-implement SUB_9_7 parsing per the wiki spec
def parse_sub_9_7(payload: bytes, p: int) -> dict[str, list[dict]]:
    """Parse the 4 groups using the wiki TEXTURE() spec."""
    groups = {}
    for gname in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
        entries = []
        val = payload[p]; p += 1
        if val == 0:
            groups[gname] = entries
            continue
        _b = payload[p]; p += 1
        shader = struct.unpack_from("<I", payload, p)[0]; p += 4
        count = payload[p]; p += 1
        for _ in range(count):
            sd_off = struct.unpack_from("<I", payload, p)[0]; p += 4
            _b2 = payload[p]; p += 1
            tex_rep = struct.unpack_from("<f", payload, p)[0]; p += 4
            d1 = struct.unpack_from("<I", payload, p)[0]; p += 4
            d2 = struct.unpack_from("<I", payload, p)[0]; p += 4
            entries.append({"sd_off": sd_off, "tex_rep": tex_rep, "d1": d1, "d2": d2})
        c2 = struct.unpack_from("<I", payload, p)[0]; p += 4
        for _ in range(c2):
            _ = struct.unpack_from("<I", payload, p)[0]; p += 4
        c3 = struct.unpack_from("<I", payload, p)[0]; p += 4
        for _ in range(c3):
            _ = struct.unpack_from("<I", payload, p)[0]; p += 4
        groups[gname] = entries
    return groups


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
            else: return None
        sitting = payload[p]; p += 1
        if sitting != 0: p += 16
        p += 4
        return p
    except Exception:
        return None


def main():
    sd = load_string_dictionary()
    inspect_string_dict(sd)
    print()

    tileart = UopArchive(EC / "tileart.uop")
    sample_ids = [16384, 16385, 16386, 16640, 22137, 19674]

    for tid in sample_ids:
        h = hash_name(f"build/tileart/{tid:08}.bin")
        e = tileart.by_hash.get(h)
        if e is None:
            print(f"\n--- tile {tid}: not in tileart")
            continue
        payload = tileart.read(e)
        off = sub_9_7_offset(payload)
        if off is None:
            print(f"\n--- tile {tid}: failed to locate SUB_9_7")
            continue
        try:
            groups = parse_sub_9_7(payload, off)
        except Exception as ex:
            print(f"\n--- tile {tid}: parse failed @ {ex}")
            continue
        print(f"\n--- tile {tid} (sub_9_7 @ 0x{off:X}) ---")
        for gname, ents in groups.items():
            if not ents: continue
            print(f"  [{gname}]")
            for i, en in enumerate(ents):
                sd_off = en["sd_off"]
                s = read_string_at_offset(sd, sd_off)
                print(f"    #{i}: sd_off={sd_off}  tex_rep={en['tex_rep']:.2f}  "
                      f"d1={en['d1']} d2={en['d2']}  -> string={s!r}")
    tileart.close()


if __name__ == "__main__":
    main()
