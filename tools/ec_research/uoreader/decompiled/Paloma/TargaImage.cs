using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace Paloma;

public class TargaImage : IDisposable
{
	private TargaHeader m_a;

	private TargaExtensionArea m_b;

	private TargaFooter m_c;

	private Bitmap m_d;

	private Bitmap m_e;

	private TGAFormat f;

	private string g = string.Empty;

	private int h;

	private int i;

	private GCHandle j;

	private GCHandle k;

	private List<List<byte>> l = new List<List<byte>>();

	private List<byte> m = new List<byte>();

	private bool n;

	public TargaHeader Header => this.m_a;

	public TargaExtensionArea ExtensionArea => this.m_b;

	public TargaFooter Footer => this.m_c;

	public TGAFormat Format => f;

	public Bitmap Image => this.m_d;

	public Bitmap Thumbnail => this.m_e;

	public string FileName => g;

	public int Stride => h;

	public int Padding => i;

	public TargaImage()
	{
		this.m_c = new TargaFooter();
		this.m_a = new TargaHeader();
		this.m_b = new TargaExtensionArea();
		this.m_d = null;
		this.m_e = null;
	}

	~TargaImage()
	{
		Dispose(disposing: false);
	}

	public TargaImage(string strFileName)
		: this()
	{
		if (Path.GetExtension(strFileName).ToLower() == ".tga")
		{
			if (File.Exists(strFileName))
			{
				g = strFileName;
				MemoryStream memoryStream = null;
				BinaryReader binaryReader = null;
				byte[] array = null;
				array = File.ReadAllBytes(g);
				if (array != null && array.Length > 0)
				{
					using (memoryStream = new MemoryStream(array))
					{
						if (memoryStream != null && memoryStream.Length > 0 && memoryStream.CanSeek)
						{
							using (binaryReader = new BinaryReader(memoryStream))
							{
								e(binaryReader);
								d(binaryReader);
								c(binaryReader);
								a(binaryReader);
								return;
							}
						}
						throw new Exception("Error loading file, could not read file from disk.");
					}
				}
				throw new Exception("Error loading file, could not read file from disk.");
			}
			throw new Exception("Error loading file, could not find file '" + strFileName + "' on disk.");
		}
		throw new Exception("Error loading file, file '" + strFileName + "' must have an extension of '.tga'.");
	}

	public TargaImage(byte[] filebytes)
		: this()
	{
		MemoryStream memoryStream;
		if (filebytes != null && filebytes.Length > 0)
		{
			using (memoryStream = new MemoryStream(filebytes))
			{
				BinaryReader a_;
				if (memoryStream != null && memoryStream.Length > 0 && memoryStream.CanSeek)
				{
					using (a_ = new BinaryReader(memoryStream))
					{
						e(a_);
						d(a_);
						c(a_);
						a(a_);
						return;
					}
				}
				throw new Exception("Error loading file, could not read file from disk.");
			}
		}
		throw new Exception("Error loading file, could not read file from disk.");
	}

	private void e(BinaryReader A_0)
	{
		if (A_0 != null && A_0.BaseStream != null && A_0.BaseStream.Length > 0 && A_0.BaseStream.CanSeek)
		{
			try
			{
				A_0.BaseStream.Seek(-18L, SeekOrigin.End);
				string text = Encoding.ASCII.GetString(A_0.ReadBytes(16));
				char[] trimChars = new char[1];
				string text2 = text.TrimEnd(trimChars);
				if (string.Compare(text2, "TRUEVISION-XFILE") == 0)
				{
					f = TGAFormat.NEW_TGA;
					A_0.BaseStream.Seek(-26L, SeekOrigin.End);
					int extensionAreaOffset = A_0.ReadInt32();
					int developerDirectoryOffset = A_0.ReadInt32();
					A_0.ReadBytes(16);
					string text3 = Encoding.ASCII.GetString(A_0.ReadBytes(1));
					char[] trimChars2 = new char[1];
					string reservedCharacter = text3.TrimEnd(trimChars2);
					this.m_c.SetExtensionAreaOffset(extensionAreaOffset);
					this.m_c.SetDeveloperDirectoryOffset(developerDirectoryOffset);
					this.m_c.SetSignature(text2);
					this.m_c.SetReservedCharacter(reservedCharacter);
				}
				else
				{
					f = TGAFormat.ORIGINAL_TGA;
				}
				return;
			}
			catch (Exception ex)
			{
				a();
				throw ex;
			}
		}
		a();
		throw new Exception("Error loading file, could not read file from disk.");
	}

	private void d(BinaryReader A_0)
	{
		if (A_0 != null && A_0.BaseStream != null && A_0.BaseStream.Length > 0 && A_0.BaseStream.CanSeek)
		{
			try
			{
				A_0.BaseStream.Seek(0L, SeekOrigin.Begin);
				this.m_a.SetImageIDLength(A_0.ReadByte());
				this.m_a.SetColorMapType((ColorMapType)A_0.ReadByte());
				this.m_a.SetImageType((ImageType)A_0.ReadByte());
				this.m_a.SetColorMapFirstEntryIndex(A_0.ReadInt16());
				this.m_a.SetColorMapLength(A_0.ReadInt16());
				this.m_a.SetColorMapEntrySize(A_0.ReadByte());
				this.m_a.SetXOrigin(A_0.ReadInt16());
				this.m_a.SetYOrigin(A_0.ReadInt16());
				this.m_a.SetWidth(A_0.ReadInt16());
				this.m_a.SetHeight(A_0.ReadInt16());
				byte b2 = A_0.ReadByte();
				switch (b2)
				{
				case 8:
				case 16:
				case 24:
				case 32:
				{
					this.m_a.SetPixelDepth(b2);
					byte a_ = A_0.ReadByte();
					this.m_a.SetAttributeBits((byte)global::d.a(a_, 0, 4));
					this.m_a.SetVerticalTransferOrder((VerticalTransferOrder)global::d.a(a_, 5, 1));
					this.m_a.SetHorizontalTransferOrder((HorizontalTransferOrder)global::d.a(a_, 4, 1));
					if (this.m_a.ImageIDLength > 0)
					{
						byte[] bytes = A_0.ReadBytes(this.m_a.ImageIDLength);
						TargaHeader targaHeader = this.m_a;
						string text = Encoding.ASCII.GetString(bytes);
						char[] trimChars = new char[1];
						targaHeader.SetImageIDValue(text.TrimEnd(trimChars));
					}
					break;
				}
				default:
					a();
					throw new Exception("Targa Image only supports 8, 16, 24, or 32 bit pixel depths.");
				}
			}
			catch (Exception ex)
			{
				a();
				throw ex;
			}
			if (this.m_a.ColorMapType == ColorMapType.COLOR_MAP_INCLUDED)
			{
				if (this.m_a.ImageType != ImageType.UNCOMPRESSED_COLOR_MAPPED && this.m_a.ImageType != ImageType.RUN_LENGTH_ENCODED_COLOR_MAPPED)
				{
					return;
				}
				if (this.m_a.ColorMapLength > 0)
				{
					try
					{
						for (int i = 0; i < this.m_a.ColorMapLength; i++)
						{
							int num = 0;
							int num2 = 0;
							int num3 = 0;
							int num4 = 0;
							switch (this.m_a.ColorMapEntrySize)
							{
							case 15:
							{
								byte[] array2 = A_0.ReadBytes(2);
								this.m_a.ColorMap.Add(global::d.a(array2[1], array2[0]));
								break;
							}
							case 16:
							{
								byte[] array = A_0.ReadBytes(2);
								this.m_a.ColorMap.Add(global::d.a(array[1], array[0]));
								break;
							}
							case 24:
								num4 = Convert.ToInt32(A_0.ReadByte());
								num3 = Convert.ToInt32(A_0.ReadByte());
								num2 = Convert.ToInt32(A_0.ReadByte());
								this.m_a.ColorMap.Add(Color.FromArgb(num2, num3, num4));
								break;
							case 32:
								num = Convert.ToInt32(A_0.ReadByte());
								num4 = Convert.ToInt32(A_0.ReadByte());
								num3 = Convert.ToInt32(A_0.ReadByte());
								num2 = Convert.ToInt32(A_0.ReadByte());
								this.m_a.ColorMap.Add(Color.FromArgb(num, num2, num3, num4));
								break;
							default:
								a();
								throw new Exception("TargaImage only supports ColorMap Entry Sizes of 15, 16, 24 or 32 bits.");
							}
						}
						return;
					}
					catch (Exception ex2)
					{
						a();
						throw ex2;
					}
				}
				a();
				throw new Exception("Image Type requires a Color Map and Color Map Length is zero.");
			}
			if (this.m_a.ImageType == ImageType.UNCOMPRESSED_COLOR_MAPPED || this.m_a.ImageType == ImageType.RUN_LENGTH_ENCODED_COLOR_MAPPED)
			{
				a();
				throw new Exception("Image Type requires a Color Map and there was not a Color Map included in the file.");
			}
			return;
		}
		a();
		throw new Exception("Error loading file, could not read file from disk.");
	}

	private void c(BinaryReader A_0)
	{
		if (A_0 != null && A_0.BaseStream != null && A_0.BaseStream.Length > 0 && A_0.BaseStream.CanSeek)
		{
			if (this.m_c.ExtensionAreaOffset <= 0)
			{
				return;
			}
			try
			{
				A_0.BaseStream.Seek(this.m_c.ExtensionAreaOffset, SeekOrigin.Begin);
				this.m_b.SetExtensionSize(A_0.ReadInt16());
				TargaExtensionArea targaExtensionArea = this.m_b;
				string text = Encoding.ASCII.GetString(A_0.ReadBytes(41));
				char[] trimChars = new char[1];
				targaExtensionArea.SetAuthorName(text.TrimEnd(trimChars));
				TargaExtensionArea targaExtensionArea2 = this.m_b;
				string text2 = Encoding.ASCII.GetString(A_0.ReadBytes(324));
				char[] trimChars2 = new char[1];
				targaExtensionArea2.SetAuthorComments(text2.TrimEnd(trimChars2));
				short num = A_0.ReadInt16();
				short num2 = A_0.ReadInt16();
				short num3 = A_0.ReadInt16();
				short num4 = A_0.ReadInt16();
				short num5 = A_0.ReadInt16();
				short num6 = A_0.ReadInt16();
				string text3 = num + "/" + num2 + "/" + num3 + " ";
				string text4 = text3;
				text3 = text4 + num4 + ":" + num5 + ":" + num6;
				if (DateTime.TryParse(text3, out var result))
				{
					this.m_b.SetDateTimeStamp(result);
				}
				TargaExtensionArea targaExtensionArea3 = this.m_b;
				string text5 = Encoding.ASCII.GetString(A_0.ReadBytes(41));
				char[] trimChars3 = new char[1];
				targaExtensionArea3.SetJobName(text5.TrimEnd(trimChars3));
				num4 = A_0.ReadInt16();
				num5 = A_0.ReadInt16();
				num6 = A_0.ReadInt16();
				TimeSpan jobTime = new TimeSpan(num4, num5, num6);
				this.m_b.SetJobTime(jobTime);
				TargaExtensionArea targaExtensionArea4 = this.m_b;
				string text6 = Encoding.ASCII.GetString(A_0.ReadBytes(41));
				char[] trimChars4 = new char[1];
				targaExtensionArea4.SetSoftwareID(text6.TrimEnd(trimChars4));
				float num7 = (float)A_0.ReadInt16() / 100f;
				string text7 = Encoding.ASCII.GetString(A_0.ReadBytes(1));
				char[] trimChars5 = new char[1];
				string text8 = text7.TrimEnd(trimChars5);
				this.m_b.SetSoftwareID(num7.ToString("F2") + text8);
				int alpha = A_0.ReadByte();
				int red = A_0.ReadByte();
				int blue = A_0.ReadByte();
				int green = A_0.ReadByte();
				this.m_b.SetKeyColor(Color.FromArgb(alpha, red, green, blue));
				this.m_b.SetPixelAspectRatioNumerator(A_0.ReadInt16());
				this.m_b.SetPixelAspectRatioDenominator(A_0.ReadInt16());
				this.m_b.SetGammaNumerator(A_0.ReadInt16());
				this.m_b.SetGammaDenominator(A_0.ReadInt16());
				this.m_b.SetColorCorrectionOffset(A_0.ReadInt32());
				this.m_b.SetPostageStampOffset(A_0.ReadInt32());
				this.m_b.SetScanLineOffset(A_0.ReadInt32());
				this.m_b.SetAttributesType(A_0.ReadByte());
				if (this.m_b.ScanLineOffset > 0)
				{
					A_0.BaseStream.Seek(this.m_b.ScanLineOffset, SeekOrigin.Begin);
					for (int i = 0; i < this.m_a.Height; i++)
					{
						this.m_b.ScanLineTable.Add(A_0.ReadInt32());
					}
				}
				if (this.m_b.ColorCorrectionOffset > 0)
				{
					A_0.BaseStream.Seek(this.m_b.ColorCorrectionOffset, SeekOrigin.Begin);
					for (int j = 0; j < 256; j++)
					{
						alpha = A_0.ReadInt16();
						red = A_0.ReadInt16();
						blue = A_0.ReadInt16();
						green = A_0.ReadInt16();
						this.m_b.ColorCorrectionTable.Add(Color.FromArgb(alpha, red, green, blue));
					}
				}
				return;
			}
			catch (Exception ex)
			{
				a();
				throw ex;
			}
		}
		a();
		throw new Exception("Error loading file, could not read file from disk.");
	}

	private byte[] b(BinaryReader A_0)
	{
		byte[] array = null;
		if (A_0 != null && A_0.BaseStream != null && A_0.BaseStream.Length > 0 && A_0.BaseStream.CanSeek)
		{
			if (this.m_a.ImageDataOffset > 0)
			{
				byte[] array2 = new byte[this.i];
				MemoryStream memoryStream = null;
				A_0.BaseStream.Seek(this.m_a.ImageDataOffset, SeekOrigin.Begin);
				int num = this.m_a.Width * this.m_a.BytesPerPixel;
				int num2 = num * this.m_a.Height;
				if (this.m_a.ImageType == ImageType.RUN_LENGTH_ENCODED_BLACK_AND_WHITE || this.m_a.ImageType == ImageType.RUN_LENGTH_ENCODED_COLOR_MAPPED || this.m_a.ImageType == ImageType.RUN_LENGTH_ENCODED_TRUE_COLOR)
				{
					byte b2 = 0;
					int num3 = -1;
					int num4 = 0;
					byte[] array3 = null;
					int num5 = 0;
					int num6 = 0;
					while (num5 < num2)
					{
						b2 = A_0.ReadByte();
						num3 = global::d.a(b2, 7, 1);
						num4 = global::d.a(b2, 0, 7) + 1;
						switch (num3)
						{
						case 1:
						{
							array3 = A_0.ReadBytes(this.m_a.BytesPerPixel);
							for (int j = 0; j < num4; j++)
							{
								byte[] array4 = array3;
								foreach (byte item in array4)
								{
									this.m.Add(item);
								}
								num6 += array3.Length;
								num5 += array3.Length;
								if (num6 == num)
								{
									this.l.Add(this.m);
									this.m = new List<byte>();
									num6 = 0;
								}
							}
							break;
						}
						case 0:
						{
							int num7 = num4 * this.m_a.BytesPerPixel;
							for (int i = 0; i < num7; i++)
							{
								this.m.Add(A_0.ReadByte());
								num5++;
								num6++;
								if (num6 == num)
								{
									this.l.Add(this.m);
									this.m = new List<byte>();
									num6 = 0;
								}
							}
							break;
						}
						}
					}
				}
				else
				{
					for (int l = 0; l < this.m_a.Height; l++)
					{
						for (int m = 0; m < num; m++)
						{
							this.m.Add(A_0.ReadByte());
						}
						this.l.Add(this.m);
						this.m = new List<byte>();
					}
				}
				bool flag = false;
				bool flag2 = false;
				switch (this.m_a.FirstPixelDestination)
				{
				case FirstPixelDestination.TOP_LEFT:
					flag = false;
					flag2 = true;
					break;
				case FirstPixelDestination.TOP_RIGHT:
					flag = false;
					flag2 = false;
					break;
				case FirstPixelDestination.BOTTOM_LEFT:
					flag = true;
					flag2 = true;
					break;
				case FirstPixelDestination.UNKNOWN:
				case FirstPixelDestination.BOTTOM_RIGHT:
					flag = true;
					flag2 = false;
					break;
				}
				using (memoryStream = new MemoryStream())
				{
					if (flag)
					{
						this.l.Reverse();
					}
					for (int n = 0; n < this.l.Count; n++)
					{
						if (flag2)
						{
							this.l[n].Reverse();
						}
						byte[] array5 = this.l[n].ToArray();
						memoryStream.Write(array5, 0, array5.Length);
						memoryStream.Write(array2, 0, array2.Length);
					}
					return memoryStream.ToArray();
				}
			}
			a();
			throw new Exception("Error loading file, No image data in file.");
		}
		a();
		throw new Exception("Error loading file, could not read file from disk.");
	}

	private void a(BinaryReader A_0)
	{
		h = ((this.m_a.Width * this.m_a.PixelDepth + 31) & -32) >> 3;
		this.i = h - (this.m_a.Width * this.m_a.PixelDepth + 7) / 8;
		byte[] value = b(A_0);
		this.j = GCHandle.Alloc(value, GCHandleType.Pinned);
		if (this.m_d != null)
		{
			this.m_d.Dispose();
		}
		if (this.m_e != null)
		{
			this.m_e.Dispose();
		}
		PixelFormat pixelFormat = b();
		this.m_d = new Bitmap(this.m_a.Width, this.m_a.Height, h, pixelFormat, this.j.AddrOfPinnedObject());
		a(A_0, pixelFormat);
		if (this.m_a.ColorMap.Count > 0)
		{
			ColorPalette palette = this.m_d.Palette;
			for (int i = 0; i < this.m_a.ColorMap.Count; i++)
			{
				if (this.m_b.AttributesType == 0 || this.m_b.AttributesType == 1)
				{
					ref Color reference = ref palette.Entries[i];
					reference = Color.FromArgb(255, this.m_a.ColorMap[i].R, this.m_a.ColorMap[i].G, this.m_a.ColorMap[i].B);
				}
				else
				{
					ref Color reference2 = ref palette.Entries[i];
					reference2 = this.m_a.ColorMap[i];
				}
			}
			this.m_d.Palette = palette;
			if (this.m_e != null)
			{
				this.m_e.Palette = palette;
			}
		}
		else if (this.m_a.PixelDepth == 8 && (this.m_a.ImageType == ImageType.UNCOMPRESSED_BLACK_AND_WHITE || this.m_a.ImageType == ImageType.RUN_LENGTH_ENCODED_BLACK_AND_WHITE))
		{
			ColorPalette palette2 = this.m_d.Palette;
			for (int j = 0; j < 256; j++)
			{
				ref Color reference3 = ref palette2.Entries[j];
				reference3 = Color.FromArgb(j, j, j);
			}
			this.m_d.Palette = palette2;
			if (this.m_e != null)
			{
				this.m_e.Palette = palette2;
			}
		}
	}

	private PixelFormat b()
	{
		PixelFormat result = PixelFormat.Undefined;
		switch (this.m_a.PixelDepth)
		{
		case 8:
			result = PixelFormat.Format8bppIndexed;
			break;
		case 16:
			if (Format == TGAFormat.NEW_TGA)
			{
				switch (this.m_b.AttributesType)
				{
				case 0:
				case 1:
				case 2:
					result = PixelFormat.Format16bppRgb555;
					break;
				case 3:
					result = PixelFormat.Format16bppArgb1555;
					break;
				}
			}
			else
			{
				result = PixelFormat.Format16bppRgb555;
			}
			break;
		case 24:
			result = PixelFormat.Format24bppRgb;
			break;
		case 32:
			if (Format == TGAFormat.NEW_TGA)
			{
				switch (this.m_b.AttributesType)
				{
				case 1:
				case 2:
					result = PixelFormat.Format32bppRgb;
					break;
				case 0:
				case 3:
					result = PixelFormat.Format32bppArgb;
					break;
				case 4:
					result = PixelFormat.Format32bppPArgb;
					break;
				}
			}
			else
			{
				result = PixelFormat.Format32bppRgb;
			}
			break;
		}
		return result;
	}

	private void a(BinaryReader A_0, PixelFormat A_1)
	{
		byte[] array = null;
		if (A_0 != null && A_0.BaseStream != null && A_0.BaseStream.Length > 0 && A_0.BaseStream.CanSeek)
		{
			if (ExtensionArea.PostageStampOffset > 0)
			{
				A_0.BaseStream.Seek(ExtensionArea.PostageStampOffset, SeekOrigin.Begin);
				int num = A_0.ReadByte();
				int num2 = A_0.ReadByte();
				int num3 = ((num * this.m_a.PixelDepth + 31) & -32) >> 3;
				int num4 = num3 - (num * this.m_a.PixelDepth + 7) / 8;
				List<List<byte>> list = new List<List<byte>>();
				List<byte> list2 = new List<byte>();
				byte[] array2 = new byte[num4];
				MemoryStream memoryStream = null;
				bool flag = false;
				bool flag2 = false;
				using (memoryStream = new MemoryStream())
				{
					int num5 = num * (this.m_a.PixelDepth / 8);
					for (int i = 0; i < num2; i++)
					{
						for (int j = 0; j < num5; j++)
						{
							list2.Add(A_0.ReadByte());
						}
						list.Add(list2);
						list2 = new List<byte>();
					}
					switch (this.m_a.FirstPixelDestination)
					{
					case FirstPixelDestination.TOP_RIGHT:
						flag2 = false;
						flag = false;
						break;
					case FirstPixelDestination.UNKNOWN:
					case FirstPixelDestination.BOTTOM_RIGHT:
						flag2 = true;
						flag = false;
						break;
					}
					if (flag2)
					{
						list.Reverse();
					}
					for (int k = 0; k < list.Count; k++)
					{
						if (flag)
						{
							list[k].Reverse();
						}
						byte[] array3 = list[k].ToArray();
						memoryStream.Write(array3, 0, array3.Length);
						memoryStream.Write(array2, 0, array2.Length);
					}
					array = memoryStream.ToArray();
				}
				if (array != null && array.Length > 0)
				{
					this.k = GCHandle.Alloc(array, GCHandleType.Pinned);
					this.m_e = new Bitmap(num, num2, num3, A_1, this.k.AddrOfPinnedObject());
				}
			}
			else if (this.m_e != null)
			{
				this.m_e.Dispose();
				this.m_e = null;
			}
		}
		else if (this.m_e != null)
		{
			this.m_e.Dispose();
			this.m_e = null;
		}
	}

	private void a()
	{
		if (this.m_d != null)
		{
			this.m_d.Dispose();
			this.m_d = null;
		}
		if (j.IsAllocated)
		{
			j.Free();
		}
		if (k.IsAllocated)
		{
			k.Free();
		}
		this.m_a = new TargaHeader();
		this.m_b = new TargaExtensionArea();
		this.m_c = new TargaFooter();
		f = TGAFormat.UNKNOWN;
		h = 0;
		i = 0;
		l.Clear();
		m.Clear();
		g = string.Empty;
	}

	public static Bitmap LoadTargaImage(string sFileName)
	{
		Bitmap bitmap = null;
		using TargaImage targaImage = new TargaImage(sFileName);
		return new Bitmap(targaImage.Image);
	}

	public static Bitmap LoadTargaImage(byte[] data)
	{
		Bitmap bitmap = null;
		using TargaImage targaImage = new TargaImage(data);
		return new Bitmap(targaImage.Image);
	}

	public void Dispose()
	{
		Dispose(disposing: true);
		GC.SuppressFinalize(this);
	}

	protected virtual void Dispose(bool disposing)
	{
		if (!n && disposing)
		{
			if (this.m_d != null)
			{
				this.m_d.Dispose();
			}
			if (this.m_e != null)
			{
				this.m_e.Dispose();
			}
			if (j.IsAllocated)
			{
				j.Free();
			}
			if (k.IsAllocated)
			{
				k.Free();
			}
		}
		n = true;
	}
}
