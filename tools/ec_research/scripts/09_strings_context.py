"""Find context around interesting tokens in the EC executable.

Look for `%08d`, `_Texture`, `_Terrain`, `_Animation` etc., and dump 80 bytes
of surrounding context to recover full asset path format strings.
"""
from pathlib import Path

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

NEEDLES = [
    b"_Texture",
    b"_Terrain",
    b"_Animation",
    b"%08d",
    b"%06d",
    b"%04d",
    b"%08x",
    b"build/",
    b"Build/",
    b"/textures",
    b"/animations",
    b".dds",
    b".tex",
    b".amou",
    b"LegacyTexture",
    b"LegacyTerrain",
    b"AnimationFrame",
]


def dump_context(path: Path):
    data = path.read_bytes()
    print(f"\n=== {path.name} ===")
    for needle in NEEDLES:
        i = 0
        seen_contexts: set[bytes] = set()
        while True:
            j = data.find(needle, i)
            if j < 0:
                break
            ctx = data[max(0, j - 50): j + len(needle) + 50]
            # printable view
            view = ''.join(chr(b) if 32 <= b < 127 else '.' for b in ctx)
            if view not in [v.decode('latin-1', errors='replace') for v in seen_contexts]:
                seen_contexts.add(ctx)
                # short trim — collapse runs of dots
                short = view
                while '....' in short:
                    short = short.replace('....', '...')
                if len(seen_contexts) <= 6:
                    print(f"  {needle!r} @ 0x{j:X}: ...{short}...")
            i = j + 1
        if seen_contexts:
            print(f"    -> {len(seen_contexts)} unique contexts for {needle!r}")


dump_context(EC / "UOSA.exe")
