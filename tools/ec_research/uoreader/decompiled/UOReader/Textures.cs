using System.Drawing;
using KUtility;
using Mythic.Package;
using UOReader.Core;

namespace UOReader;

public class Textures
{
	private MythicPackage a;

	private Tileart b;

	public MythicPackage UOP => a;

	public Textures(string path)
	{
		a = new MythicPackage(path);
		b = FilePointers.tileart;
	}

	public Texture GetFromNAME(string fulltid)
	{
		Texture texture = new Texture();
		for (int i = 0; i < a.Blocks.Count; i++)
		{
			for (int j = 0; j < a.Blocks[i].Files.Count; j++)
			{
				if (HashDictionary.Get(a.Blocks[i].Files[j].FileHash, add: false) == fulltid)
				{
					byte[] rawdata = a.Blocks[i].Files[j].Unpack(a.FileInfo.FullName);
					DDSImage dDSImage = new DDSImage(rawdata);
					Bitmap image = dDSImage.images[0];
					texture.Image = image;
					string tid = "null";
					string[] array = fulltid.Split('/');
					if (array.Length >= 3)
					{
						tid = array[2].Remove(array[2].IndexOf('.'));
					}
					texture.Props = b.GetFromID(tid);
					if (a.FileInfo.Name == "Texture.uop")
					{
						texture.IsEC = true;
					}
					return texture;
				}
			}
		}
		texture.Image = null;
		texture.Props = null;
		return texture;
	}

	public Texture GetFromHASH(string hash)
	{
		Texture texture = new Texture();
		ulong num = ulong.Parse(hash);
		for (int i = 0; i < a.Blocks.Count; i++)
		{
			for (int j = 0; j < a.Blocks[i].Files.Count; j++)
			{
				if (a.Blocks[i].Files[j].FileHash == num)
				{
					byte[] rawdata = a.Blocks[i].Files[j].Unpack(a.FileInfo.FullName);
					DDSImage dDSImage = new DDSImage(rawdata);
					Bitmap image = dDSImage.images[0];
					texture.Image = image;
					texture.Props = null;
					return texture;
				}
			}
		}
		texture.Image = null;
		texture.Props = null;
		return texture;
	}

	public Texture GetFromID(string tid)
	{
		if (tid.Length < 8)
		{
			int num = 8 - tid.Length;
			for (int i = 0; i < num; i++)
			{
				tid = "0" + tid;
			}
		}
		string fulltid = "build/tileartlegacy/" + tid + ".dds";
		if (a.FileInfo.Name == "Texture.uop")
		{
			fulltid = "build/worldart/" + tid + ".dds";
		}
		return GetFromNAME(fulltid);
	}
}
