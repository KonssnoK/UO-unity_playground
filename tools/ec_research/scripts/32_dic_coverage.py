"""Load Dictionary.dic and compute name-coverage across every EC UOP archive."""
import sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive, hash_name
from ec.dic import load_dictionary

DIC = HERE / "Dictionary.dic"
EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")


def main():
    mapping = load_dictionary(DIC)
    named = sum(1 for v in mapping.values() if v is not None)
    print(f"Dictionary: {len(mapping)} hashes, {named} with names ({100*named/len(mapping):.1f}%)")

    # Verify Jenkins matches
    ok = bad = 0
    for h, n in mapping.items():
        if n is None:
            continue
        try:
            if hash_name(n) == h:
                ok += 1
            else:
                bad += 1
        except UnicodeEncodeError:
            bad += 1
        if ok + bad >= 5000:
            break
    print(f"Sanity-check Jenkins on first 5k: {ok} ok, {bad} bad")

    archives = sorted(p.name for p in EC.glob("*.uop"))
    print(f"\nProcessing {len(archives)} UOPs:")
    grand_total = grand_known = 0
    by_arc: list[tuple[str, int, int, Counter]] = []
    for arc_name in archives:
        try:
            arc = UopArchive(EC / arc_name)
        except Exception as e:
            print(f"  {arc_name}: skip ({e})")
            continue
        total = len(arc.by_hash)
        known = 0
        prefixes: Counter = Counter()
        for h in arc.by_hash.keys():
            n = mapping.get(h)
            if n:
                known += 1
                # bucket by first-two path components
                head = "/".join(n.split("/")[:2])
                prefixes[head] += 1
        arc.close()
        by_arc.append((arc_name, total, known, prefixes))
        grand_total += total
        grand_known += known

    for name, total, known, prefixes in by_arc:
        pct = 100 * known / total if total else 0
        print(f"\n  {name:32s} {known:6d}/{total:6d} ({pct:5.1f}%)")
        for prefix, count in prefixes.most_common(4):
            print(f"      {prefix:40s} {count}")
    pct = 100 * grand_known / grand_total
    print(f"\nGRAND TOTAL: {grand_known}/{grand_total} ({pct:.1f}%)")


if __name__ == "__main__":
    main()
