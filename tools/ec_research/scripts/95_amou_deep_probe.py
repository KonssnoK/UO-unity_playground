"""Deep probe of the AMOU payload structure."""
import io, struct, sys
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
archives = [UopArchive(EC / f"AnimationFrame{i}.uop") for i in range(1, 7)]

def fetch(body, action):
    key = f"build/animationframe/{body:06}/{action:02}.bin"
    h = hash_name(key)
    for arc in archives:
        e = arc.by_hash.get(h)
        if e: return arc.read(e), arc
    return None, None

SAMPLES = [(400, 0), (400, 1), (400, 4), (1, 0), (50, 0), (200, 0), (300, 0)]

records = []
for body, action in SAMPLES:
    data, _ = fetch(body, action)
    if data is None: continue
    records.append((body, action, data))
    print(f'sample body={body} action={action}: {len(data)} bytes')

print()
ref_body, ref_act, ref = records[0]
print(f'=== Comparing all to ref body={ref_body},action={ref_act} ===')
for body, action, data in records[1:]:
    N = min(len(data), len(ref), 256)
    diffs = [i for i in range(N) if data[i] != ref[i]]
    print(f'  body={body},action={action}: first-256 differs at {len(diffs)} positions: {diffs[:12]}')

print()
print(f'=== Annotated body={ref_body},action={ref_act} ({len(ref)} bytes) ===')
print('--- header (32B) ---')
def U16(o): return struct.unpack_from("<H", ref, o)[0]
def U32(o): return struct.unpack_from("<I", ref, o)[0]
def I16(o): return struct.unpack_from("<h", ref, o)[0]
print(f'  [00] magic={ref[:4]!r}')
print(f'  [04] version u32 = {U32(4)}')
print(f'  [08] dsize u32 = {U32(8)}')
print(f'  [0c] count u32 = {U32(0xC)}')
print(f'  [10] bbox_min = ({I16(0x10)}, {I16(0x12)})')
print(f'  [14] bbox_max = ({I16(0x14)}, {I16(0x16)})')
print(f'  [18] atlas_w u16 = {U16(0x18)}  pad u16 = {U16(0x1a)}  atlas_h u32 = {U32(0x1c)}')

print('--- post-header @ 0x20 ---')
print(f'  [20] u32 = 0x{U32(0x20):08X} = {U32(0x20)}')
print(f'  [24] u32 = 0x{U32(0x24):08X} = {U32(0x24)}')
print(f'  [28] bytes = {tuple(ref[0x28:0x2C])}')
print(f'  [2c] bytes = {tuple(ref[0x2C:0x30])}')

print('--- 32 4-byte tuples from 0x30 (palette?) ---')
for i in range(32):
    off = 0x30 + i*4
    if off + 4 > len(ref): break
    b = ref[off:off+4]
    print(f'  +0x{off:04X}: {b.hex()}  R=0x{b[0]:02x} G=0x{b[1]:02x} B=0x{b[2]:02x} A=0x{b[3]:02x}')

# Test palette-size hypothesis
print()
n_pal_count = U32(0x20)  # 0x32 = 50 in our sample
n_pal_bytes = U32(0x24)  # 0x428 = 1064
print(f'  IF u32@0x20 ({n_pal_count}) is palette entry count → palette ends at 0x{0x30 + n_pal_count*4:X}')
print(f'  IF u32@0x24 ({n_pal_bytes}) is palette byte size → palette ends at 0x{0x30 + n_pal_bytes:X}')

# Print bytes around both candidate end points
for label, end in [('@count*4', 0x30 + n_pal_count*4), ('@byte-size', 0x30 + n_pal_bytes)]:
    if end + 32 > len(ref): continue
    print(f'  bytes at end-of-pal {label} (0x{end:X}): {ref[end:end+32].hex()}')

# Cross-validate: do all the 4-byte tuples within the first 0x428 bytes after 0x30
# look like RGB triples (each entry's 4th byte mostly 0)?
print()
print('--- 4th-byte distribution in proposed palette region (0x30..0x30+0x428) ---')
pal_region = ref[0x30:0x30 + n_pal_bytes]
fourth_bytes = Counter(pal_region[3::4])
print(f'  4th-byte values, top 8: {fourth_bytes.most_common(8)}')

for a in archives:
    a.close()
