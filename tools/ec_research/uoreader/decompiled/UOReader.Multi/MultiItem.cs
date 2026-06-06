using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace UOReader.Multi;

public class MultiItem
{
	private uint m_a;

	private uint b;

	private List<MultiTile> c;

	private Text d;

	private short e;

	private short f;

	private short g;

	private short h;

	private short i;

	private short j;

	private readonly int k = 22;

	private readonly int l = 32;

	public uint ID
	{
		get
		{
			return this.m_a;
		}
		set
		{
			this.m_a = value;
		}
	}

	public uint TilesCount
	{
		get
		{
			return b;
		}
		set
		{
			b = value;
		}
	}

	public List<MultiTile> TileList => c;

	public short MaxZ => j;

	public short MinZ => g;

	public short MaxX => h;

	public short MaxY => i;

	public short MinX => e;

	public short MinY => f;

	public MultiItem(Text display)
	{
		d = display;
		c = new List<MultiTile>();
		j = -255;
	}

	public void Order()
	{
		for (int i = 0; i < TileList.Count; i++)
		{
			_ = TileList[i].XOffset;
			for (int j = 0; j < TileList.Count - 1; j++)
			{
				if (TileList[j].ZOffset > TileList[j + 1].ZOffset)
				{
					MultiTile item = TileList[j];
					TileList.RemoveAt(j);
					TileList.Insert(j + 1, item);
				}
			}
		}
		for (int k = 0; k < TileList.Count; k++)
		{
			for (int l = 0; l < TileList.Count - 1; l++)
			{
				if (TileList[l].ZOffset == TileList[l + 1].ZOffset && TileList[l].YOffset > TileList[l + 1].YOffset)
				{
					MultiTile item2 = TileList[l];
					TileList.RemoveAt(l);
					TileList.Insert(l + 1, item2);
				}
			}
		}
		for (int m = 0; m < TileList.Count; m++)
		{
			for (int n = 0; n < TileList.Count - 1; n++)
			{
				if (TileList[n].ZOffset == TileList[n + 1].ZOffset && TileList[n].YOffset == TileList[n + 1].YOffset && TileList[n].XOffset > TileList[n + 1].XOffset)
				{
					MultiTile item3 = TileList[n];
					TileList.RemoveAt(n);
					TileList.Insert(n + 1, item3);
				}
			}
		}
	}

	public void Load(string path)
	{
		using FileStream fs = new FileStream(path, FileMode.Open);
		Load(fs);
	}

	public void Load(byte[] path)
	{
		using MemoryStream fs = new MemoryStream(path);
		Load(fs);
	}

	public void Load(Stream fs)
	{
		using BinaryReader binaryReader = new BinaryReader(fs);
		this.m_a = binaryReader.ReadUInt32();
		b = binaryReader.ReadUInt32();
		h = 0;
		i = 0;
		e = 0;
		f = 0;
		g = 0;
		j = 0;
		for (uint num = 0u; num < b; num++)
		{
			ushort graphic = binaryReader.ReadUInt16();
			short num2 = binaryReader.ReadInt16();
			short num3 = binaryReader.ReadInt16();
			short num4 = binaryReader.ReadInt16();
			if (num4 > 255)
			{
				MessageBox.Show("MultiItem.cs - WRONG Z");
			}
			num4 = (sbyte)num4;
			byte unk = binaryReader.ReadByte();
			byte unk2 = binaryReader.ReadByte();
			if (num2 > h)
			{
				h = num2;
			}
			if (num3 > i)
			{
				i = num3;
			}
			if (num4 > j)
			{
				j = num4;
			}
			if (num2 < e)
			{
				e = num2;
			}
			if (num3 < f)
			{
				f = num3;
			}
			if (num4 < g)
			{
				g = num4;
			}
			MultiTile multiTile = new MultiTile(graphic, num2, num3, num4, unk, unk2);
			uint num5 = binaryReader.ReadUInt32();
			for (uint num6 = 0u; num6 < num5; num6++)
			{
				int n = binaryReader.ReadInt32();
				multiTile.UnkList.Add(StringDictionary.GetDictionary().GetStringAtPosition(n));
			}
			c.Add(multiTile);
		}
	}

	internal void a()
	{
		c.Clear();
	}

	public WorkerResult GetFinalBitmap2(int maxHeight, bool usingEC)
	{
		int num = ((!usingEC) ? (MaxX * k + MaxY * k - MinX * k - MinY * k) : (MaxX * l + MaxY * l - MinX * l - MinY * l));
		num += 50;
		if (num < 600)
		{
			num = 600;
		}
		int num2 = num + 128;
		int num3 = num / 2;
		int num4 = num2 / 2;
		StringBuilder stringBuilder = new StringBuilder();
		Bitmap bitmap = new Bitmap(num, num2);
		Graphics graphics = Graphics.FromImage(bitmap);
		Pen pen = new Pen(Brushes.Black);
		graphics.DrawRectangle(pen, new Rectangle(0, 0, num - 1, num2 - 1));
		for (int i = 0; i < TilesCount; i++)
		{
			if (TileList[i].ZOffset > maxHeight)
			{
				continue;
			}
			TileartItem tileartFromID = TileartItem.GetTileartFromID(TileList[i].ID);
			if (tileartFromID == null)
			{
				stringBuilder.AppendLine("No tileart for ID: " + TileList[i].ID);
				continue;
			}
			int num5 = ((!usingEC) ? 1 : 0);
			if (tileartFromID.m_textures[num5].TexturePresent == 0)
			{
				stringBuilder.AppendLine("No texture for ID: " + TileList[i].ID);
				continue;
			}
			bool isEC = false;
			Bitmap texture = tileartFromID.GetTexture(num5, 0, out isEC);
			if (texture != null)
			{
				a(stringBuilder, i);
				if (isEC)
				{
					a(graphics, TileList[i], texture, l, 6, num3, num4, tileartFromID.m_imgoffEC[0], tileartFromID.m_imgoffEC[1], tileartFromID.m_imgoffEC[2], tileartFromID.m_imgoffEC[3], tileartFromID.m_imgoffEC[4], tileartFromID.m_imgoffEC[5]);
				}
				else
				{
					a(graphics, TileList[i], texture, k, 4, num3, num4, tileartFromID.m_imgoff2D[0], tileartFromID.m_imgoff2D[1], tileartFromID.m_imgoff2D[2], tileartFromID.m_imgoff2D[3], tileartFromID.m_imgoff2D[4], tileartFromID.m_imgoff2D[5]);
				}
			}
		}
		for (int j = 0; j < TilesCount; j++)
		{
			int num6 = ((!usingEC) ? k : l);
			int num7 = num3 + (TileList[j].XOffset - TileList[j].YOffset) * num6;
			int num8 = num4 + (TileList[j].XOffset + TileList[j].YOffset) * num6;
			if (TileList[j].XOffset == 0 && TileList[j].YOffset == 0)
			{
				pen.Color = Color.PaleGreen;
			}
			graphics.DrawRectangle(pen, new Rectangle(num7 - 1, num8 - 1, 2, 2));
			if (TileList[j].XOffset == 0 && TileList[j].YOffset == 0)
			{
				pen.Color = Color.Black;
			}
		}
		graphics.Dispose();
		return new WorkerResult(bitmap, stringBuilder.ToString());
	}

	private void a(StringBuilder A_0, int A_1)
	{
		short xOffset = TileList[A_1].XOffset;
		short yOffset = TileList[A_1].YOffset;
		short zOffset = TileList[A_1].ZOffset;
		A_0.Append("ID " + TileList[A_1].ID.ToString() + "\t\tx " + xOffset + "\ty " + yOffset + "\tz " + zOffset + "\tUnk " + TileList[A_1].Unk1 + "\tUnk " + TileList[A_1].Unk2);
		for (int i = 0; i < TileList[A_1].UnkList.Count; i++)
		{
			A_0.AppendLine("\t" + TileList[A_1].UnkList[i]);
		}
		A_0.AppendLine();
	}

	public WorkerResult GetFinalBitmap(int maxHeight, bool usingEC)
	{
		int num = MaxX * k + MaxY * k - MinX * k - MinY * k + 50;
		if (num < 600)
		{
			num = 600;
		}
		int num2 = num + 128;
		int num3 = num / 2;
		int num4 = num2 / 2;
		StringBuilder stringBuilder = new StringBuilder();
		Bitmap bitmap = new Bitmap(num, num2);
		Graphics graphics = Graphics.FromImage(bitmap);
		Pen pen = new Pen(Brushes.Black);
		graphics.DrawRectangle(pen, new Rectangle(0, 0, num - 1, num2 - 1));
		for (int i = 0; i < TilesCount; i++)
		{
			TileartItem tileartFromID = TileartItem.GetTileartFromID(TileList[i].ID);
			if (tileartFromID == null)
			{
				stringBuilder.AppendLine("No tileart for ID: " + TileList[i].ID);
				continue;
			}
			int num5 = ((!usingEC) ? 1 : 0);
			if (tileartFromID.m_textures[num5].TexturePresent == 0)
			{
				stringBuilder.AppendLine("No texture for ID: " + TileList[i].ID);
				continue;
			}
			bool isEC = false;
			Bitmap texture = tileartFromID.GetTexture(num5, 0, out isEC);
			if (texture == null)
			{
				continue;
			}
			short xOffset = TileList[i].XOffset;
			short yOffset = TileList[i].YOffset;
			short zOffset = TileList[i].ZOffset;
			if (zOffset <= maxHeight)
			{
				a(stringBuilder, i);
				int num6 = 0;
				int num7 = 0;
				int num8;
				int num9;
				if (isEC)
				{
					num7 = tileartFromID.m_imgoffEC[1] - tileartFromID.m_imgoffEC[3];
					num6 = tileartFromID.m_imgoffEC[2] - tileartFromID.m_imgoffEC[0];
					num8 = num3 - yOffset * l + xOffset * l + num6;
					num9 = num4 + yOffset * l + xOffset * l + num7 + 64 + num6;
					num9 -= zOffset * 6;
					num8 -= tileartFromID.m_imgoffEC[4];
					num9 += tileartFromID.m_imgoffEC[5];
				}
				else
				{
					num7 = tileartFromID.m_imgoff2D[1] - tileartFromID.m_imgoff2D[3];
					num6 = tileartFromID.m_imgoff2D[0];
					num8 = num3 - yOffset * k + xOffset * k + num6;
					num9 = num4 + yOffset * k + xOffset * k + num7 + 64 + num6;
					num9 -= zOffset * 4;
					num8 += tileartFromID.m_imgoff2D[4];
					num9 += tileartFromID.m_imgoff2D[5];
				}
				Rectangle srcRect = ((!isEC) ? new Rectangle(tileartFromID.m_imgoff2D[0], tileartFromID.m_imgoff2D[1], tileartFromID.m_imgoff2D[2], tileartFromID.m_imgoff2D[3]) : new Rectangle(tileartFromID.m_imgoffEC[0], tileartFromID.m_imgoffEC[1], tileartFromID.m_imgoffEC[2], tileartFromID.m_imgoffEC[3]));
				graphics.DrawImage(texture, num8, num9, srcRect, GraphicsUnit.Pixel);
				graphics.DrawRectangle(new Pen(Color.Red), num8, num9, 2, 2);
			}
		}
		graphics.Dispose();
		return new WorkerResult(bitmap, stringBuilder.ToString());
	}

	private void a(Graphics A_0, MultiTile A_1, Bitmap A_2, int A_3, int A_4, int A_5, int A_6, int A_7, int A_8, int A_9, int A_10, int A_11, int A_12)
	{
		int num = A_5 + (A_1.XOffset - A_1.YOffset) * A_3;
		int num2 = A_6 + (A_1.XOffset + A_1.YOffset) * A_3;
		int num3 = A_9 - A_7;
		int num4 = A_10 - A_8;
		if (num3 % 2 == 1)
		{
			num--;
		}
		num -= A_3;
		num2 += (5 - A_1.ZOffset) * A_4;
		num2 -= num4;
		num2 += A_12;
		num += A_11;
		Rectangle srcRect = new Rectangle(A_7, A_8, num3, num4);
		A_0.DrawImage(A_2, num, num2, srcRect, GraphicsUnit.Pixel);
	}
}
