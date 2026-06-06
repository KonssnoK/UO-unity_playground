using System.IO;
using System.Text;
using Mythic.Package;
using UOReader.TextureContainer;

namespace UOReader;

public class Tileart
{
	private MythicPackage a;

	public MythicPackage UOP => a;

	public Tileart(string p)
	{
		a = new MythicPackage(p);
	}

	public Tileprops GetFromID(string tid)
	{
		if (tid.Length < 8)
		{
			int num = 8 - tid.Length;
			for (int i = 0; i < num; i++)
			{
				tid = "0" + tid;
			}
		}
		string text = "build/tileart/" + tid + ".bin";
		for (int j = 0; j < a.Blocks.Count; j++)
		{
			for (int k = 0; k < a.Blocks[j].Files.Count; k++)
			{
				if (HashDictionary.Get(a.Blocks[j].Files[k].FileHash, add: false) == text)
				{
					byte[] stream = a.Blocks[j].Files[k].Unpack(a.FileInfo.FullName);
					Tileprops tileprops = new Tileprops();
					tileprops.Read(stream);
					return tileprops;
				}
			}
		}
		return null;
	}

	public void DoStatistics()
	{
		for (int i = 0; i < a.Blocks.Count; i++)
		{
			for (int j = 0; j < a.Blocks[i].Files.Count; j++)
			{
				if (HashDictionary.Get(a.Blocks[i].Files[j].FileHash, add: false) != null)
				{
					byte[] stream = a.Blocks[i].Files[j].Unpack(a.FileInfo.FullName);
					Tileprops tileprops = new Tileprops();
					tileprops.Read(stream);
				}
			}
		}
		using FileStream stream2 = new FileStream("tiledataSTATS.txt", FileMode.Append);
		using TextWriter textWriter = new StreamWriter(stream2);
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.Append("UnkTypes: \n");
		foreach (int key in Tileprops.UnkType_L.Keys)
		{
			stringBuilder.Append(key + "\t\t");
			if (key == 400)
			{
				stringBuilder.Append(Tileprops.UnkType_L[key].Count);
			}
			else
			{
				for (int k = 0; k < Tileprops.UnkType_L[key].Count; k++)
				{
					stringBuilder.Append(Tileprops.UnkType_L[key][k] + "\t");
				}
			}
			stringBuilder.AppendLine();
		}
		textWriter.WriteLine(stringBuilder.ToString());
		stringBuilder.AppendLine();
		stringBuilder.Remove(0, stringBuilder.Length - 1);
		stringBuilder.Append("Unk6: \n");
		foreach (int key2 in Tileprops.Unk6_L.Keys)
		{
			stringBuilder.Append(key2 + "\t\t");
			if (key2 == 0)
			{
				stringBuilder.Append(Tileprops.Unk6_L[key2].Count);
			}
			else
			{
				for (int l = 0; l < Tileprops.Unk6_L[key2].Count; l++)
				{
					stringBuilder.Append(Tileprops.Unk6_L[key2][l] + "\t");
				}
			}
			stringBuilder.AppendLine();
		}
		textWriter.WriteLine(stringBuilder.ToString());
		stringBuilder.AppendLine();
		stringBuilder.Remove(0, stringBuilder.Length - 1);
		stringBuilder.Append("Unk4: ");
		foreach (int item in Tileprops.Unk4_L)
		{
			stringBuilder.Append(item + "\t");
		}
		textWriter.WriteLine(stringBuilder.ToString());
	}
}
