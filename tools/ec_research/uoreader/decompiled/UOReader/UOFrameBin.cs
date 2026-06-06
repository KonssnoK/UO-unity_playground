using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace UOReader;

public class UOFrameBin
{
	private byte[] m_a;

	private uint m_b;

	private uint m_c;

	private uint m_d;

	private short e;

	private short f;

	private short g;

	private short h;

	private uint i;

	private uint j;

	private uint k;

	private uint l;

	private List<ColourEntry> m = new List<ColourEntry>();

	private List<FrameEntry> n = new List<FrameEntry>();

	private byte[] o;

	private long p;

	private List<TreeNode> q = new List<TreeNode>();

	private Image r;

	public List<TreeNode> Frames => q;

	public short InitCoordsX => e;

	public short InitCoordsY => f;

	public byte[] ImageData => o;

	public long ImageDataOffset => p;

	public List<ColourEntry> Colours => m;

	public Image ColoursIMG => r;

	public uint ColoursCount => i;

	private void a()
	{
		j = 0u;
		i = 0u;
		m.Clear();
		g = 0;
		h = 0;
		l = 0u;
		k = 0u;
		n.Clear();
		this.m_d = 0u;
		e = 0;
		f = 0;
		this.m_c = 0u;
		this.m_b = 0u;
		q.Clear();
	}

	public void Load(byte[] ms)
	{
		a();
		using (MemoryStream input = new MemoryStream(ms))
		{
			using BinaryReader a_ = new BinaryReader(input);
			if (d(a_))
			{
				c(a_);
				b(a_);
				a(a_);
			}
			else
			{
				MessageBox.Show("THIS IS NOT ANIMATIONFRAME.BIN FILE!");
			}
		}
		Bitmap bitmap = new Bitmap((int)(this.i + 100), 101);
		int num = 0;
		for (int i = 0; i < m.Count; i++)
		{
			Color pixel = m[i].Pixel;
			if (i % 32 == 0)
			{
				num += 10;
			}
			for (int j = 0; j < 100; j++)
			{
				bitmap.SetPixel(i + num, j, pixel);
			}
			bitmap.SetPixel(i + num, 100, Color.Black);
		}
		r = bitmap;
		for (int k = 0; k < this.k; k++)
		{
			TreeNode treeNode = new TreeNode();
			treeNode.Tag = n[k];
			treeNode.Text = n[k].Frame.ToString();
			q.Add(treeNode);
		}
	}

	private bool d(BinaryReader A_0)
	{
		this.m_a = A_0.ReadBytes(4);
		if (this.m_a[0] != 65 || this.m_a[1] != 77 || this.m_a[2] != 79)
		{
			return false;
		}
		this.m_b = A_0.ReadUInt32();
		this.m_c = A_0.ReadUInt32();
		this.m_d = A_0.ReadUInt32();
		e = A_0.ReadInt16();
		f = A_0.ReadInt16();
		g = A_0.ReadInt16();
		h = A_0.ReadInt16();
		i = A_0.ReadUInt32();
		j = A_0.ReadUInt32();
		k = A_0.ReadUInt32();
		l = A_0.ReadUInt32();
		return true;
	}

	private bool c(BinaryReader A_0)
	{
		A_0.BaseStream.Seek(j, SeekOrigin.Begin);
		m.Clear();
		for (int i = 0; i < this.i; i++)
		{
			ColourEntry item = new ColourEntry(A_0.ReadByte(), A_0.ReadByte(), A_0.ReadByte(), A_0.ReadByte());
			m.Add(item);
		}
		return true;
	}

	private bool b(BinaryReader A_0)
	{
		A_0.BaseStream.Seek(l, SeekOrigin.Begin);
		n.Clear();
		for (int i = 0; i < k; i++)
		{
			FrameEntry item = new FrameEntry(A_0.ReadUInt16(), A_0.ReadUInt16(), A_0.ReadInt16(), A_0.ReadInt16(), A_0.ReadInt16(), A_0.ReadInt16(), (uint)(l + i * 16 + A_0.ReadUInt32()), this.i);
			n.Add(item);
		}
		return true;
	}

	private bool a(BinaryReader A_0)
	{
		p = l + k * 16;
		o = new byte[(int)(this.m_c - p)];
		A_0.BaseStream.Seek(p, SeekOrigin.Begin);
		o = A_0.ReadBytes((int)(this.m_c - p));
		return true;
	}

	public string FillTxtInfos()
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.Append("Animation ID: " + this.m_d + "\n\n");
		stringBuilder.Append("Version: " + this.m_b + "\n");
		stringBuilder.Append("ColourCount: " + i + "\n");
		stringBuilder.Append("ColourOffset: " + j + "\n");
		stringBuilder.Append("FramesCount: " + k + "\n");
		stringBuilder.Append("FramesOffset: " + l + "\n\n");
		stringBuilder.Append("MainInitX: " + e + "\tMainInitY: " + f + "\nMainEndX: " + g + "\tMainEndY: " + h + "\n\n");
		return stringBuilder.ToString();
	}

	public int GetWidth()
	{
		return Math.Abs(g - e);
	}

	public int GetHeight()
	{
		return Math.Abs(h - f);
	}
}
