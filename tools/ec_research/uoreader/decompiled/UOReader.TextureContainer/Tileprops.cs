using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace UOReader.TextureContainer;

public class Tileprops
{
	public static List<byte> Unk_L = new List<byte>();

	public static List<int> Unk2_L = new List<int>();

	public static List<int> Unk3_L = new List<int>();

	public static List<int> Unk4_L = new List<int>();

	public static List<int> Unk5_L = new List<int>();

	public static Dictionary<int, List<uint>> Unk6_L = new Dictionary<int, List<uint>>();

	public static Dictionary<int, List<uint>> UnkType_L = new Dictionary<int, List<uint>>();

	private ushort m_a;

	private uint m_b;

	private uint m_c;

	private byte m_d;

	private byte m_e;

	private float m_f;

	private float m_g;

	private int m_h;

	private int i;

	private int j;

	private int k;

	private byte[] l = new byte[4];

	private int[] m = new int[6];

	private int[] n = new int[6];

	private string o;

	private string p;

	private TileFlag q;

	private TileFlag r;

	public int[] ImageOffset2D => m;

	public int[] ImageOffsetEC => n;

	public string Dump => o;

	public string FlagsDump => p;

	public TileFlag Flags => q;

	public TileFlag Flags2 => r;

	public ushort Header => this.m_a;

	public uint ID => this.m_b;

	public uint Group => this.m_c;

	public byte Unk => this.m_d;

	public int Unk2 => (int)this.m_f;

	public int Unk3 => (int)this.m_g;

	public int FixedZero => this.m_h;

	public int OldID => i;

	public int Unk6 => j;

	public int UnkType => k;

	public byte[] RadarCol => l;

	public void Read(byte[] stream)
	{
		using MemoryStream input = new MemoryStream(stream);
		using BinaryReader binaryReader = new BinaryReader(input);
		StringBuilder stringBuilder = new StringBuilder();
		this.m_a = binaryReader.ReadUInt16();
		this.m_c = binaryReader.ReadUInt32();
		this.m_b = binaryReader.ReadUInt32();
		this.m_d = binaryReader.ReadByte();
		this.m_e = binaryReader.ReadByte();
		this.m_f = binaryReader.ReadSingle();
		this.m_g = binaryReader.ReadSingle();
		this.m_h = binaryReader.ReadInt32();
		i = binaryReader.ReadInt32();
		j = binaryReader.ReadInt32();
		k = binaryReader.ReadInt32();
		stringBuilder.AppendLine("Head\t" + this.m_a);
		stringBuilder.AppendLine("StrDic Offset\t" + this.m_c);
		stringBuilder.AppendLine("\t" + StringDictionary.GetDictionary().GetStringAtPosition(this.m_c));
		stringBuilder.AppendLine("ID\t" + this.m_b);
		stringBuilder.AppendLine("Bool\t" + this.m_d);
		stringBuilder.AppendLine("Bool\t" + this.m_e);
		stringBuilder.AppendLine("UAdd\t" + this.m_f);
		stringBuilder.AppendLine("UAdd\t" + this.m_g);
		stringBuilder.AppendLine("FixedZero?\t" + this.m_h);
		stringBuilder.AppendLine("OldID\t" + i.ToString("X"));
		stringBuilder.AppendLine("Unk\t" + j.ToString("X"));
		stringBuilder.AppendLine("Type??\t" + k);
		if (!Unk_L.Contains(this.m_d))
		{
			Unk_L.Add(this.m_d);
		}
		if (!Unk4_L.Contains(this.m_h))
		{
			Unk4_L.Add(this.m_h);
		}
		if (!Unk6_L.ContainsKey(j))
		{
			Unk6_L.Add(j, new List<uint>());
		}
		Unk6_L[j].Add(this.m_b);
		if (!UnkType_L.ContainsKey(k))
		{
			UnkType_L.Add(k, new List<uint>());
		}
		UnkType_L[k].Add(this.m_b);
		byte b = binaryReader.ReadByte();
		int num = binaryReader.ReadInt32();
		int num2 = binaryReader.ReadInt32();
		int num3 = binaryReader.ReadInt32();
		int num4 = binaryReader.ReadInt32();
		int num5 = binaryReader.ReadInt32();
		long num6 = binaryReader.ReadInt64();
		long num7 = binaryReader.ReadInt64();
		q = (TileFlag)Enum.Parse(typeof(TileFlag), num6.ToString());
		r = (TileFlag)Enum.Parse(typeof(TileFlag), num7.ToString());
		StringBuilder stringBuilder2 = new StringBuilder();
		a(q, stringBuilder2);
		a(r, stringBuilder2);
		p = stringBuilder2.ToString();
		int num8 = binaryReader.ReadInt32();
		stringBuilder.AppendLine("BUnk\t" + b);
		stringBuilder.AppendLine("Unk\t" + num.ToString("X"));
		stringBuilder.AppendLine("Unk\t" + num2);
		stringBuilder.AppendLine("LightRelated\t" + num3.ToString("X"));
		stringBuilder.AppendLine("LightRelated\t" + num4.ToString("X"));
		stringBuilder.AppendLine("Unk\t" + num5);
		stringBuilder.AppendLine("FLAGS\t" + q);
		stringBuilder.AppendLine("FLAGS\t" + r);
		stringBuilder.AppendLine("Facing?\t" + num8);
		h(binaryReader, stringBuilder);
		stringBuilder.AppendLine();
		try
		{
			g(binaryReader, stringBuilder);
			f(binaryReader, stringBuilder);
			stringBuilder.AppendLine();
			e(binaryReader, stringBuilder);
			d(binaryReader, stringBuilder);
			c(binaryReader, stringBuilder);
			this.b(binaryReader, stringBuilder);
			Sub_9_7(binaryReader, stringBuilder);
			Sub_9_7(binaryReader, stringBuilder);
			Sub_9_7(binaryReader, stringBuilder);
			Sub_9_7(binaryReader, stringBuilder);
			a(binaryReader, stringBuilder);
		}
		catch (Exception)
		{
		}
		stringBuilder.AppendLine();
		stringBuilder.AppendLine("----");
		while (binaryReader.BaseStream.Position < binaryReader.BaseStream.Length)
		{
			stringBuilder.Append(binaryReader.ReadByte().ToString("X") + " ");
		}
		o = stringBuilder.ToString();
	}

	private void a(TileFlag A_0, StringBuilder A_1)
	{
		A_1.Append(A_0.ToString());
		A_1.AppendLine();
	}

	private void h(BinaryReader A_0, StringBuilder A_1)
	{
		for (int i = 0; i < 6; i++)
		{
			n[i] = A_0.ReadInt32();
		}
		for (int j = 0; j < 6; j++)
		{
			m[j] = A_0.ReadInt32();
		}
		A_1.AppendLine("ECOffset\t" + n[0] + " " + n[1] + " " + n[2] + " " + n[3] + " " + n[4] + " " + n[5]);
		A_1.AppendLine("2DOffset\t" + m[0] + " " + m[1] + " " + m[2] + " " + m[3] + " " + m[4] + " " + m[5]);
	}

	private void g(BinaryReader A_0, StringBuilder A_1)
	{
		byte b = A_0.ReadByte();
		A_1.AppendLine("C1\t" + b);
		for (int i = 0; i < b; i++)
		{
			TileArtProperties a_ = (TileArtProperties)A_0.ReadByte();
			int a_2 = A_0.ReadInt32();
			a(A_1, a_, a_2);
		}
	}

	private void a(StringBuilder A_0, TileArtProperties A_1, int A_2)
	{
		if (A_1 == TileArtProperties.Weight && A_2 == 255)
		{
			A_0.AppendLine(A_1.ToString() + "\tNot Movable");
		}
		else
		{
			A_0.AppendLine(A_1.ToString() + "\t" + A_2);
		}
	}

	private void f(BinaryReader A_0, StringBuilder A_1)
	{
		byte b = A_0.ReadByte();
		A_1.AppendLine("C2\t" + b);
		for (int i = 0; i < b; i++)
		{
			TileArtProperties a_ = (TileArtProperties)A_0.ReadByte();
			int a_2 = A_0.ReadInt32();
			a(A_1, a_, a_2);
		}
	}

	private void e(BinaryReader A_0, StringBuilder A_1)
	{
		int num = A_0.ReadInt32();
		A_1.AppendLine("C3 \t" + num + " - Coins stacks:");
		for (int num2 = num; num2 != 0; num2--)
		{
			int num3 = A_0.ReadInt32();
			int num4 = A_0.ReadInt32();
			A_1.AppendLine("Amount:" + num2 + "\t" + num3 + " - ID " + num4);
		}
		A_1.AppendLine();
	}

	private void d(BinaryReader A_0, StringBuilder A_1)
	{
		int num = A_0.ReadInt32();
		A_1.AppendLine("C4\t" + num);
		for (int i = 0; i < num; i++)
		{
			byte b = A_0.ReadByte();
			A_1.AppendLine("val\t" + b + " animation appearance filter");
			switch (b)
			{
			case 1:
			{
				byte b2 = A_0.ReadByte();
				int num5 = A_0.ReadInt32();
				A_1.AppendLine("\t\t" + b2 + " " + num5);
				break;
			}
			case 0:
			{
				uint num2 = A_0.ReadUInt32();
				A_1.AppendLine("\tSubC\t" + num2);
				for (int j = 0; j < num2; j++)
				{
					int num3 = A_0.ReadInt32();
					int num4 = A_0.ReadInt32();
					A_1.AppendLine("\t\t" + num3 + " " + num4);
				}
				break;
			}
			}
		}
		A_1.AppendLine();
	}

	private void c(BinaryReader A_0, StringBuilder A_1)
	{
		byte b = A_0.ReadByte();
		A_1.AppendLine("ChairRelated\t" + b + " sitting data count(0:1)");
		if (b != 0)
		{
			int num = A_0.ReadInt32();
			int num2 = A_0.ReadInt32();
			int num3 = A_0.ReadInt32();
			int num4 = A_0.ReadInt32();
			A_1.AppendLine("Unk\t" + num + " " + num2 + " " + num3 + " " + num4);
		}
		A_1.AppendLine();
	}

	private void b(BinaryReader A_0, StringBuilder A_1)
	{
		for (int i = 0; i < 4; i++)
		{
			l[i] = A_0.ReadByte();
		}
		A_1.AppendLine("RadarCol\n\tR" + l[0] + " G" + l[1] + " B" + l[2] + " A" + l[3]);
		A_1.AppendLine();
	}

	public static void Sub_9_7(BinaryReader r, StringBuilder sb)
	{
		byte b = r.ReadByte();
		sb.AppendLine("V7\t" + b + " - Textures");
		if (b != 0)
		{
			byte b2 = r.ReadByte();
			int num = r.ReadInt32();
			sb.AppendLine("Unk\t" + b2);
			sb.AppendLine("\t" + StringDictionary.GetDictionary().GetStringAtPosition(num));
			byte b3 = r.ReadByte();
			sb.AppendLine("\tC7.1\t" + b3);
			for (int i = 0; i < b3; i++)
			{
				int num2 = r.ReadInt32();
				byte b4 = r.ReadByte();
				float num3 = r.ReadSingle();
				int num4 = r.ReadInt32();
				float num5 = r.ReadInt32();
				sb.AppendLine("\t- " + i);
				sb.AppendLine("\t\t" + StringDictionary.GetDictionary().GetStringAtPosition(num2));
				sb.AppendLine("\t\t " + b4 + " " + num3.ToString() + " " + num4 + " " + num5);
			}
			uint num6 = r.ReadUInt32();
			sb.AppendLine("\tC7.2\t" + num6);
			for (int j = 0; j < num6; j++)
			{
				int num7 = r.ReadInt32();
				sb.AppendLine("\t- " + j + "\t" + num7);
			}
			uint num8 = r.ReadUInt32();
			sb.AppendLine("\tC7.3\t" + num8);
			for (int k = 0; k < num8; k++)
			{
				float num9 = r.ReadSingle();
				sb.AppendLine("\t- " + k + "\t" + num9);
			}
		}
		sb.AppendLine();
	}

	private void a(BinaryReader A_0, StringBuilder A_1)
	{
		byte b = A_0.ReadByte();
		A_1.AppendLine("C8\t" + b);
		for (int i = 0; i < b; i++)
		{
			EffectsCollection.Sub_4_6_30(A_0, A_1);
		}
		A_1.AppendLine();
	}
}
