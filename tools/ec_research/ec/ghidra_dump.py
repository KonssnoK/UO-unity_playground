"""Random-access reader for the full-binary Ghidra dump produced by FullDump.java.

The dump is stored as JSONL (one decompiled function per line) plus a sidecar
index mapping entry address -> line number. This module gives constant-time
lookup by address and convenience queries (callees, callers, strings).

Usage:

    from ec.ghidra_dump import GhidraDump
    g = GhidraDump.open()   # uses tools/ghidra/ghidra_full.jsonl by default
    fn = g.by_addr("00a72320")
    print(fn["decompiled"])
    for callee in g.callees("0051a840"):
        print(callee["entry"], callee["name"])

If the dump is too large to fit in memory, the JSONL is mmap'd and each entry
is parsed on demand. Lookups by address are O(1) via the line-offset index.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Iterable, Optional


_DEFAULT_JSONL = Path(__file__).resolve().parent.parent / "../ghidra/ghidra_full.jsonl"
_DEFAULT_INDEX = Path(__file__).resolve().parent.parent / "../ghidra/ghidra_full_index.json"


class GhidraDump:
    def __init__(self, jsonl_path: Path, index_path: Path):
        self.jsonl_path = Path(jsonl_path)
        self.index_path = Path(index_path)
        # Map: hex address (lowercase, no leading zeros stripped) -> byte offset in jsonl
        self._offsets: dict[str, int] = {}
        self._name_to_addr: dict[str, list[str]] = {}
        self._load_index()

    @classmethod
    def open(cls,
             jsonl_path: Optional[os.PathLike] = None,
             index_path: Optional[os.PathLike] = None) -> "GhidraDump":
        jp = Path(jsonl_path) if jsonl_path else _DEFAULT_JSONL.resolve()
        ip = Path(index_path) if index_path else _DEFAULT_INDEX.resolve()
        if not jp.exists():
            raise FileNotFoundError(
                f"Ghidra full-dump not found at {jp}. "
                "Run tools/ghidra/run_full_dump.ps1 to generate it.")
        return cls(jp, ip)

    def _load_index(self) -> None:
        # The index sidecar maps entry -> line number, not byte offset.
        # That's fine — we build the byte-offset map ourselves on first open.
        # JSONL has fixed line ends so byte-offsets are constant after the
        # initial scan.
        with open(self.jsonl_path, "rb") as f:
            off = 0
            for line in f:
                # Extract entry from "entry":"..." prefix without full JSON parse.
                a = line.find(b'"entry":"')
                if a < 0:
                    off += len(line); continue
                a += len(b'"entry":"')
                b = line.find(b'"', a)
                if b < 0:
                    off += len(line); continue
                entry = line[a:b].decode("ascii")
                self._offsets[entry.lower()] = off
                off += len(line)

    def by_addr(self, addr: str) -> Optional[dict]:
        """Look up a function by its entry address (e.g. '00a72320')."""
        key = addr.lower().lstrip("0").rjust(8, "0") if len(addr.lstrip("0")) <= 8 else addr.lower()
        # Try as given + zero-padded forms; ghidra-style addresses are 8 hex chars.
        for candidate in (addr.lower(), key, addr.lower().zfill(8)):
            off = self._offsets.get(candidate)
            if off is not None:
                return self._read_at(off)
        return None

    def _read_at(self, byte_offset: int) -> dict:
        with open(self.jsonl_path, "rb") as f:
            f.seek(byte_offset)
            line = f.readline()
        return json.loads(line)

    def callees(self, addr: str) -> list[dict]:
        fn = self.by_addr(addr)
        if fn is None: return []
        return [c for c in (self.by_addr(a) for a in fn.get("callees", [])) if c is not None]

    def callers(self, addr: str) -> list[dict]:
        fn = self.by_addr(addr)
        if fn is None: return []
        return [c for c in (self.by_addr(a) for a in fn.get("callers", [])) if c is not None]

    def search_strings(self, needle: str, limit: int = 50) -> list[dict]:
        """Return functions whose `strings` array contains a substring match."""
        needle = needle.lower()
        hits: list[dict] = []
        with open(self.jsonl_path, "rb") as f:
            for line in f:
                lower = line.lower()
                if b'"strings":[' not in lower: continue
                # Quick prefilter: needle anywhere in the line.
                if needle.encode("utf-8") not in lower: continue
                obj = json.loads(line)
                for s in obj.get("strings", []):
                    if needle in s.lower():
                        hits.append(obj)
                        if len(hits) >= limit: return hits
                        break
        return hits

    def iter_all(self) -> Iterable[dict]:
        with open(self.jsonl_path, "rb") as f:
            for line in f:
                yield json.loads(line)

    def __len__(self) -> int:
        return len(self._offsets)


if __name__ == "__main__":
    import sys
    g = GhidraDump.open()
    print(f"loaded {len(g)} functions from {g.jsonl_path}")
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            fn = g.by_addr(arg)
            if fn is None:
                print(f"{arg}: NOT FOUND")
            else:
                print(f"\n=== {arg} ({fn['name']}) ===")
                print(fn.get("signature"))
                print(f"callees: {fn.get('callees', [])[:10]}")
                print(f"callers ({len(fn.get('callers', []))}): {fn.get('callers', [])[:10]}")
                print(f"strings: {fn.get('strings', [])[:5]}")
                print(fn.get("decompiled", "")[:3000])
