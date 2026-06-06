using System.IO;
using System.Text;

namespace UOReader;

public class TextureItem
{
	public byte TexturePresent;

	public byte unk1;

	public int NameIndex;

	public byte count1;

	public TextureItemImage[] tiArray;

	public uint count2;

	public int[] unk8;

	public uint count3;

	public float[] unk9;

	public static TextureItem ReadTexture(BinaryReader r)
	{
		TextureItem textureItem = new TextureItem();
		textureItem.TexturePresent = r.ReadByte();
		if (textureItem.TexturePresent != 0)
		{
			textureItem.unk1 = r.ReadByte();
			textureItem.NameIndex = r.ReadInt32();
			textureItem.count1 = r.ReadByte();
			textureItem.tiArray = new TextureItemImage[textureItem.count1];
			for (int i = 0; i < textureItem.count1; i++)
			{
				textureItem.tiArray[i] = new TextureItemImage();
				textureItem.tiArray[i].strDic = r.ReadInt32();
				textureItem.tiArray[i].unk4 = r.ReadByte();
				textureItem.tiArray[i].unk5 = r.ReadSingle();
				textureItem.tiArray[i].unk6 = r.ReadInt32();
				textureItem.tiArray[i].unk7 = r.ReadInt32();
			}
			textureItem.count2 = r.ReadUInt32();
			textureItem.unk8 = new int[textureItem.count2];
			for (int j = 0; j < textureItem.count2; j++)
			{
				textureItem.unk8[j] = r.ReadInt32();
			}
			textureItem.count3 = r.ReadUInt32();
			textureItem.unk9 = new float[textureItem.count3];
			for (int k = 0; k < textureItem.count3; k++)
			{
				textureItem.unk9[k] = r.ReadSingle();
			}
		}
		return textureItem;
	}

	public static string PrintTextureInfo(TextureItem t)
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("V7\t" + t.TexturePresent + " - Textures");
		if (t.TexturePresent == 0)
		{
			stringBuilder.AppendLine();
			return stringBuilder.ToString();
		}
		stringBuilder.AppendLine("Unk\t" + t.unk1);
		stringBuilder.AppendLine("\t" + StringDictionary.GetDictionary().GetStringAtPosition(t.NameIndex));
		stringBuilder.AppendLine("\tC7.1\t" + t.count1);
		for (int i = 0; i < t.tiArray.Length; i++)
		{
			stringBuilder.AppendLine("\t- " + i);
			stringBuilder.AppendLine("\t\t" + StringDictionary.GetDictionary().GetStringAtPosition(t.tiArray[i].strDic));
			stringBuilder.AppendLine("\t\t " + t.tiArray[i].unk4 + " " + t.tiArray[i].unk5.ToString() + " " + t.tiArray[i].unk6 + " " + t.tiArray[i].unk7);
		}
		stringBuilder.AppendLine("\tC7.2\t" + t.count2);
		for (int j = 0; j < t.count2; j++)
		{
			stringBuilder.AppendLine("\t- " + j + "\t" + t.unk8[j]);
		}
		stringBuilder.AppendLine("\tC7.3\t" + t.count3);
		for (int k = 0; k < t.count3; k++)
		{
			stringBuilder.AppendLine("\t- " + k + "\t" + t.unk9[k]);
		}
		stringBuilder.AppendLine();
		return stringBuilder.ToString();
	}
}
