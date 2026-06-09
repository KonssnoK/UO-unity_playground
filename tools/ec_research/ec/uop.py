"""UOP container reader + Jenkins one-at-a-time hash used by UO file names.

Mirrors the algorithm in src/ClassicUO.IO/UOFileUop.cs.
"""

from __future__ import annotations

import io
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


UOP_MAGIC = 0x50594D  # 'MYP\0' little-endian


def hash_name(name: str) -> int:
    """Jenkins-like hash used to address UOP entries by virtual filename.

    Faithful port of UOFileUop.CreateHash.
    """
    b = name.encode("ascii")
    n = len(b)
    eax = 0
    ecx = 0
    edx = 0
    ebx = edi = esi = (n + 0xDEADBEEF) & 0xFFFFFFFF

    M = 0xFFFFFFFF
    i = 0
    while i + 12 < n:
        edi = (((b[i + 7] << 24) | (b[i + 6] << 16) | (b[i + 5] << 8) | b[i + 4]) + edi) & M
        esi = (((b[i + 11] << 24) | (b[i + 10] << 16) | (b[i + 9] << 8) | b[i + 8]) + esi) & M
        edx = (((b[i + 3] << 24) | (b[i + 2] << 16) | (b[i + 1] << 8) | b[i]) - esi) & M
        edx = ((edx + ebx) ^ (esi >> 28) ^ ((esi << 4) & M)) & M
        esi = (esi + edi) & M
        edi = ((edi - edx) ^ (edx >> 26) ^ ((edx << 6) & M)) & M
        edx = (edx + esi) & M
        esi = ((esi - edi) ^ (edi >> 24) ^ ((edi << 8) & M)) & M
        edi = (edi + edx) & M
        ebx = ((edx - esi) ^ (esi >> 16) ^ ((esi << 16) & M)) & M
        esi = (esi + edi) & M
        edi = ((edi - ebx) ^ (ebx >> 13) ^ ((ebx << 19) & M)) & M
        ebx = (ebx + esi) & M
        esi = ((esi - edi) ^ (edi >> 28) ^ ((edi << 4) & M)) & M
        edi = (edi + ebx) & M
        i += 12

    rem = n - i
    if rem == 0:
        return ((esi & M) << 32) | eax

    if rem >= 12: esi = (esi + ((b[i + 11] << 24) & M)) & M
    if rem >= 11: esi = (esi + ((b[i + 10] << 16) & M)) & M
    if rem >= 10: esi = (esi + ((b[i + 9] << 8) & M)) & M
    if rem >= 9:  esi = (esi + b[i + 8]) & M
    if rem >= 8:  edi = (edi + ((b[i + 7] << 24) & M)) & M
    if rem >= 7:  edi = (edi + ((b[i + 6] << 16) & M)) & M
    if rem >= 6:  edi = (edi + ((b[i + 5] << 8) & M)) & M
    if rem >= 5:  edi = (edi + b[i + 4]) & M
    if rem >= 4:  ebx = (ebx + ((b[i + 3] << 24) & M)) & M
    if rem >= 3:  ebx = (ebx + ((b[i + 2] << 16) & M)) & M
    if rem >= 2:  ebx = (ebx + ((b[i + 1] << 8) & M)) & M
    if rem >= 1:  ebx = (ebx + b[i]) & M

    esi = ((esi ^ edi) - ((edi >> 18) ^ ((edi << 14) & M))) & M
    ecx = ((esi ^ ebx) - ((esi >> 21) ^ ((esi << 11) & M))) & M
    edi = ((edi ^ ecx) - ((ecx >> 7) ^ ((ecx << 25) & M))) & M
    esi = ((esi ^ edi) - ((edi >> 16) ^ ((edi << 16) & M))) & M
    edx = ((esi ^ ecx) - ((esi >> 28) ^ ((esi << 4) & M))) & M
    edi = ((edi ^ edx) - ((edx >> 18) ^ ((edx << 14) & M))) & M
    eax = ((esi ^ edi) - ((edi >> 8) ^ ((edi << 24) & M))) & M
    return ((edi & M) << 32) | eax


@dataclass(frozen=True)
class UopEntry:
    offset: int          # absolute offset to payload (after header)
    compressed_size: int
    decompressed_size: int
    hash: int
    flag: int            # 0=none, 1=zlib, 3=zlib_bwt


class UopArchive:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._fh = open(self.path, "rb")
        self.version = 0
        self.entries: list[UopEntry] = []
        self.by_hash: dict[int, UopEntry] = {}
        self._read_index()

    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def close(self):
        if self._fh: self._fh.close(); self._fh = None

    def _read_index(self):
        f = self._fh
        f.seek(0)
        magic, version, _ts, next_block, _bs, _ch = struct.unpack("<IIIqIi", f.read(28))
        if magic != UOP_MAGIC:
            raise ValueError(f"bad uop magic 0x{magic:X}")
        self.version = version
        f.seek(next_block)
        while True:
            (files_count,) = struct.unpack("<i", f.read(4))
            (next_block,) = struct.unpack("<q", f.read(8))
            for _ in range(files_count):
                off, hl, csize, dsize, h, _dh, flag = struct.unpack("<qiiiQIh", f.read(34))
                if off == 0:
                    continue
                e = UopEntry(off + hl, csize, dsize, h, flag)
                self.entries.append(e)
                self.by_hash[h] = e
            if next_block == 0:
                break
            f.seek(next_block)

    def read(self, entry: UopEntry) -> bytes:
        self._fh.seek(entry.offset)
        data = self._fh.read(entry.compressed_size)
        if entry.flag == 1:
            return zlib.decompress(data)
        return data

    def get_by_name(self, name: str) -> bytes | None:
        e = self.by_hash.get(hash_name(name))
        return self.read(e) if e else None

    def iter_decompressed(self) -> Iterable[tuple[UopEntry, bytes]]:
        for e in self.entries:
            yield e, self.read(e)
