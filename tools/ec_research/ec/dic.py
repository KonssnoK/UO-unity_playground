"""Mythic Package Editor Dictionary.dic loader.

Format (from HashDictionary.cs):
  magic        : 4 bytes = b'DIC\\0'
  version      : 1 byte
  records*:
    hash       : uint64 LE
    has_name   : uint8  (1 = name follows, 0 = unknown name)
    name       : .NET BinaryWriter string format = LEB128 length + UTF-8 bytes
"""
from __future__ import annotations

import struct
from pathlib import Path


def _read_7bit_int(buf: bytes, i: int) -> tuple[int, int]:
    """.NET BinaryReader.Read7BitEncodedInt."""
    n = 0
    shift = 0
    while True:
        b = buf[i]
        i += 1
        n |= (b & 0x7F) << shift
        if (b & 0x80) == 0:
            return n, i
        shift += 7
        if shift > 35:
            raise ValueError("bad 7bit int")


def load_dictionary(path: str | Path) -> dict[int, str | None]:
    data = Path(path).read_bytes()
    if data[:4] != b"DIC\0":
        raise ValueError(f"bad magic {data[:4]!r}")
    i = 4
    _version = data[i]
    i += 1
    out: dict[int, str | None] = {}
    n = len(data)
    while i + 9 <= n:
        h = struct.unpack_from("<Q", data, i)[0]
        i += 8
        has_name = data[i]
        i += 1
        if has_name == 1:
            length, i = _read_7bit_int(data, i)
            name = data[i:i + length].decode("utf-8", errors="replace")
            i += length
            if h not in out:
                out[h] = name
        elif has_name == 0:
            if h not in out:
                out[h] = None
        else:
            raise ValueError(f"bad has_name byte 0x{has_name:02X} at offset 0x{i-1:X}")
    return out
