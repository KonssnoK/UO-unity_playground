//Copyright (c) 2012-2014 Lorenzo Consolaro
//
// Rewritten for Unity 6 (CoreCLR) - removed System.Drawing dependency.
// Unity natively supports DXT1/DXT5, so we just parse the DDS header
// and extract raw texture data for direct use with Texture2D.LoadRawTextureData().

using System;
using System.IO;
using UnityEngine;

namespace KUtility {
	public class DDSImage {
		private const int DDPF_ALPHAPIXELS = 0x00000001;
		private const int DDPF_ALPHA = 0x00000002;
		private const int DDPF_FOURCC = 0x00000004;
		private const int DDPF_RGB = 0x00000040;
		private const int DDPF_YUV = 0x00000200;
		private const int DDPF_LUMINANCE = 0x00020000;
		private const int DDSD_MIPMAPCOUNT = 0x00020000;
		private const int FOURCC_DXT1 = 0x31545844;
		private const int FOURCC_DX10 = 0x30315844;
		private const int FOURCC_DXT5 = 0x35545844;

		public int width;
		public int height;
		public TextureFormat format;
		public byte[] rawTextureData;

		public DDSImage(byte[] rawdata) {
			using (MemoryStream ms = new MemoryStream(rawdata)) {
				using (BinaryReader r = new BinaryReader(ms)) {
					int dwMagic = r.ReadInt32();
					if (dwMagic != 0x20534444) {
						throw new Exception("This is not a DDS!");
					}

					DDS_HEADER header = new DDS_HEADER();
					Read_DDS_HEADER(header, r);

					if (((header.ddspf.dwFlags & DDPF_FOURCC) != 0) && (header.ddspf.dwFourCC == FOURCC_DX10)) {
						throw new Exception("DX10 not supported yet!");
					}

					width = header.dwWidth;
					height = header.dwHeight;

					// Determine format and data size
					int dataSize;
					if ((header.ddspf.dwFlags & DDPF_RGB) != 0) {
						format = TextureFormat.ARGB32;
						dataSize = width * height * 4;
					} else if ((header.ddspf.dwFlags & DDPF_FOURCC) != 0) {
						switch (header.ddspf.dwFourCC) {
							case FOURCC_DXT1:
								format = TextureFormat.DXT1;
								dataSize = Mathf.Max(1, (width + 3) / 4) * Mathf.Max(1, (height + 3) / 4) * 8;
								break;
							case FOURCC_DXT5:
								format = TextureFormat.DXT5;
								dataSize = Mathf.Max(1, (width + 3) / 4) * Mathf.Max(1, (height + 3) / 4) * 16;
								break;
							default:
								throw new Exception(string.Format("0x{0} texture compression not implemented.", header.ddspf.dwFourCC.ToString("X")));
						}
					} else {
						// V8U8 or other - fall back to ARGB32
						format = TextureFormat.ARGB32;
						dataSize = width * height * 4;
					}

					// Use PitchOrLinearSize if available, otherwise use calculated size
					if (header.dwPitchOrLinearSize > 0 && (header.ddspf.dwFlags & DDPF_FOURCC) != 0) {
						dataSize = header.dwPitchOrLinearSize;
					}

					// For compressed formats (DXT1/DXT5), read raw data and flip vertically
					// DDS stores top-to-bottom, Unity expects bottom-to-top
					if (format == TextureFormat.DXT1 || format == TextureFormat.DXT5) {
						rawTextureData = r.ReadBytes(dataSize);
						rawTextureData = FlipDXTVertically(rawTextureData, width, height, format);
					} else if ((header.ddspf.dwFlags & DDPF_RGB) != 0) {
						// Uncompressed ARGB - read and convert to Unity's RGBA32
						format = TextureFormat.RGBA32;
						int pixelCount = width * height;
						int bytesPerPixel = header.ddspf.dwRGBBitCount / 8;
						byte[] srcData = r.ReadBytes(pixelCount * bytesPerPixel);
						rawTextureData = new byte[pixelCount * 4];
						for (int i = 0; i < pixelCount; i++) {
							int srcIdx = i * bytesPerPixel;
							int dstIdx = i * 4;
							if (bytesPerPixel >= 3) {
								rawTextureData[dstIdx + 0] = srcData[srcIdx + 2]; // R
								rawTextureData[dstIdx + 1] = srcData[srcIdx + 1]; // G
								rawTextureData[dstIdx + 2] = srcData[srcIdx + 0]; // B
								rawTextureData[dstIdx + 3] = bytesPerPixel >= 4 ? srcData[srcIdx + 3] : (byte)255; // A
							}
						}
					} else {
						// V8U8 normal map - convert to RGBA
						format = TextureFormat.RGBA32;
						rawTextureData = new byte[width * height * 4];
						for (int i = 0; i < width * height; i++) {
							sbyte red = r.ReadSByte();
							sbyte green = r.ReadSByte();
							rawTextureData[i * 4 + 0] = (byte)(0x7F - red);
							rawTextureData[i * 4 + 1] = (byte)(0x7F - green);
							rawTextureData[i * 4 + 2] = 0xFF;
							rawTextureData[i * 4 + 3] = 0xFF;
						}
					}
				}
			}
		}

		/// <summary>
		/// Flips DXT compressed texture data vertically.
		/// Swaps rows of 4x4 blocks and flips the pixel rows within each block.
		/// </summary>
		private static byte[] FlipDXTVertically(byte[] data, int w, int h, TextureFormat fmt) {
			int blockSize = (fmt == TextureFormat.DXT1) ? 8 : 16;
			int blocksPerRow = Mathf.Max(1, (w + 3) / 4);
			int blockRows = Mathf.Max(1, (h + 3) / 4);
			int rowSize = blocksPerRow * blockSize;

			byte[] flipped = new byte[data.Length];

			for (int row = 0; row < blockRows; row++) {
				int srcOffset = row * rowSize;
				int dstOffset = (blockRows - 1 - row) * rowSize;

				for (int col = 0; col < blocksPerRow; col++) {
					int src = srcOffset + col * blockSize;
					int dst = dstOffset + col * blockSize;

					if (fmt == TextureFormat.DXT1) {
						// Copy color endpoints (4 bytes)
						Buffer.BlockCopy(data, src, flipped, dst, 4);
						// Flip the 4 row bytes (each byte = 1 row of 4 pixels, 2 bits each)
						flipped[dst + 4] = data[src + 7];
						flipped[dst + 5] = data[src + 6];
						flipped[dst + 6] = data[src + 5];
						flipped[dst + 7] = data[src + 4];
					} else {
						// DXT5: flip alpha block (8 bytes) then color block (8 bytes)
						// Alpha endpoints (2 bytes)
						flipped[dst + 0] = data[src + 0];
						flipped[dst + 1] = data[src + 1];
						// Alpha indices: 6 bytes = 16 x 3-bit indices, 4 rows of 4
						// Each row = 12 bits. Rows are packed across bytes.
						FlipDXT5Alpha(data, src + 2, flipped, dst + 2);
						// Color block (same as DXT1)
						Buffer.BlockCopy(data, src + 8, flipped, dst + 8, 4);
						flipped[dst + 12] = data[src + 15];
						flipped[dst + 13] = data[src + 14];
						flipped[dst + 14] = data[src + 13];
						flipped[dst + 15] = data[src + 12];
					}
				}
			}
			return flipped;
		}

		/// <summary>
		/// Flips the 4 rows of 3-bit alpha indices in a DXT5 alpha block.
		/// 6 bytes = 48 bits = 16 x 3-bit values arranged in 4 rows of 4.
		/// </summary>
		private static void FlipDXT5Alpha(byte[] src, int srcOff, byte[] dst, int dstOff) {
			// Read 48 bits as a ulong
			ulong bits = 0;
			for (int i = 0; i < 6; i++) {
				bits |= (ulong)src[srcOff + i] << (8 * i);
			}

			// Extract 4 rows of 4x3-bit values (12 bits per row)
			ulong row0 = bits & 0xFFF;
			ulong row1 = (bits >> 12) & 0xFFF;
			ulong row2 = (bits >> 24) & 0xFFF;
			ulong row3 = (bits >> 36) & 0xFFF;

			// Reassemble with rows flipped
			ulong flipped = row3 | (row2 << 12) | (row1 << 24) | (row0 << 36);

			for (int i = 0; i < 6; i++) {
				dst[dstOff + i] = (byte)(flipped >> (8 * i));
			}
		}

		private void Read_DDS_HEADER(DDS_HEADER h, BinaryReader r) {
			h.dwSize = r.ReadInt32();
			h.dwFlags = r.ReadInt32();
			h.dwHeight = r.ReadInt32();
			h.dwWidth = r.ReadInt32();
			h.dwPitchOrLinearSize = r.ReadInt32();
			h.dwDepth = r.ReadInt32();
			h.dwMipMapCount = r.ReadInt32();
			for (int i = 0; i < 11; ++i) {
				h.dwReserved1[i] = r.ReadInt32();
			}
			Read_DDS_PIXELFORMAT(h.ddspf, r);
			h.dwCaps = r.ReadInt32();
			h.dwCaps2 = r.ReadInt32();
			h.dwCaps3 = r.ReadInt32();
			h.dwCaps4 = r.ReadInt32();
			h.dwReserved2 = r.ReadInt32();
		}

		private void Read_DDS_PIXELFORMAT(DDS_PIXELFORMAT p, BinaryReader r) {
			p.dwSize = r.ReadInt32();
			p.dwFlags = r.ReadInt32();
			p.dwFourCC = r.ReadInt32();
			p.dwRGBBitCount = r.ReadInt32();
			p.dwRBitMask = r.ReadInt32();
			p.dwGBitMask = r.ReadInt32();
			p.dwBBitMask = r.ReadInt32();
			p.dwABitMask = r.ReadInt32();
		}
	}

	class DDS_HEADER {
		public int dwSize;
		public int dwFlags;
		public int dwHeight;
		public int dwWidth;
		public int dwPitchOrLinearSize;
		public int dwDepth;
		public int dwMipMapCount;
		public int[] dwReserved1 = new int[11];
		public DDS_PIXELFORMAT ddspf = new DDS_PIXELFORMAT();
		public int dwCaps;
		public int dwCaps2;
		public int dwCaps3;
		public int dwCaps4;
		public int dwReserved2;
	}

	class DDS_PIXELFORMAT {
		public int dwSize;
		public int dwFlags;
		public int dwFourCC;
		public int dwRGBBitCount;
		public int dwRBitMask;
		public int dwGBitMask;
		public int dwBBitMask;
		public int dwABitMask;

		public DDS_PIXELFORMAT() {
		}
	}
}
