"""Survey every entry of GameData.uop: dump first line of each decompressed payload."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = Path(__file__).resolve().parent.parent / "out" / "GameData_all"
OUT.mkdir(parents=True, exist_ok=True)

arc = UopArchive(EC / "GameData.uop")
print(f"Total: {len(arc.entries)} entries")
for i, (e, payload) in enumerate(arc.iter_decompressed()):
    head = payload[:200]
    try:
        text = head.decode('latin-1')
        first_lines = text.split("\n", 3)[:3]
        summary = " | ".join(line.strip()[:80] for line in first_lines if line.strip())
    except Exception:
        summary = "<binary>"
    print(f"  [{i:02}] csize={e.compressed_size:6d} dsize={e.decompressed_size:6d} hash=0x{e.hash:016X} :: {summary[:140]}")
    (OUT / f"{i:02}.bin").write_bytes(payload)
arc.close()
