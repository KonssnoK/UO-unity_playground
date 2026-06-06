"""Reverse-engineer the AMOU animation frame header layout.

Sample a few AnimationFrame entries and dump the first 96 bytes plus an
attempted struct decode.
"""
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = HERE.parent / "out" / "amou"
OUT.mkdir(parents=True, exist_ok=True)

# AnimationFrame1.uop entry 0 raw bytes earlier:
#   41 4D 4F 55 01 00 00 00 14 00 01 00 90 01 00 00
#   E1 FF 9D FF 1F 00 EB FF 00 01 00 00 28 00 00 00
#
# Hypothesis layout (4-byte aligned):
#   uint32 magic    "AMOU"
#   uint32 version  1
#   uint16 unk0_lo  0x0014 (= 20, maybe frame-count?)
#   uint16 unk0_hi  0x0001
#   uint32 unk1     0x00000190 (= 400, maybe data size or width?)
#   int16  bbox_min_x = -31
#   int16  bbox_min_y = -99
#   int16  bbox_max_x = +31
#   int16  bbox_max_y = -21
#   uint16 frame_w   0x0100 = 256
#   uint16 ...       0x0000
#   uint32 frame_h   0x28 = 40
# (subsequent bytes likely color palette + pixel runs)

arc = UopArchive(EC / "AnimationFrame1.uop")
print(f"AnimationFrame1.uop entries: {len(arc.entries)}")

# Pull a handful of decompressed payloads to compare layout
samples = []
for i, (e, payload) in enumerate(arc.iter_decompressed()):
    if i >= 8:
        break
    samples.append(payload)
    print(f"\n--- entry {i}  dsize={e.decompressed_size} ---")
    print(f"  head hex: {payload[:32].hex(' ')}")
    if payload[:4] == b"AMOU":
        # parse hypothesized fields
        magic = payload[:4]
        ver,  = struct.unpack_from("<I", payload, 4)
        u_a, u_b = struct.unpack_from("<HH", payload, 8)
        u_c, = struct.unpack_from("<I", payload, 12)
        bbx0, bby0, bbx1, bby1 = struct.unpack_from("<hhhh", payload, 16)
        w, _, h = struct.unpack_from("<HHI", payload, 24)
        print(f"  ver={ver}  u_a={u_a}  u_b={u_b}  u_c={u_c}")
        print(f"  bbox=({bbx0},{bby0})..({bbx1},{bby1})  w={w}  h={h}")
arc.close()

# Save samples as binary for later inspection
for i, p in enumerate(samples):
    (OUT / f"frame_{i:02}.bin").write_bytes(p)
print(f"\nSamples saved to {OUT}")
