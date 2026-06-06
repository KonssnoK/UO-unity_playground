"""Dump the raw bytes of tile 200's tileart record and search for byte
patterns that match the EXPECTED sd_off (19896, 19941, 19969 for sprite 200)
to see where in the record the right sd_off actually sits."""
from __future__ import annotations
import struct, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
ART_ID = 200 + 0x4000

tileart = UopArchive(EC / "tileart.uop")
h = hash_name(f"build/tileart/{ART_ID:08}.bin")
e = tileart.by_hash[h]
payload = tileart.read(e)
tileart.close()

print(f"tile 200 record bytes={len(payload)}")

# Hex dump full payload
print("\n--- full hex dump ---")
for i in range(0, len(payload), 16):
    chunk = payload[i:i+16]
    hexs = " ".join(f"{b:02x}" for b in chunk)
    asci = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
    print(f"  {i:04x}: {hexs:<48}  {asci}")

# Search for byte patterns matching expected sd_off
expected = [
    ("WorldArt sprite200 cs=19896", 19896),
    ("TileArtLegacy sprite200 cs=19941", 19941),
    ("TileArtEnhanced sprite200 cs=19969", 19969),
    ("Jungle466 cs=45536", 45536),
    ("Jungle466 Legacy cs=45577", 45577),
    ("Jungle466 Enhanced cs=45605", 45605),
    ("Jungle467 cs=45634 [what we got TileArtLegacy]", 45634),
    ("Jungle467 cs=45635 [TileArtEnhanced]", 45635),
]
print("\n--- searching for byte patterns matching expected sd_off LE u32 ---")
for label, val in expected:
    pat = struct.pack("<I", val)
    positions = []
    p = 0
    while True:
        idx = payload.find(pat, p)
        if idx < 0: break
        positions.append(idx)
        p = idx + 1
    print(f"  {label:<55} pat={pat.hex()} positions={positions}")
