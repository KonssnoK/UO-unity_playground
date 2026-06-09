"""Dump the surrounding 160 bytes for each occurrence of key tokens."""
from pathlib import Path

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
data = (EC / "UOSA.exe").read_bytes()

TOKENS = [
    b"TileArtEnhanced",
    b"TileArtLegacy",
    b"GumpArtMask",
    b"AnimationFrame",
    b"MobAnimTexture",
    b"AnimationLegacyFrameSet",
    b"AnimationFrameSet",
    b"EffectTexture",
    b"build/tileart",
    b"build/animation",
]

for tok in TOKENS:
    print(f"\n=== {tok.decode()} ===")
    i = 0
    count = 0
    while True:
        j = data.find(tok, i)
        if j < 0:
            break
        ctx = data[max(0, j - 70): j + len(tok) + 90]
        view = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
        print(f"  @ 0x{j:X}: {view}")
        i = j + 1
        count += 1
        if count >= 10:
            print("  (cap)")
            break
