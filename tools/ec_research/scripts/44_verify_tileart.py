"""Verify the wiki's Tileart record format against real tileart.uop entries.

Wiki source: tools/ec_research/docs/wiki_assumptions/Tileart.creole
Treat every field there as an assumption to verify.

Strategy:
  1. Parse a handful of records using the wiki spec.
  2. Check invariants we expect:
     - WORD at 0x00 is 0x0004 (our build), wiki said 0x0003.
     - DWORD at 0x06 equals the tile id we used to look it up.
     - SUB_9 / SUB_9_2 count bytes are sane (<= ~30 per legacy tiledata).
     - Sum of consumed bytes equals payload length.
  3. Cross-reference height / weight values against CC's tiledata.mul for the same id where possible.

The verifier reports per-record:
  - successful structural parse
  - mismatches between expected/observed fields
  - leftover bytes if any
"""
from __future__ import annotations

import io
import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


PROP_NAMES = {
    0: "Weight", 1: "Quality", 2: "Quantity", 3: "Height",
    4: "Value",  5: "AcVc",    6: "Slot",     7: "off_C8",
    8: "Appearance", 9: "Race", 10: "Gender", 11: "Paperdoll",
}


@dataclass
class TileArtRecord:
    version: int = 0
    string_id: int = 0
    tile_id: int = 0
    unk_bool: int = 0
    unk_byte: int = 0
    unk_float_a: float = 0.0
    unk_float_b: float = 0.0
    fixed_zero: int = 0
    old_id: int = 0
    unk_dword_a: int = 0
    unk_dword_b: int = 0
    unk_byte_2: int = 0
    unk_float_c: float = 0.0
    unk_dword_c: int = 0
    light_float_a: float = 0.0
    light_float_b: float = 0.0
    unk_dword_d: int = 0
    flags_a: int = 0
    flags_b: int = 0
    unk_dword_e: int = 0
    ec_image: bytes = b""
    img2d_image: bytes = b""

    props_a: list[tuple[int, int]] = field(default_factory=list)
    props_b: list[tuple[int, int]] = field(default_factory=list)
    money: list[tuple[int, int]] = field(default_factory=list)
    sub4: list = field(default_factory=list)
    sitting: tuple | None = None
    radar_rgba: tuple[int, int, int, int] | None = None
    textures_groups: list = field(default_factory=list)
    effects: list = field(default_factory=list)
    leftover: bytes = b""


class Reader:
    def __init__(self, b: bytes):
        self.b = b
        self.p = 0
        self.n = len(b)

    def remaining(self) -> int:
        return self.n - self.p

    def take(self, n: int) -> bytes:
        if self.p + n > self.n:
            raise ValueError(f"need {n}, have {self.remaining()}")
        out = self.b[self.p: self.p + n]
        self.p += n
        return out

    def u8(self):  return struct.unpack_from("<B", self.take(1))[0]
    def u16(self): return struct.unpack_from("<H", self.take(2))[0]
    def u32(self): return struct.unpack_from("<I", self.take(4))[0]
    def u64(self): return struct.unpack_from("<Q", self.take(8))[0]
    def f32(self): return struct.unpack_from("<f", self.take(4))[0]


def parse_textures_group(r: Reader) -> list[dict]:
    """SUB_9_7 — one of four texture groups. Wiki marks it as 'call TEXTURES()'
    but doesn't expand the function. We empirically observe one count + N entries,
    each containing a string-dict offset / id pair."""
    # First try the simplest layout: BYTE count, then N × {DWORD imgId, DWORD?}
    count = r.u8()
    entries = []
    # heuristic: try N * 8 bytes; if that overshoots remaining, fall back
    for _ in range(count):
        if r.remaining() < 8:
            return [{"_ERR": "out of bytes mid-textures", "count_so_far": len(entries)}]
        a = r.u32()
        b = r.u32()
        entries.append({"a": a, "b": b})
    return entries


def parse_record(payload: bytes) -> TileArtRecord:
    r = Reader(payload)
    rec = TileArtRecord()
    rec.version       = r.u16()
    rec.string_id     = r.u32()
    rec.tile_id       = r.u32()
    rec.unk_bool      = r.u8()
    rec.unk_byte      = r.u8()
    rec.unk_float_a   = r.f32()
    rec.unk_float_b   = r.f32()
    rec.fixed_zero    = r.u32()
    rec.old_id        = r.u32()
    rec.unk_dword_a   = r.u32()
    rec.unk_dword_b   = r.u32()
    rec.unk_byte_2    = r.u8()
    rec.unk_float_c   = r.f32()
    rec.unk_dword_c   = r.u32()
    rec.light_float_a = r.f32()
    rec.light_float_b = r.f32()
    rec.unk_dword_d   = r.u32()
    rec.flags_a       = r.u64()
    rec.flags_b       = r.u64()
    rec.unk_dword_e   = r.u32()
    rec.ec_image      = r.take(24)
    rec.img2d_image   = r.take(24)

    # SUB_9: BYTE count, then count × {BYTE prop, DWORD value}
    cnt = r.u8()
    for _ in range(cnt):
        rec.props_a.append((r.u8(), r.u32()))
    # SUB_9_2: same
    cnt = r.u8()
    for _ in range(cnt):
        rec.props_b.append((r.u8(), r.u32()))
    # SUB_9_3: DWORD count, then count × {DWORD amount, DWORD id}
    cnt = r.u32()
    for _ in range(cnt):
        rec.money.append((r.u32(), r.u32()))
    # SUB_9_4: DWORD count, complex
    cnt = r.u32()
    for _ in range(cnt):
        val = r.u8()
        if val == 0:
            sub_count = r.u32()
            sub = []
            for _ in range(sub_count):
                sub.append((r.u32(), r.u32()))
            rec.sub4.append({"val": 0, "sub": sub})
        elif val == 1:
            a = r.u8()
            b = r.u32()
            rec.sub4.append({"val": 1, "a": a, "b": b})
        else:
            rec.sub4.append({"val": val, "_unhandled": True})
            break
    # SUB_9_5: BYTE count, if nonzero -> 4 DWORDs
    cnt = r.u8()
    if cnt != 0:
        rec.sitting = (r.u32(), r.u32(), r.u32(), r.u32())
    # SUB_9_6: 4 bytes RGBA
    rec.radar_rgba = (r.u8(), r.u8(), r.u8(), r.u8())
    # SUB_9_7 × 4 texture groups
    for tag in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
        rec.textures_groups.append({"tag": tag, "entries": parse_textures_group(r)})
    # SUB_9_8: BYTE count, complex per-effect
    cnt = r.u8()
    # Without RE'ing the effect dispatcher fully, we just record the rest.
    rec.effects = [{"count": cnt, "raw_rest_size": r.remaining()}]
    rec.leftover = payload[r.p:]
    return rec


def main():
    arc = UopArchive(EC / "tileart.uop")
    print(f"Loaded tileart.uop ({len(arc.entries)} entries)")
    ids = [0, 1, 100, 0x4000, 0x4001, 0x4002, 0x4100, 0x8000, 22137, 8251, 5903, 5433]
    for tid in ids:
        h = hash_name(f"build/tileart/{tid:08}.bin")
        e = arc.by_hash.get(h)
        if e is None:
            print(f"\n--- tile {tid}: MISS")
            continue
        payload = arc.read(e)
        try:
            rec = parse_record(payload)
        except Exception as ex:
            print(f"\n--- tile {tid}: PARSE ERROR @ size={len(payload)}  {ex}")
            print(f"    head: {payload[:48].hex(' ')}")
            continue
        ok = (rec.tile_id == tid)
        print(f"\n--- tile {tid} (size={len(payload)}, leftover={len(rec.leftover)}) ---  {'OK' if ok else 'TileID MISMATCH'}")
        print(f"  ver={rec.version}  string_id={rec.string_id}  tile_id={rec.tile_id}  old_id={rec.old_id}")
        print(f"  unk_bool={rec.unk_bool} unk_byte={rec.unk_byte} unk_byte_2={rec.unk_byte_2}")
        print(f"  floats: a={rec.unk_float_a:.3f} b={rec.unk_float_b:.3f} c={rec.unk_float_c:.3f}  "
              f"light=({rec.light_float_a:.3f}, {rec.light_float_b:.3f})")
        print(f"  flags_a=0x{rec.flags_a:016X}  flags_b=0x{rec.flags_b:016X}")
        print(f"  props_a({len(rec.props_a)}): "
              + ", ".join(f"{PROP_NAMES.get(p,'?'+str(p))}={v}" for p, v in rec.props_a))
        print(f"  props_b({len(rec.props_b)}): "
              + ", ".join(f"{PROP_NAMES.get(p,'?'+str(p))}={v}" for p, v in rec.props_b))
        if rec.money:
            print(f"  money: {rec.money}")
        if rec.sub4:
            print(f"  sub4: {rec.sub4}")
        if rec.sitting:
            print(f"  sitting: {rec.sitting}")
        print(f"  radar RGBA: {rec.radar_rgba}")
        for grp in rec.textures_groups:
            print(f"  tex[{grp['tag']}]: {grp['entries']}")
        print(f"  effects: {rec.effects}")
        if rec.leftover:
            print(f"  LEFTOVER ({len(rec.leftover)}B): {rec.leftover[:40].hex(' ')}…")


if __name__ == "__main__":
    main()
