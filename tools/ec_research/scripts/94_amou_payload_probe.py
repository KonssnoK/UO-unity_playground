"""Probe the AMOU payload past the 32-byte header. Goal: identify how the
frame pixel data is encoded — DXT block stream? PNG? Custom RLE? — so we
can plan the C# decoder."""
import struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

# Try a known body+action pair; iterate the 6 frame archives.
CANDIDATES = [
    (109, 0, "horse idle"),
    (400, 0, "human male idle"),
    (400, 1, "human male walk"),
    (1, 0, "ogre idle"),
]

archives = [UopArchive(EC / f"AnimationFrame{i}.uop") for i in range(1, 7)]

def find_entry(body, action):
    key = f"build/animationframe/{body:06}/{action:02}.bin"
    h = hash_name(key)
    for i, arc in enumerate(archives):
        e = arc.by_hash.get(h)
        if e is not None:
            return i + 1, arc, e
    return None, None, None

for body, action, name in CANDIDATES:
    idx, arc, e = find_entry(body, action)
    if e is None:
        print(f"[{body} {action}] {name}: NOT FOUND")
        continue
    data = arc.read(e)
    print(f"\n[{body} {action}] {name}: archive AnimationFrame{idx}.uop  size={len(data)}")

    # Header (32 B)
    magic = data[:4]
    version = struct.unpack_from('<I', data, 4)[0]
    dsize = struct.unpack_from('<I', data, 8)[0]
    count = struct.unpack_from('<I', data, 12)[0]
    bbox = struct.unpack_from('<4h', data, 16)
    atlas_w = struct.unpack_from('<H', data, 24)[0]
    atlas_pad = struct.unpack_from('<H', data, 26)[0]
    atlas_h = struct.unpack_from('<I', data, 28)[0]
    print(f"  header: magic={magic} version={version} dsize={dsize} count={count}")
    print(f"  bbox=(minX={bbox[0]}, minY={bbox[1]}, maxX={bbox[2]}, maxY={bbox[3]})")
    print(f"  atlas_w={atlas_w}  atlas_pad={atlas_pad}  atlas_h={atlas_h}")

    payload = data[32:]
    print(f"  payload size: {len(payload)} bytes")
    # First 64 bytes of payload, hex
    print(f"  first 64 hex: {payload[:64].hex()}")
    # Check for common signatures
    sigs = {
        b'DDS ': 'DDS texture',
        b'\x89PNG': 'PNG',
        b'DXT1': 'DXT1 bytes',
        b'DXT5': 'DXT5 bytes',
        b'OggS': 'Ogg',
    }
    for s, name2 in sigs.items():
        idx_s = payload.find(s)
        if 0 <= idx_s < 128:
            print(f"  -> signature {name2!r} at offset {idx_s}")
    # Distribution of bytes (entropy hint)
    from collections import Counter
    bc = Counter(payload[:4096])
    top = bc.most_common(5)
    total = sum(bc.values())
    print(f"  top byte freq (first 4 KiB): {[(b, c, f'{100*c/total:.1f}%') for b, c in top]}")

for a in archives:
    a.close()
