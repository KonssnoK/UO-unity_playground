using System;
using System.Drawing;
using System.IO;
using System.Text;
using Mythic.Package;

namespace UOReader;

public class TileartItem
{
	private const string m_a = "build/tileart/";

	private const string m_b = ".bin";

	public ushort m_header;

	public uint m_id;

	public uint m_nameIndex;

	public byte m_unk;

	public byte m_unk7;

	public float m_unk2;

	public float m_unk3;

	public int m_fixedZero;

	public int m_oldID;

	public float m_unk6;

	public int m_unk_type;

	public byte m_unk8;

	public int m_unk9;

	public int m_unk10;

	public float m_unk11;

	public float m_unk12;

	public int m_unk13;

	public int m_unk16;

	public long m_int_flags;

	public long m_int_flags_full;

	public TileFlag m_flags;

	public TileFlag m_flags2;

	public int[] m_imgoff2D = new int[6];

	public int[] m_imgoffEC = new int[6];

	public TileartPropItem[] props;

	public TileartPropItem[] props2;

	public StackAlias[] m_stackaliases;

	public AnimationAppearanceItem m_appearance;

	public SittingAnimationItem m_sittingAnimation;

	public RadarColItem m_radarCol;

	public TextureItem[] m_textures = new TextureItem[4];

	public EffectItem[] m_effects;

	public string m_dump;

	public string m_flagsdump;

	private static MythicPackage m_c;

	public TileartItem(byte[] data)
	{
		a(data);
	}

	public static TileartItem GetTileartFromID(int id)
	{
		TileartItem result = null;
		if (TileartItem.m_c == null)
		{
			TileartItem.m_c = new MythicPackage(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Tileart));
		}
		string text = id.ToString();
		if (text.Length < 8)
		{
			int num = 8 - text.Length;
			for (int i = 0; i < num; i++)
			{
				text = "0" + text;
			}
		}
		text = "build/tileart/" + text + ".bin";
		SearchResult searchResult = TileartItem.m_c.Search(text);
		if (searchResult.Found)
		{
			byte[] data = TileartItem.m_c.Blocks[searchResult.Block].Files[searchResult.File].Unpack(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Tileart));
			result = new TileartItem(data);
		}
		return result;
	}

	public static Bitmap getImageFromID(int id)
	{
		bool flag = false;
		TileartItem tileartFromID = GetTileartFromID(id);
		if (tileartFromID == null)
		{
			return null;
		}
		int num = ((!flag) ? 1 : 0);
		if (tileartFromID.m_textures[num].TexturePresent == 0)
		{
			return null;
		}
		bool isEC = false;
		return tileartFromID.GetTexture(num, 0, out isEC);
	}

	private void a(byte[] A_0)
	{
		using MemoryStream input = new MemoryStream(A_0);
		using BinaryReader binaryReader = new BinaryReader(input);
		m_header = binaryReader.ReadUInt16();
		m_nameIndex = binaryReader.ReadUInt32();
		m_id = binaryReader.ReadUInt32();
		m_unk = binaryReader.ReadByte();
		m_unk7 = binaryReader.ReadByte();
		m_unk2 = binaryReader.ReadSingle();
		m_unk3 = binaryReader.ReadSingle();
		m_fixedZero = binaryReader.ReadInt32();
		m_oldID = binaryReader.ReadInt32();
		m_unk6 = binaryReader.ReadInt32();
		m_unk_type = binaryReader.ReadInt32();
		m_unk8 = binaryReader.ReadByte();
		m_unk9 = binaryReader.ReadInt32();
		m_unk10 = binaryReader.ReadInt32();
		m_unk11 = binaryReader.ReadSingle();
		m_unk12 = binaryReader.ReadSingle();
		m_unk13 = binaryReader.ReadInt32();
		m_int_flags = binaryReader.ReadInt64();
		m_int_flags_full = binaryReader.ReadInt64();
		m_flags = (TileFlag)Enum.Parse(typeof(TileFlag), m_int_flags.ToString());
		m_flags2 = (TileFlag)Enum.Parse(typeof(TileFlag), m_int_flags_full.ToString());
		m_flagsdump = m_flags.ToString() + "\n" + m_flags2;
		m_unk16 = binaryReader.ReadInt32();
		for (int i = 0; i < 6; i++)
		{
			m_imgoffEC[i] = binaryReader.ReadInt32();
		}
		for (int j = 0; j < 6; j++)
		{
			m_imgoff2D[j] = binaryReader.ReadInt32();
		}
		try
		{
			props = c(binaryReader);
			props2 = c(binaryReader);
			b(binaryReader);
			m_appearance = AnimationAppearanceItem.ReadAnimationAppearance(binaryReader);
			m_sittingAnimation = SittingAnimationItem.ReadSittingAnimation(binaryReader);
			m_radarCol = RadarColItem.ReadRadarCol(binaryReader);
			m_textures[0] = TextureItem.ReadTexture(binaryReader);
			m_textures[1] = TextureItem.ReadTexture(binaryReader);
			m_textures[2] = TextureItem.ReadTexture(binaryReader);
			m_textures[3] = TextureItem.ReadTexture(binaryReader);
			a(binaryReader);
		}
		catch
		{
		}
	}

	private TileartPropItem[] c(BinaryReader A_0)
	{
		byte b = A_0.ReadByte();
		TileartPropItem[] array = new TileartPropItem[b];
		for (int i = 0; i < b; i++)
		{
			array[i] = TileartPropItem.ReadProp(A_0);
		}
		return array;
	}

	private void b(BinaryReader A_0)
	{
		int num = A_0.ReadInt32();
		m_stackaliases = new StackAlias[num];
		for (int i = 0; i < num; i++)
		{
			m_stackaliases[i] = StackAlias.ReadStackAlias(A_0);
		}
	}

	private void a(BinaryReader A_0)
	{
		byte b = A_0.ReadByte();
		m_effects = new EffectItem[b];
		for (int i = 0; i < b; i++)
		{
			m_effects[i] = EffectItem.ReadEffect(A_0);
		}
	}

	public string DumpDatas()
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("Head\t" + m_header);
		stringBuilder.AppendLine("StrDic Offset\t" + m_nameIndex);
		stringBuilder.AppendLine("\t" + StringDictionary.GetDictionary().GetStringAtPosition(m_nameIndex));
		stringBuilder.AppendLine("ID\t" + m_id);
		stringBuilder.AppendLine("UBool\t" + m_unk);
		stringBuilder.AppendLine("UBool\t" + m_unk7);
		stringBuilder.AppendLine("UFloat\t" + m_unk2);
		stringBuilder.AppendLine("UFloat\t" + m_unk3);
		stringBuilder.AppendLine("FixedZero?\t" + m_fixedZero);
		stringBuilder.AppendLine("OldID\t" + m_oldID + " " + m_oldID.ToString("X"));
		stringBuilder.AppendLine("UFloat6\t" + m_unk6);
		stringBuilder.AppendLine("Type??\t" + ((m_unk_type == 400) ? "tile(400)" : ((m_unk_type == 666) ? "item(666)" : m_unk_type.ToString())));
		stringBuilder.AppendLine("BUnk8\t" + m_unk8);
		stringBuilder.AppendLine("Unk9\t" + m_unk9 + " " + m_unk9.ToString("X"));
		stringBuilder.AppendLine("Unk10\t" + m_unk10 + " " + m_unk10.ToString("X"));
		stringBuilder.AppendLine("LightRelated\t" + m_unk11);
		stringBuilder.AppendLine("LightRelated\t" + m_unk12);
		stringBuilder.AppendLine("Unk13\t" + m_unk13 + " " + m_unk13.ToString("X"));
		stringBuilder.AppendLine("FLAGS\t" + m_flags);
		stringBuilder.AppendLine("FLAGS\t" + m_flags2);
		stringBuilder.AppendLine("Facing?\t" + m_unk16);
		stringBuilder.AppendLine("ECOffset\t" + m_imgoffEC[0] + " " + m_imgoffEC[1] + " " + m_imgoffEC[2] + " " + m_imgoffEC[3] + " " + m_imgoffEC[4] + " " + m_imgoffEC[5]);
		stringBuilder.AppendLine("\t\t w: " + (m_imgoffEC[2] - m_imgoffEC[0]) + " h: " + (m_imgoffEC[3] - m_imgoffEC[1]) + " wTot: " + (m_imgoffEC[2] - m_imgoffEC[0] + m_imgoffEC[4]) + " hTot: " + (m_imgoffEC[3] - m_imgoffEC[1] + m_imgoffEC[5]));
		stringBuilder.AppendLine("2DOffset\t" + m_imgoff2D[0] + " " + m_imgoff2D[1] + " " + m_imgoff2D[2] + " " + m_imgoff2D[3] + " " + m_imgoff2D[4] + " " + m_imgoff2D[5]);
		stringBuilder.AppendLine("\t\t w: " + (m_imgoff2D[2] - m_imgoff2D[0]) + " h: " + (m_imgoff2D[3] - m_imgoff2D[1]));
		stringBuilder.AppendLine("C1\t" + props.Length);
		for (int i = 0; i < props.Length; i++)
		{
			if (props[i].prop == TileArtProperties.Weight && props[i].value == 255)
			{
				stringBuilder.AppendLine(props[i].prop.ToString() + "\tNot Movable");
			}
			else
			{
				stringBuilder.AppendLine(props[i].prop.ToString() + "\t" + props[i].value);
			}
		}
		stringBuilder.AppendLine("C2\t" + props2.Length);
		for (int j = 0; j < props2.Length; j++)
		{
			if (props2[j].prop == TileArtProperties.Weight && props2[j].value == 255)
			{
				stringBuilder.AppendLine(props2[j].prop.ToString() + "\tNot Movable");
			}
			else
			{
				stringBuilder.AppendLine(props2[j].prop.ToString() + "\t" + props2[j].value);
			}
		}
		stringBuilder.AppendLine();
		for (int num = m_stackaliases.Length; num != 0; num--)
		{
			stringBuilder.Append(StackAlias.PrintStackAlias(m_stackaliases[num], num));
		}
		stringBuilder.AppendLine(AnimationAppearanceItem.PrintAnimationAppearance(m_appearance));
		stringBuilder.AppendLine(SittingAnimationItem.PrintSittingAnimation(m_sittingAnimation));
		stringBuilder.AppendLine(RadarColItem.PrintRadarColInfo(m_radarCol));
		for (int k = 0; k < m_textures.Length; k++)
		{
			stringBuilder.AppendLine(TextureItem.PrintTextureInfo(m_textures[k]));
		}
		stringBuilder.AppendLine("C8\t" + m_effects.Length);
		for (int l = 0; l < m_effects.Length; l++)
		{
			stringBuilder.AppendLine(EffectItem.PrintEffect(m_effects[l]));
		}
		m_dump = stringBuilder.ToString();
		return stringBuilder.ToString();
	}

	public Bitmap GetTexture(int tex, int sub, out bool isEC)
	{
		int strDic = m_textures[tex].tiArray[sub].strDic;
		string stringAtPosition = StringDictionary.GetDictionary().GetStringAtPosition(strDic);
		return TextureImage.GetTextureImage().GetFromTGA(stringAtPosition, out isEC);
	}

	public static void DrawBorders(Bitmap cimg, bool isEC, TileartItem tai, bool drawOffsets)
	{
		Graphics graphics = Graphics.FromImage(cimg);
		Pen pen = new Pen(Brushes.Pink);
		int num;
		int num2;
		int num3;
		int num4;
		int num5;
		int num6;
		if (isEC)
		{
			num = tai.m_imgoffEC[0];
			num2 = tai.m_imgoffEC[1];
			num3 = tai.m_imgoffEC[2];
			if (num3 == 0)
			{
				num3 = tai.m_imgoffEC[3];
			}
			num4 = tai.m_imgoffEC[3];
			num5 = tai.m_imgoffEC[4];
			num6 = tai.m_imgoffEC[5];
		}
		else
		{
			num = tai.m_imgoff2D[0];
			num2 = tai.m_imgoff2D[1];
			num3 = tai.m_imgoff2D[2];
			num4 = tai.m_imgoff2D[3];
			num5 = tai.m_imgoff2D[4];
			num6 = tai.m_imgoff2D[5];
		}
		int num7 = num3 - num;
		int num8 = num4 - num2;
		if (drawOffsets)
		{
			if (num5 > 0)
			{
				num += num5;
			}
			else
			{
				num7 -= num5;
			}
			if (num6 > 0)
			{
				num2 += num6;
			}
			else
			{
				num8 -= num6;
			}
		}
		graphics.DrawRectangle(pen, new Rectangle(num, num2, num7, num8));
		graphics.Dispose();
	}
}
