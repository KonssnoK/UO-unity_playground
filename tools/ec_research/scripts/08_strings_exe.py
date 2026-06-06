"""Pull printable strings from UOSA.exe and grep for naming-pattern fragments."""
import re
import sys
from pathlib import Path

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

KEY_PATTERNS = [
    re.compile(rb"build/[\w./%-]+"),
    re.compile(rb"[\w/]*legacy[\w/]*"),
    re.compile(rb"[\w/]*texture[\w/]*", re.I),
    re.compile(rb"[\w/]*animation[\w/]*", re.I),
    re.compile(rb"[\w/]*terrain[\w/]*", re.I),
    re.compile(rb"[\w/]+\.(dds|tga|bin|dat|amou|tex)"),
    re.compile(rb"%[0-9]+[dxX]"),
]

ASCII_STRING_RE = re.compile(rb"[\x20-\x7E]{6,}")
WIDE_STRING_RE = re.compile(rb"(?:[\x20-\x7E]\x00){6,}")


def extract(path: Path):
    data = path.read_bytes()
    out = set()
    for m in ASCII_STRING_RE.findall(data):
        out.add(m)
    for m in WIDE_STRING_RE.findall(data):
        try:
            out.add(m.decode('utf-16-le').encode('ascii'))
        except Exception:
            pass
    return out


for exe_name in ["UOSA.exe", "UOSA_TC.exe"]:
    p = EC / exe_name
    if not p.exists():
        print(f"missing: {p}")
        continue
    print(f"\n=== {p.name}: {p.stat().st_size} bytes ===")
    strings = extract(p)
    hits: set[bytes] = set()
    for s in strings:
        for pat in KEY_PATTERNS:
            for m in pat.findall(s):
                if 4 <= len(m) <= 200:
                    hits.add(m)
    for s in sorted(hits):
        print(f"  {s.decode('ascii', errors='replace')!r}")
