"""Emit patterns.json — machine-readable handoff for the C# port."""
import json
import sys
from dataclasses import asdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.patterns import SPECS, GAMEDATA_CRITICAL_CSVS, HASH_CONVENTION

out = {
    "hash_convention": HASH_CONVENTION.strip(),
    "gamedata_critical_csvs": GAMEDATA_CRITICAL_CSVS,
    "specs": [asdict(s) for s in SPECS],
}
out_path = HERE.parent / "out" / "uop_patterns.json"
out_path.parent.mkdir(exist_ok=True)
out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"wrote {out_path}  ({out_path.stat().st_size} bytes, {len(SPECS)} specs)")
