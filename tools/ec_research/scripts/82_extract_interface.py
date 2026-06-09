"""Extract Interface.uop (Lua + XML) and grep for RequestTileArt usage —
the Lua scripts are where EC actually draws tileart on screen.
"""
import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = Path(__file__).resolve().parent.parent / "out" / "interface"
OUT.mkdir(parents=True, exist_ok=True)

arc = UopArchive(EC / "Interface.uop")
print(f"{len(arc.entries)} entries; extracting...")

# We don't have filenames since UOP keys by hash. Save by index + content type.
counters = {"lua": 0, "xml": 0, "other": 0}
hits_by_name = {}
import re
TILEART_RE = re.compile(rb"(RequestTileArt|RequestLegacyTileArt|ReleaseTileArt|tileart|TileArt|UOEC_SIZE|UOCC_SIZE)", re.IGNORECASE)

for i, e in enumerate(arc.entries):
    try:
        data = arc.read(e)
    except Exception:
        continue
    if not data: continue
    head = data[:200].lower()
    if b"<?xml" in head[:20] or head.startswith(b"<modulefile"):
        ext = "xml"
    elif head.startswith(b"--") or b"function " in head or b"end\n" in data[:300]:
        ext = "lua"
    else:
        ext = "bin"
    name = f"e{i:05}.{ext}"
    (OUT / name).write_bytes(data)
    counters[ext if ext != "bin" else "other"] = counters.get(ext if ext != "bin" else "other", 0) + 1

    # Check for tileart references
    if TILEART_RE.search(data):
        hits_by_name[name] = data

arc.close()
print(f"counters: {counters}")
print(f"files referencing TileArt: {len(hits_by_name)}")
for name in sorted(hits_by_name)[:20]:
    print(f"  {name}")
print(f"\\nOutput dir: {OUT.resolve()}")
