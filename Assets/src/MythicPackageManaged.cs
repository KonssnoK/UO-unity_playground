// Managed replacement for Mythic.Package.dll
// Uses System.IO.Compression instead of native Zlib32.dll
// Compatible with Unity 6 / .NET 6+ / CoreCLR

using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;

namespace Mythic.Package {

	public class MythicPackage {
		public List<MythicPackageBlock> Blocks { get; private set; }
		public FileInfo FileInfo { get; private set; }

		public MythicPackage(string filePath) {
			FileInfo = new FileInfo(filePath);
			Blocks = new List<MythicPackageBlock>();

			using (FileStream fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
			using (BinaryReader r = new BinaryReader(fs)) {
				// UOP header
				uint magic = r.ReadUInt32(); // MYP\0
				uint version = r.ReadUInt32();
				uint misc = r.ReadUInt32();
				long firstBlockOffset = r.ReadInt64();
				uint blockCapacity = r.ReadUInt32();
				uint fileCount = r.ReadUInt32();

				// Read blocks
				long nextBlock = firstBlockOffset;
				while (nextBlock != 0) {
					fs.Seek(nextBlock, SeekOrigin.Begin);

					uint filesInBlock = r.ReadUInt32();
					long nextBlockOffset = r.ReadInt64();

					MythicPackageBlock block = new MythicPackageBlock();

					for (int i = 0; i < filesInBlock; i++) {
						MythicPackageFile file = new MythicPackageFile();
						file.DataOffset = r.ReadInt64();
						file.HeaderLength = r.ReadUInt32();
						file.CompressedSize = r.ReadUInt32();
						file.DecompressedSize = r.ReadUInt32();
						file.FileHash = r.ReadUInt64();
						file.DataHash = r.ReadUInt32();
						file.Compression = r.ReadInt16();

						if (file.DataOffset != 0) {
							block.Files.Add(file);
						}
					}

					Blocks.Add(block);
					nextBlock = nextBlockOffset;
				}
			}
		}
	}

	public class MythicPackageBlock {
		public List<MythicPackageFile> Files { get; private set; }

		public MythicPackageBlock() {
			Files = new List<MythicPackageFile>();
		}
	}

	public class MythicPackageFile {
		public long DataOffset;
		public uint HeaderLength;
		public uint CompressedSize;
		public uint DecompressedSize;
		public ulong FileHash;
		public uint DataHash;
		public short Compression;

		public byte[] Unpack(string fullName) {
			using (FileStream fs = new FileStream(fullName, FileMode.Open, FileAccess.Read))
			using (BinaryReader r = new BinaryReader(fs)) {
				fs.Seek(DataOffset + HeaderLength, SeekOrigin.Begin);

				byte[] compressedData = r.ReadBytes((int)CompressedSize);

				// Compression: 0 = none, 1 = zlib
				if (Compression == 0 || CompressedSize == DecompressedSize) {
					return compressedData;
				}

				// Zlib compressed - skip 2-byte zlib header, then use DeflateStream
				byte[] decompressed = new byte[DecompressedSize];
				using (MemoryStream ms = new MemoryStream(compressedData, 2, compressedData.Length - 2))
				using (DeflateStream ds = new DeflateStream(ms, CompressionMode.Decompress)) {
					int totalRead = 0;
					while (totalRead < decompressed.Length) {
						int read = ds.Read(decompressed, totalRead, decompressed.Length - totalRead);
						if (read == 0) break;
						totalRead += read;
					}
				}
				return decompressed;
			}
		}
	}

	public static class HashDictionary {
		public static ulong HashFileName(string s) {
			uint eax, ecx, edx, ebx, esi, edi;
			eax = ecx = edx = ebx = esi = edi = 0;
			ebx = edi = esi = (uint)s.Length + 0xDEADBEEF;

			int i = 0;
			for (i = 0; i + 12 < s.Length; i += 12) {
				edi += (uint)(s[i + 7] << 24 | s[i + 6] << 16 | s[i + 5] << 8 | s[i + 4]);
				esi += (uint)(s[i + 11] << 24 | s[i + 10] << 16 | s[i + 9] << 8 | s[i + 8]);
				edx = (uint)(s[i + 3] << 24 | s[i + 2] << 16 | s[i + 1] << 8 | s[i]) - esi;

				edx = (edx + ebx) ^ (esi >> 28) ^ (esi << 4);
				esi += edi;
				edi = (edi - edx) ^ (edx >> 26) ^ (edx << 6);
				edx += esi;
				esi = (esi - edi) ^ (edi >> 24) ^ (edi << 8);
				edi += edx;
				ebx = (edx - esi) ^ (esi >> 16) ^ (esi << 16);
				esi += edi;
				edi = (edi - ebx) ^ (ebx >> 13) ^ (ebx << 19);
				ebx += esi;
				esi = (esi - edi) ^ (edi >> 28) ^ (edi << 4);
				edi += ebx;
			}

			if (s.Length - i > 0) {
				switch (s.Length - i) {
					case 12:
						esi += (uint)s[i + 11] << 24;
						goto case 11;
					case 11:
						esi += (uint)s[i + 10] << 16;
						goto case 10;
					case 10:
						esi += (uint)s[i + 9] << 8;
						goto case 9;
					case 9:
						esi += (uint)s[i + 8];
						goto case 8;
					case 8:
						edi += (uint)s[i + 7] << 24;
						goto case 7;
					case 7:
						edi += (uint)s[i + 6] << 16;
						goto case 6;
					case 6:
						edi += (uint)s[i + 5] << 8;
						goto case 5;
					case 5:
						edi += (uint)s[i + 4];
						goto case 4;
					case 4:
						ebx += (uint)s[i + 3] << 24;
						goto case 3;
					case 3:
						ebx += (uint)s[i + 2] << 16;
						goto case 2;
					case 2:
						ebx += (uint)s[i + 1] << 8;
						goto case 1;
					case 1:
						ebx += (uint)s[i];
						break;
				}

				esi = (esi ^ edi) - ((edi >> 18) ^ (edi << 14));
				ecx = (esi ^ ebx) - ((esi >> 21) ^ (esi << 11));
				edi = (edi ^ ecx) - ((ecx >> 7) ^ (ecx << 25));
				esi = (esi ^ edi) - ((edi >> 16) ^ (edi << 16));
				edx = (esi ^ ecx) - ((esi >> 28) ^ (esi << 4));
				edi = (edi ^ edx) - ((edx >> 18) ^ (edx << 14));
				eax = (esi ^ edi) - ((edi >> 8) ^ (edi << 24));

				return ((ulong)edi << 32) | eax;
			}

			return ((ulong)esi << 32) | eax;
		}
	}
}
