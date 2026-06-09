"""Dump the raw bytes of the SUB_9_7 region for several tiles so we can
visually pick out the actual entry layout (rather than assume u32+u32)."""

from __future__ import annotations

import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


class R:
    def __init__(self, buf): self.buf, self.p = buf, 0
    def u8(self):  v = self.buf[self.p]; self.p += 1; return v
    def u16(self): v = struct.unpack_from("<H", self.buf, self.p)[0]; self.p += 2; return v
    def u32(self): v = struct.unpack_from("<I", self.buf, self.p)[0]; self.p += 4; return v

    def skip_to_sub_9_7(self):
        self.p = 0x7D
        # SUB_9
        cnt = self.u8(); self.p += cnt * 5
        # SUB_9_2
        cnt = self.u8(); self.p += cnt * 5
        # SUB_9_3
        cnt = self.u32(); self.p += cnt * 8
        # SUB_9_4
        cnt = self.u32()
        for _ in range(cnt):
            val = self.u8()
            if val == 0:
                sub = self.u32(); self.p += sub * 8
            elif val == 1:
                self.p += 5
            else:
                break
        # SUB_9_5
        sitting = self.u8()
        if sitting != 0: self.p += 16
        # SUB_9_6 (RGBA)
        self.p += 4


def main():
    arc = UopArchive(EC / "tileart.uop")
    ids = [19674, 19672, 19661, 19683, 19680, 16384, 16640, 22137, 8251, 5903]
    for tid in ids:
        h = hash_name(f"build/tileart/{tid:08}.bin")
        e = arc.by_hash.get(h)
        if e is None:
            print(f"\nID {tid}: MISS"); continue
        payload = arc.read(e)
        r = R(payload)
        try:
            r.skip_to_sub_9_7()
        except Exception as ex:
            print(f"\nID {tid}: header parse failed {ex}"); continue
        start = r.p
        # capture next 80 bytes of sub_9_7 region for inspection
        chunk = payload[start: start + 80]
        print(f"\nID {tid}: SUB_9_7 starts at 0x{start:X}  payload_size={len(payload)}")
        print(f"  hex: {chunk.hex(' ')}")
        # Annotate: per-group u8 count + N bytes worth of entries.
        p = 0
        for grp_name in ("WorldArt", "TileArtLegacy", "TileArtEnhanced", "Textures"):
            cnt = chunk[p]
            print(f"  {grp_name} cnt={cnt} @ +{p}")
            p += 1
            if cnt == 0:
                continue
            # try 8/12/16/20 byte entries — show what each reading would yield
            for entry_size in (8, 12, 16, 20):
                if p + entry_size > len(chunk):
                    continue
                entry_bytes = chunk[p: p + entry_size]
                u32s = struct.unpack_from(f"<{entry_size // 4}I", entry_bytes)
                print(f"    if entry_size={entry_size}: first entry = u32s {u32s}")
            # default: skip 8 bytes per entry
            p += cnt * 8
    arc.close()


if __name__ == "__main__":
    main()
