"""Probe how SUB_9_7 names like 'Data\\TileArtEnhanced\\500.tga' map to
actual UOP entries in EC's archives."""
import sys, struct
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ec.uop import UopArchive, hash_name

EC = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced")
hd = UopArchive(EC / 'Texture.uop')
lt = UopArchive(EC / 'LegacyTexture.uop')

SEP = chr(92)  # backslash

candidates = [
    f"Data{SEP}TileArtEnhanced{SEP}500.tga",
    f"Data{SEP}TileArtEnhanced{SEP}500.dds",
    f"Data{SEP}TileArtEnhanced{SEP}00000500.dds",
    "Data/TileArtEnhanced/500.tga",
    "data/tileartenhanced/500.tga",
    "build/tileartenhanced/500.dds",
    "build/tileartenhanced/00000500.dds",
    "build/tileartenhanced/00001414.dds",
    f"Data{SEP}WorldArt{SEP}500.dds",
    f"Data{SEP}WorldArt{SEP}00000500.dds",
    f"Data{SEP}WorldArt{SEP}00001414.dds",
    "00000500.dds",
    "500.dds",
    "build/worldart/00000500.dds",
    "build/worldart/00000500_TileArt.dds",
    "build/worldart/00000500_TileArtEnhanced.dds",
]
for arc_name, arc in [("Texture.uop", hd), ("LegacyTexture.uop", lt)]:
    print(f"\n--- {arc_name} probes ---")
    for c in candidates:
        h = hash_name(c)
        if h in arc.by_hash:
            e = arc.by_hash[h]
            print(f"  HIT  {c!r}  size={e.decompressed_size}")

# Dump unique directory prefixes used in string_dictionary
sd_arc = UopArchive(EC / 'string_dictionary.uop')
sd = sd_arc.read(list(sd_arc.by_hash.values())[0])
strings = []
pos = 0
while pos + 2 < len(sd):
    n = struct.unpack_from('<H', sd, pos)[0]
    if n == 0 or n > 1024:
        pos += 1; continue
    if pos + 2 + n > len(sd):
        break
    tb = sd[pos+2:pos+2+n]
    if all(0x20 <= b < 0x80 or b in (0x09, 0x0a) for b in tb):
        strings.append(tb.decode('utf-8'))
        pos += 2 + n; continue
    pos += 1

prefixes = Counter()
for s in strings:
    if s.endswith('.tga') and SEP in s:
        head = s.rsplit(SEP, 1)[0]
        prefixes[head] += 1
print("\n--- unique .tga directories in string_dictionary ---")
for h, c in prefixes.most_common(20):
    print(f"  {c:5d}  {h}")

# Suffix samples
suffix_examples = {h: [] for h in prefixes}
for s in strings:
    if s.endswith('.tga') and SEP in s:
        head, tail = s.rsplit(SEP, 1)
        if len(suffix_examples[head]) < 3:
            suffix_examples[head].append(tail)
print("\n--- sample filenames under each prefix ---")
for h, exs in suffix_examples.items():
    print(f"  {h}{SEP} -> {exs}")

hd.close(); lt.close(); sd_arc.close()
