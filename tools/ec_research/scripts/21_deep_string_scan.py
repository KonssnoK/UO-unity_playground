"""Deep, broader string scan of UOSA.exe.

Pull ALL ASCII + UTF-16-LE strings, then categorize:
  - Any string containing `%` placeholder (printf templates)
  - Any string ending in .dds / .tex / .tga / .bin / .csv / .xml / .uop / .amou
  - Any string containing '/' or '\\' AND a known asset-domain token
  - Any string starting with 'build/', 'Build/', 'build\\', 'Build\\', 'data/'
Print every unique candidate so we can spot path templates.
"""
import re
import sys
from collections import Counter
from pathlib import Path

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
EXE = EC / "UOSA.exe"

data = EXE.read_bytes()
print(f"Loaded {len(data)} bytes from {EXE.name}")

# ASCII strings (min 4 chars to catch short folder names)
ascii_strs = set(m.decode('latin-1') for m in re.findall(rb"[\x20-\x7E]{4,}", data))
# UTF-16-LE strings (typical for Windows resources)
wide_strs = set()
for m in re.findall(rb"(?:[\x20-\x7E]\x00){4,}", data):
    try:
        wide_strs.add(m.decode('utf-16-le'))
    except Exception:
        pass

print(f"ASCII strings: {len(ascii_strs)};  Wide strings: {len(wide_strs)}")
all_strs = ascii_strs | wide_strs

# Bucket 1: printf templates with placeholders
fmt_templates = sorted({s for s in all_strs if "%" in s and ("/" in s or "\\" in s) and len(s) < 200})
# Bucket 2: file-extension strings that look like paths
ext_re = re.compile(r"\.(?:dds|tex|tga|bin|csv|xml|uop|amou|stx|bmp|raw|wav|mp3)$", re.I)
path_strs = sorted({s for s in all_strs if ext_re.search(s) and len(s) < 200 and len(s) >= 5})
# Bucket 3: things that look like UOP-internal paths
internal_paths = sorted({s for s in all_strs
                        if (s.startswith(("build/", "Build/", "build\\", "Build\\", "data/", "Data/"))
                            and len(s) < 200)})
# Bucket 4: strings containing 'TileArt' / 'Texture' / 'LegacyTile' / 'AnimationFrame' tokens with a path separator
tok_strs = sorted({s for s in all_strs
                  if any(tok in s for tok in ["TileArt", "Texture", "LegacyTile", "AnimationFrame", "GumpArt", "MobAnim"])
                  and ("/" in s or "\\" in s) and len(s) < 200})

print("\n--- Printf path templates (% + /) ---")
for s in fmt_templates:
    print(f"  {s!r}")

print(f"\n--- Path-like strings ending with known ext (showing 80) ---")
for s in path_strs[:80]:
    print(f"  {s!r}")
print(f"  (total {len(path_strs)})")

print("\n--- UOP-internal path candidates (build/, data/, …) ---")
for s in internal_paths:
    print(f"  {s!r}")

print("\n--- Asset-token + separator strings ---")
for s in tok_strs:
    print(f"  {s!r}")
