using System;
using System.IO;
using System.Text;

namespace UOReader;

public class TerrainDefinitionItem
{
	public int nameid;

	public uint id;

	public float unk;

	public float unk2;

	public float unk3;

	public uint tilesCount;

	private TerrainDefinitionTileAlias[] a;

	private TextureItem b;

	private byte[] c;

	public TerrainDefinitionItem(byte[] data)
	{
		c = data;
		Load();
	}

	public void Load()
	{
		using MemoryStream input = new MemoryStream(c);
		using BinaryReader binaryReader = new BinaryReader(input);
		nameid = binaryReader.ReadInt32();
		id = binaryReader.ReadUInt32();
		unk = binaryReader.ReadSingle();
		unk2 = binaryReader.ReadSingle();
		unk3 = binaryReader.ReadSingle();
		tilesCount = binaryReader.ReadUInt32();
		a = new TerrainDefinitionTileAlias[tilesCount];
		for (int i = 0; i < tilesCount; i++)
		{
			a[i] = new TerrainDefinitionTileAlias();
			a[i].countindex = binaryReader.ReadUInt32();
			a[i].alias = binaryReader.ReadUInt32();
			a[i].tileFlags = binaryReader.ReadUInt64();
		}
		b = TextureItem.ReadTexture(binaryReader);
	}

	public override string ToString()
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("Name: " + StringDictionary.GetDictionary().GetStringAtPosition(nameid));
		stringBuilder.AppendLine("ID: " + id);
		stringBuilder.AppendLine(unk.ToString() ?? "");
		stringBuilder.AppendLine("UFloat: " + unk2);
		stringBuilder.AppendLine(unk3.ToString() ?? "");
		stringBuilder.AppendLine();
		stringBuilder.AppendLine("Count: " + tilesCount);
		for (int i = 0; i < tilesCount; i++)
		{
			stringBuilder.AppendLine("-\t#" + a[i].countindex);
			stringBuilder.AppendLine("\tAlias " + a[i].alias);
			TileFlag tileFlag = (TileFlag)Enum.Parse(typeof(TileFlag), a[i].tileFlags.ToString());
			stringBuilder.Append("\tFlags: " + tileFlag);
			stringBuilder.AppendLine();
		}
		stringBuilder.AppendLine();
		stringBuilder.Append(TextureItem.PrintTextureInfo(b));
		return stringBuilder.ToString();
	}
}
