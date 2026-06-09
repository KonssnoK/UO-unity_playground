"""Grep for any string containing '/%' to find path format templates."""
import re
from pathlib import Path

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")

def extract_strings(data: bytes, min_len: int = 4):
    return set(re.findall(rb"[\x20-\x7E]{%d,}" % min_len, data))

data = (EC / "UOSA.exe").read_bytes()
strings = extract_strings(data, 6)

# Match anything that contains a printf placeholder
interesting = []
for s in strings:
    if (b'%' in s) and (b'/' in s or b'\\' in s):
        try:
            interesting.append(s.decode('ascii'))
        except Exception:
            pass

print(f"Strings containing path + format spec: {len(interesting)}")
for s in sorted(set(interesting)):
    if any(t in s.lower() for t in ['texture', 'terrain', 'animation', 'tile', 'gump', 'art', 'mob', 'paperdoll', 'frame', 'build']):
        print(f"  {s!r}")
