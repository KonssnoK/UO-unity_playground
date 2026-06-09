"""Reverse-engineer the SUB_9_7 textures reference inside tileart.uop records.

Each tileart record carries up to four texture refs (WorldArt / TileArtLegacy /
TileArtEnhanced / Textures). My current C# guess assumes `(byte count, then
count × (u32, u32))` for each group. The `b` values we see look like
`<id_or_hash>:16 | 0:16` for static tiles, but the relationship between `b`
and an actual sprite-id key in Texture.uop / LegacyTexture.uop has not been
confirmed.

This script picks a handful of tiles whose SPRITE we'd recognize and tries
several interpretations of the SUB_9_7 references:

  1. `b` (lower 32 bits) treated as the sprite id ->
     build/tileartlegacy/{b:08}.dds
  2. `b >> 16` (upper 16 bits) treated as the sprite id
  3. `a` (256 in every sample so far) treated as the sprite id (sanity)
  4. `a:16 | b:16` etc.

For each candidate, we hash the proposed name and check whether the resulting
hash exists in the Texture.uop / LegacyTexture.uop archives.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name


EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def read_record(arc: UopArchive, tile_id: int) -> bytes | None:
    h = hash_name(f"build/tileart/{tile_id:08}.bin")
    e = arc.by_hash.get(h)
    if e is None:
        return None
    return arc.read(e)


class R:
    def __init__(self, buf: bytes):
        self.buf, self.p = buf, 0

    def u8(self):  v = self.buf[self.p]; self.p += 1; return v
    def u16(self): v = struct.unpack_from("<H", self.buf, self.p)[0]; self.p += 2; return v
    def u32(self): v = struct.unpack_from("<I", self.buf, self.p)[0]; self.p += 4; return v
    def u64(self): v = struct.unpack_from("<Q", self.buf, self.p)[0]; self.p += 8; return v
    def f32(self): v = struct.unpack_from("<f", self.buf, self.p)[0]; self.p += 4; return v

    def skip_to_sub_9_7(self):
        # header through 0x7C (image blobs end at 0x7D)
        self.p = 0x7D

        # SUB_9 (u8 count + count × (u8, u32))
        cnt = self.u8()
        self.p += cnt * 5
        # SUB_9_2
        cnt = self.u8()
        self.p += cnt * 5
        # SUB_9_3 (u32 count + count × (u32, u32))
        cnt = self.u32()
        self.p += cnt * 8
        # SUB_9_4 (u32 count + variable per entry)
        cnt = self.u32()
        for _ in range(cnt):
            val = self.u8()
            if val == 0:
                sub = self.u32()
                self.p += sub * 8
            elif val == 1:
                self.p += 5
            else:
                break
        # SUB_9_5
        sitting = self.u8()
        if sitting != 0:
            self.p += 16
        # SUB_9_6 (RGBA radar)
        self.p += 4

    def read_sub_9_7_group(self):
        """Read one of the four texture groups under our current guess:
        u8 count, then count × (u32 a, u32 b)."""
        cnt = self.u8()
        entries = []
        for _ in range(cnt):
            a = self.u32()
            b = self.u32()
            entries.append((a, b))
        return entries


def candidates_from_ab(a: int, b: int) -> list[tuple[str, int]]:
    """Return (label, id) interpretations to try as a sprite id."""
    return [
        ("b (full)",      b),
        ("b >> 16",       b >> 16),
        ("b & 0xFFFF",    b & 0xFFFF),
        ("b - 0x4000",    b - 0x4000 if b >= 0x4000 else b),
        ("a",             a),
        ("a >> 16",       a >> 16),
    ]


def probe(arc_name: str, prefix: str, candidates: list[int]) -> list[tuple[int, str]]:
    """Return (id, name) hits in the archive for any candidate id."""
    arc = UopArchive(EC / arc_name)
    seen = arc.by_hash
    out = []
    for cid in candidates:
        if cid is None or cid < 0:
            continue
        name = f"{prefix}{cid:08}.dds"
        if hash_name(name) in seen:
            out.append((cid, name))
    arc.close()
    return out


def main():
    arc = UopArchive(EC / "tileart.uop")
    # Tile ids whose sprite shape we know roughly. Trees in CC's art are around
    # static ids 3155..3245 (item-id space), i.e. art ids 19539..19629. The
    # log we already have shows trees at 19661, 19672, 19674, 19680, 19683.
    sample_ids = [19674, 19672, 19661, 19683, 19680,    # observed in user's run
                  16384, 16640, 22137, 8251, 5903]      # earlier known tiles

    for tid in sample_ids:
        payload = read_record(arc, tid)
        if payload is None:
            print(f"\n--- tile {tid}: NOT FOUND")
            continue
        r = R(payload)
        try:
            r.skip_to_sub_9_7()
        except Exception as ex:
            print(f"\n--- tile {tid}: skip failed {ex}")
            continue

        groups = [
            ("WorldArt",         "build/worldart/"),
            ("TileArtLegacy",    "build/tileartlegacy/"),
            ("TileArtEnhanced",  "build/tileartenhanced/"),  # archive may not exist; harmless
            ("Textures",         "build/textures/"),         # ditto
        ]
        print(f"\n=== tile {tid} (payload {len(payload)}B; record_offset_at_sub_9_7 = 0x{r.p:X}) ===")
        for label, prefix in groups:
            try:
                entries = r.read_sub_9_7_group()
            except Exception as ex:
                print(f"  group {label}: parse error {ex}")
                break
            if not entries:
                print(f"  group {label}: empty")
                continue
            print(f"  group {label}: {entries}")
            # Try every candidate from the first (a,b) against the corresponding archive.
            a, b = entries[0]
            # candidates exist regardless of archive — pull plausible numeric ids
            for cand_label, cid in candidates_from_ab(a, b):
                hits_legacy = probe("LegacyTexture.uop", "build/tileartlegacy/", [cid])
                hits_world  = probe("Texture.uop",       "build/worldart/",       [cid])
                if hits_legacy or hits_world:
                    print(f"    candidate {cand_label!r:14} cid={cid}  "
                          f"-> LegacyTexture:{bool(hits_legacy)} Texture:{bool(hits_world)}")
    arc.close()


if __name__ == "__main__":
    main()
