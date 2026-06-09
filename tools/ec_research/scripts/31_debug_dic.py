"""Debug Dictionary.dic parsing — locate the exact record framing."""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ec.uop import hash_name, UopArchive

DIC = Path(r"C:\Users\konss\Desktop\Dictionary.dic")
data = DIC.read_bytes()
print(f"File size: {len(data)}")
print(f"First 64 bytes hex: {data[:64].hex(' ')}")

# Check our two candidate names — what does Jenkins say?
for n in ["build/sectors/waypoint.bin",
          "build/animationdefinition/00000060.bin",
          "build/animationdefinition/00000061.bin"]:
    print(f"  jenkins({n!r}) = 0x{hash_name(n):016X}")

# Cross-check vs AnimationDefinition.uop: pull the hash that belongs to id 60
arc = UopArchive(r"C:\Games\Electronic Arts\Ultima Online Enhanced\AnimationDefinition.uop")
target = hash_name("build/animationdefinition/00000060.bin")
print(f"In AnimationDefinition.uop: entry exists for id 60? {target in arc.by_hash}")
arc.close()

# Dump first 200 bytes split on candidate framings
# Candidate A: [01][len_u8][name][hash_u64]   start at 0x0F
print("\n--- candidate A: [01][len][name][hash], start 0x0F ---")
i = 0x0F
for _ in range(4):
    m = data[i]
    L = data[i + 1]
    n = data[i+2:i+2+L].decode('ascii', errors='replace')
    h = struct.unpack_from("<Q", data, i + 2 + L)[0]
    j = hash_name(n)
    print(f"  i=0x{i:X}: marker=0x{m:02X} L={L} name={n!r}  stored=0x{h:016X}  jenkins=0x{j:016X}  {'OK' if h==j else 'MISMATCH'}")
    i += 2 + L + 8

# Maybe header isn't 0x0F. Locate the first 'build/' string and back-derive the framing.
idx = data.find(b"build/")
print(f"\nFirst 'build/' at offset 0x{idx:X}")
# Walk back: assume name immediately follows [01][len], so name starts at idx
# Then [01] at idx-2, [len] at idx-1
print(f"  byte before len: data[idx-2]=0x{data[idx-2]:02X}, len byte=data[idx-1]={data[idx-1]}")

# Try header = 0x10 (might be 12-byte header, not 11)
print("\n--- candidate B: header 12 bytes, start 0x10 ---")
i = 0x10
for _ in range(4):
    if data[i] != 0x01:
        print(f"  i=0x{i:X}: not a marker (0x{data[i]:02X})")
        break
    L = data[i + 1]
    n = data[i+2:i+2+L].decode('ascii', errors='replace')
    h = struct.unpack_from("<Q", data, i + 2 + L)[0]
    j = hash_name(n)
    print(f"  i=0x{i:X}: L={L} name={n!r}  stored=0x{h:016X}  jenkins=0x{j:016X}  {'OK' if h==j else 'MISMATCH'}")
    i += 2 + L + 8
