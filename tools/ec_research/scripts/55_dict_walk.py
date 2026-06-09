"""Walk string_dictionary.bin linearly using u16-length-prefixed entries.
Report whether specific offsets land at the *start* of a string entry."""
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from ec.uop import UopArchive

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
arc = UopArchive(EC / "string_dictionary.uop")
sd = arc.get_by_name("build/stringdictionary/string_dictionary.bin")
arc.close()

# Walk: header is 16 bytes, then u16 length + content repeats.
p = 16
entries = []   # list of (content_offset, length, string)
while p + 2 <= len(sd):
    length = struct.unpack_from("<H", sd, p)[0]
    if length == 0 or length > 500:
        # try advancing 1 byte to recover from misalign
        break
    content_start = p + 2
    if content_start + length > len(sd):
        break
    s = sd[content_start: content_start + length].decode("ascii", errors="replace")
    entries.append((content_start, length, s))
    p = content_start + length

print(f"walked {len(entries)} entries, stopped at offset {p} (file size {len(sd)})")
print(f"first 5: {entries[:5]}")
print(f"last  5: {entries[-5:]}")

# Now: for offsets we care about, find which entry contains them
targets = [45085, 7478, 24115, 54565, 54566, 58231]
print()
for off in targets:
    matching = None
    for cs, ln, s in entries:
        if cs == off:
            matching = ("EXACT START", cs, ln, s)
            break
        if cs <= off < cs + ln:
            matching = ("INSIDE", cs, ln, s)
            break
    if matching:
        kind, cs, ln, s = matching
        print(f"@ {off}: {kind}  start={cs}  len={ln}  string={s!r}")
    else:
        print(f"@ {off}: NOT FOUND in walked entries (parsed only first {len(entries)})")
