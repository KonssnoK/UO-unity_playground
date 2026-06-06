"""Read DAT_00c9d1a0 and DAT_00c853b4 from UOSA.exe.

PE file: parse section headers to find where .data starts in the file,
then compute the file offset of each VA. Read 4 bytes, interpret as
float and int.
"""
import struct
from pathlib import Path

EXE = Path(r"C:\Games\Electronic Arts\Ultima Online Enhanced\UOSA.exe")
data = EXE.read_bytes()

# PE header
e_lfanew = struct.unpack_from('<I', data, 0x3C)[0]
assert data[e_lfanew:e_lfanew+4] == b'PE\x00\x00'
coff = e_lfanew + 4
num_sections = struct.unpack_from('<H', data, coff + 2)[0]
opt_header_size = struct.unpack_from('<H', data, coff + 16)[0]
opt = coff + 20
image_base = struct.unpack_from('<I', data, opt + 28)[0]
print(f"image_base = 0x{image_base:08x}")
sections = opt + opt_header_size
sec_size = 40

# Build section table
def va_to_file_offset(va):
    rva = va - image_base
    for i in range(num_sections):
        s = sections + i * sec_size
        name = data[s:s+8].rstrip(b'\x00').decode()
        v_size = struct.unpack_from('<I', data, s+8)[0]
        v_addr = struct.unpack_from('<I', data, s+12)[0]
        r_size = struct.unpack_from('<I', data, s+16)[0]
        r_ptr  = struct.unpack_from('<I', data, s+20)[0]
        if v_addr <= rva < v_addr + max(v_size, r_size):
            return r_ptr + (rva - v_addr)
    return None

# Print sections
print("Sections:")
for i in range(num_sections):
    s = sections + i * sec_size
    name = data[s:s+8].rstrip(b'\x00').decode()
    v_size = struct.unpack_from('<I', data, s+8)[0]
    v_addr = struct.unpack_from('<I', data, s+12)[0]
    r_size = struct.unpack_from('<I', data, s+16)[0]
    r_ptr  = struct.unpack_from('<I', data, s+20)[0]
    print(f"  {name:>10}  VA=0x{image_base+v_addr:08x} size=0x{v_size:08x}  file=0x{r_ptr:08x}+0x{r_size:08x}")

# Read DATs
for label, va in [
    ("DAT_00c9d1a0", 0x00c9d1a0),
    ("DAT_00c853b4", 0x00c853b4),
    ("DAT_00d0a324", 0x00d0a324),
    ("DAT_00d0a0dc", 0x00d0a0dc),
    ("DAT_00d0a0d0", 0x00d0a0d0),
]:
    off = va_to_file_offset(va)
    if off is None:
        print(f"{label} @0x{va:08x}: VA not in any section")
        continue
    b = data[off:off+8]
    f = struct.unpack_from('<f', b, 0)[0]
    i = struct.unpack_from('<I', b, 0)[0]
    d8 = struct.unpack_from('<d', b, 0)[0] if len(b) >= 8 else None
    print(f"{label} @0x{va:08x} (file 0x{off:08x}): bytes={b.hex()}  float={f}  uint=0x{i:08x}={i}  double={d8}")
