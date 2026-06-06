"""Parse every GameData.uop CSV and consolidate."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name
from ec.dic import load_dictionary

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
OUT = HERE.parent / "out" / "gamedata"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    mapping = load_dictionary(HERE / "Dictionary.dic")
    arc = UopArchive(EC / "GameData.uop")
    print(f"Entries: {len(arc.entries)}")
    named = unnamed = 0
    for e in arc.entries:
        n = mapping.get(e.hash)
        if n:
            named += 1
            short = n.split("/")[-1]
            (OUT / short).write_bytes(arc.read(e))
        else:
            unnamed += 1
            (OUT / f"_unnamed_{e.hash:016X}.bin").write_bytes(arc.read(e))
    arc.close()
    print(f"  named: {named}  unnamed: {unnamed}")
    # List CSVs
    for f in sorted(OUT.iterdir()):
        try:
            text = f.read_text(encoding='utf-8', errors='ignore')
            first = text.splitlines()[0] if text.splitlines() else ""
            print(f"  {f.name:40s}  {len(text):6d}B  {first[:80]}")
        except Exception:
            print(f"  {f.name}  (binary)")


if __name__ == "__main__":
    main()
