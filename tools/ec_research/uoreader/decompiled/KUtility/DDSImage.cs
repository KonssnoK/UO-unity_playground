using System;
using System.Drawing;
using System.IO;

namespace KUtility;

public class DDSImage
{
	private const int m_a = 1;

	private const int m_b = 2;

	private const int m_c = 4;

	private const int m_d = 64;

	private const int m_e = 512;

	private const int f = 131072;

	private const int g = 131072;

	private const int h = 827611204;

	private const int i = 808540228;

	private const int j = 894720068;

	public int dwMagic;

	private f k = new f();

	private a l;

	public byte[] bdata;

	public byte[] bdata2;

	public Bitmap[] images;

	public DDSImage(byte[] rawdata)
	{
		using MemoryStream input = new MemoryStream(rawdata);
		using BinaryReader binaryReader = new BinaryReader(input);
		dwMagic = binaryReader.ReadInt32();
		if (dwMagic != 542327876)
		{
			throw new Exception("This is not a DDS!");
		}
		a(k, binaryReader);
		if ((k.i.b & 4) != 0 && k.i.c == 808540228)
		{
			throw new Exception("DX10 not supported yet!");
		}
		int num = 1;
		if ((k.b & 0x20000) != 0)
		{
			num = k.g;
		}
		images = new Bitmap[num];
		bdata = binaryReader.ReadBytes(k.e);
		for (int i = 0; i < num; i++)
		{
			int a_ = (int)((double)k.d / Math.Pow(2.0, i));
			int a_2 = (int)((double)k.c / Math.Pow(2.0, i));
			if ((k.i.b & 0x40) != 0)
			{
				images[i] = a(bdata, a_, a_2);
			}
			else if ((k.i.b & 4) != 0)
			{
				images[i] = e(bdata, a_, a_2);
			}
			else if ((k.i.b & 4) == 0 && k.i.d == 16 && k.i.e == 255 && k.i.f == 65280 && k.i.g == 0 && k.i.h == 0)
			{
				images[i] = b(bdata, a_, a_2);
			}
		}
	}

	private Bitmap e(byte[] A_0, int A_1, int A_2)
	{
		return k.i.c switch
		{
			827611204 => d(A_0, A_1, A_2), 
			894720068 => c(A_0, A_1, A_2), 
			_ => throw new Exception(string.Format("0x{0} texture compression not implemented.", k.i.c.ToString("X"))), 
		};
	}

	private Bitmap d(byte[] A_0, int A_1, int A_2)
	{
		Bitmap bitmap = new Bitmap((A_1 < 4) ? 4 : A_1, (A_2 < 4) ? 4 : A_2);
		using MemoryStream input = new MemoryStream(A_0);
		using BinaryReader binaryReader = new BinaryReader(input);
		for (int i = 0; i < A_2; i += 4)
		{
			for (int j = 0; j < A_1; j += 4)
			{
				b(j, i, binaryReader.ReadBytes(8), bitmap);
			}
		}
		return bitmap;
	}

	private void b(int A_0, int A_1, byte[] A_2, Bitmap A_3)
	{
		ushort num = (ushort)(A_2[0] | (A_2[1] << 8));
		ushort num2 = (ushort)(A_2[2] | (A_2[3] << 8));
		int num3 = (num >> 11) * 255 + 16;
		byte b2 = (byte)((num3 / 32 + num3) / 32);
		num3 = ((num & 0x7E0) >> 5) * 255 + 32;
		byte b3 = (byte)((num3 / 64 + num3) / 64);
		num3 = (num & 0x1F) * 255 + 16;
		byte b4 = (byte)((num3 / 32 + num3) / 32);
		num3 = (num2 >> 11) * 255 + 16;
		byte b5 = (byte)((num3 / 32 + num3) / 32);
		num3 = ((num2 & 0x7E0) >> 5) * 255 + 32;
		byte b6 = (byte)((num3 / 64 + num3) / 64);
		num3 = (num2 & 0x1F) * 255 + 16;
		byte b7 = (byte)((num3 / 32 + num3) / 32);
		uint num4 = (uint)(A_2[4] | (A_2[5] << 8) | (A_2[6] << 16) | (A_2[7] << 24));
		for (int i = 0; i < 4; i++)
		{
			for (int j = 0; j < 4; j++)
			{
				Color color = Color.FromArgb(0);
				byte b8 = (byte)((num4 >> 2 * (4 * i + j)) & 3);
				if (num > num2)
				{
					switch (b8)
					{
					case 0:
						color = Color.FromArgb(255, b2, b3, b4);
						break;
					case 1:
						color = Color.FromArgb(255, b5, b6, b7);
						break;
					case 2:
						color = Color.FromArgb(255, (2 * b2 + b5) / 3, (2 * b3 + b6) / 3, (2 * b4 + b7) / 3);
						break;
					case 3:
						color = Color.FromArgb(255, (b2 + 2 * b5) / 3, (b3 + 2 * b6) / 3, (b4 + 2 * b7) / 3);
						break;
					}
				}
				else
				{
					switch (b8)
					{
					case 0:
						color = Color.FromArgb(255, b2, b3, b4);
						break;
					case 1:
						color = Color.FromArgb(255, b5, b6, b7);
						break;
					case 2:
						color = Color.FromArgb(255, (b2 + b5) / 2, (b3 + b6) / 2, (b4 + b7) / 2);
						break;
					case 3:
						color = Color.FromArgb(255, 0, 0, 0);
						break;
					}
				}
				A_3.SetPixel(A_0 + j, A_1 + i, color);
			}
		}
	}

	private Bitmap c(byte[] A_0, int A_1, int A_2)
	{
		Bitmap bitmap = new Bitmap((A_1 < 4) ? 4 : A_1, (A_2 < 4) ? 4 : A_2);
		using MemoryStream input = new MemoryStream(A_0);
		using BinaryReader binaryReader = new BinaryReader(input);
		for (int i = 0; i < A_2; i += 4)
		{
			for (int j = 0; j < A_1; j += 4)
			{
				a(j, i, binaryReader.ReadBytes(16), bitmap);
			}
		}
		return bitmap;
	}

	private void a(int A_0, int A_1, byte[] A_2, Bitmap A_3)
	{
		byte b2 = A_2[0];
		byte b3 = A_2[1];
		int num = 2;
		uint num2 = (uint)(A_2[num + 2] | (A_2[num + 3] << 8) | (A_2[num + 4] << 16) | (A_2[num + 5] << 24));
		ushort num3 = (ushort)(A_2[num] | (A_2[num + 1] << 8));
		ushort num4 = (ushort)(A_2[8] | (A_2[9] << 8));
		ushort num5 = (ushort)(A_2[10] | (A_2[11] << 8));
		int num6 = (num4 >> 11) * 255 + 16;
		byte b4 = (byte)((num6 / 32 + num6) / 32);
		num6 = ((num4 & 0x7E0) >> 5) * 255 + 32;
		byte b5 = (byte)((num6 / 64 + num6) / 64);
		num6 = (num4 & 0x1F) * 255 + 16;
		byte b6 = (byte)((num6 / 32 + num6) / 32);
		num6 = (num5 >> 11) * 255 + 16;
		byte b7 = (byte)((num6 / 32 + num6) / 32);
		num6 = ((num5 & 0x7E0) >> 5) * 255 + 32;
		byte b8 = (byte)((num6 / 64 + num6) / 64);
		num6 = (num5 & 0x1F) * 255 + 16;
		byte b9 = (byte)((num6 / 32 + num6) / 32);
		uint num7 = (uint)(A_2[12] | (A_2[13] << 8) | (A_2[14] << 16) | (A_2[15] << 24));
		for (int i = 0; i < 4; i++)
		{
			for (int j = 0; j < 4; j++)
			{
				int num8 = 3 * (4 * i + j);
				int num9 = (int)((num8 <= 12) ? ((num3 >> num8) & 7) : ((num8 != 15) ? ((num2 >> num8 - 16) & 7) : ((num3 >> 15) | ((num2 << 1) & 6))));
				byte alpha = num9 switch
				{
					0 => b2, 
					1 => b3, 
					_ => (b2 <= b3) ? (num9 switch
					{
						6 => 0, 
						7 => byte.MaxValue, 
						_ => (byte)(((6 - num9) * b2 + (num9 - 1) * b3) / 5), 
					}) : ((byte)(((8 - num9) * b2 + (num9 - 1) * b3) / 7)), 
				};
				byte b10 = (byte)((num7 >> 2 * (4 * i + j)) & 3);
				Color color = default(Color);
				switch (b10)
				{
				case 0:
					color = Color.FromArgb(alpha, b4, b5, b6);
					break;
				case 1:
					color = Color.FromArgb(alpha, b7, b8, b9);
					break;
				case 2:
					color = Color.FromArgb(alpha, (2 * b4 + b7) / 3, (2 * b5 + b8) / 3, (2 * b6 + b9) / 3);
					break;
				case 3:
					color = Color.FromArgb(alpha, (b4 + 2 * b7) / 3, (b5 + 2 * b8) / 3, (b6 + 2 * b9) / 3);
					break;
				}
				A_3.SetPixel(A_0 + j, A_1 + i, color);
			}
		}
	}

	private Bitmap b(byte[] A_0, int A_1, int A_2)
	{
		Bitmap bitmap = new Bitmap(A_1, A_2);
		using MemoryStream input = new MemoryStream(A_0);
		using BinaryReader binaryReader = new BinaryReader(input);
		for (int i = 0; i < A_2; i++)
		{
			for (int j = 0; j < A_1; j++)
			{
				sbyte b2 = binaryReader.ReadSByte();
				sbyte b3 = binaryReader.ReadSByte();
				byte blue = byte.MaxValue;
				bitmap.SetPixel(j, i, Color.FromArgb(127 - b2, 127 - b3, blue));
			}
		}
		return bitmap;
	}

	private Bitmap a(byte[] A_0, int A_1, int A_2)
	{
		Bitmap bitmap = new Bitmap(A_1, A_2);
		using MemoryStream input = new MemoryStream(A_0);
		using BinaryReader binaryReader = new BinaryReader(input);
		for (int i = 0; i < A_2; i++)
		{
			for (int j = 0; j < A_1; j++)
			{
				bitmap.SetPixel(j, i, Color.FromArgb(binaryReader.ReadInt32()));
			}
		}
		return bitmap;
	}

	private void a(f A_0, BinaryReader A_1)
	{
		A_0.a = A_1.ReadInt32();
		A_0.b = A_1.ReadInt32();
		A_0.c = A_1.ReadInt32();
		A_0.d = A_1.ReadInt32();
		A_0.e = A_1.ReadInt32();
		A_0.f = A_1.ReadInt32();
		A_0.g = A_1.ReadInt32();
		for (int i = 0; i < 11; i++)
		{
			A_0.h[i] = A_1.ReadInt32();
		}
		a(A_0.i, A_1);
		A_0.j = A_1.ReadInt32();
		A_0.k = A_1.ReadInt32();
		A_0.l = A_1.ReadInt32();
		A_0.m = A_1.ReadInt32();
		A_0.n = A_1.ReadInt32();
	}

	private void a(e A_0, BinaryReader A_1)
	{
		A_0.a = A_1.ReadInt32();
		A_0.b = A_1.ReadInt32();
		A_0.c = A_1.ReadInt32();
		A_0.d = A_1.ReadInt32();
		A_0.e = A_1.ReadInt32();
		A_0.f = A_1.ReadInt32();
		A_0.g = A_1.ReadInt32();
		A_0.h = A_1.ReadInt32();
	}
}
