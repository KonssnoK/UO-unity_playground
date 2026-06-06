using System.Drawing;
using KUtility;
using Mythic.Package;
using Paloma;

namespace UOReader;

public class TextureImage
{
	private static string[] m_a;

	private static TextureImage b;

	private MythicPackage[] c;

	private TextureImage()
	{
		c = new MythicPackage[TextureImage.m_a.Length];
		for (int i = 0; i < TextureImage.m_a.Length; i++)
		{
			c[i] = new MythicPackage(TextureImage.m_a[i]);
		}
	}

	public static TextureImage GetTextureImage()
	{
		if (b == null)
		{
			b = new TextureImage();
		}
		return b;
	}

	public Bitmap GetFromNAME(string fulltid, MythicPackage m_UOP, bool isDDS)
	{
		for (int i = 0; i < m_UOP.Blocks.Count; i++)
		{
			for (int j = 0; j < m_UOP.Blocks[i].Files.Count; j++)
			{
				if (m_UOP.Blocks[i].Files[j].FileHash == HashDictionary.HashFileName(fulltid))
				{
					byte[] array = m_UOP.Blocks[i].Files[j].Unpack(m_UOP.FileInfo.FullName);
					if (isDDS)
					{
						DDSImage dDSImage = new DDSImage(array);
						return dDSImage.images[0];
					}
					return TargaImage.LoadTargaImage(array);
				}
			}
		}
		return null;
	}

	public Bitmap GetFromTGA(string path, out bool isEC)
	{
		string text = "";
		string text2 = "";
		string text3 = "";
		MythicPackage mythicPackage = null;
		isEC = false;
		if (path.Contains("TileArtLegacy\\"))
		{
			text = path.Substring(path.IndexOf("TileArtLegacy\\") + "TileArtLegacy\\".Length);
			text2 = "build/tileartlegacy/";
			text3 = Utils.GetStringValue(Utils.FileNames.LegacyTexture);
		}
		else
		{
			if (!path.Contains("TileArtEnhanced\\"))
			{
				if (path.Contains("Textures\\"))
				{
					return a(path);
				}
				if (path.Contains("WorldArt\\"))
				{
					return a(path, out isEC, A_2: true);
				}
				return null;
			}
			text = path.Substring(path.IndexOf("TileArtEnhanced\\") + "TileArtEnhanced\\".Length);
			text2 = "build/worldart/";
			text3 = Utils.GetStringValue(Utils.FileNames.Texture);
			isEC = true;
		}
		int length = text.Length - ".tga".Length;
		string text4 = text.Substring(0, length);
		if (text4.Length < 8)
		{
			int num = 8 - text4.Length;
			for (int i = 0; i < num; i++)
			{
				text4 = "0" + text4;
			}
		}
		string fulltid = text2 + text4 + ".dds";
		for (int j = 0; j < c.Length; j++)
		{
			if ("\\" + c[j].FileInfo.Name == text3)
			{
				mythicPackage = c[j];
				return GetFromNAME(fulltid, mythicPackage, isDDS: true);
			}
		}
		fulltid = text2 + text4 + ".tga";
		for (int k = 0; k < c.Length; k++)
		{
			if ("\\" + c[k].FileInfo.Name == text3)
			{
				mythicPackage = c[k];
				return GetFromNAME(fulltid, mythicPackage, isDDS: false);
			}
		}
		return null;
	}

	private Bitmap a(string A_0, out bool A_1, bool A_2)
	{
		MythicPackage mythicPackage = null;
		string text = A_0.Substring(A_0.IndexOf("WorldArt\\") + "WorldArt\\".Length);
		if (text.Contains("_"))
		{
			text = text.Substring(0, text.IndexOf("_")) + ".tga";
		}
		int length = text.Length - ".tga".Length;
		string text2 = text.Substring(0, length);
		if (text2.Length < 8)
		{
			int num = 8 - text2.Length;
			for (int i = 0; i < num; i++)
			{
				text2 = "0" + text2;
			}
		}
		string[] array = new string[2] { ".dds", ".tga" };
		for (int j = 0; j < 2; j++)
		{
			string text3 = (A_2 ? "build/worldart/" : "build/tileartlegacy/");
			if (!A_2)
			{
				Utils.GetStringValue(Utils.FileNames.LegacyTexture);
			}
			else
			{
				Utils.GetStringValue(Utils.FileNames.Texture);
			}
			for (int k = 0; k < array.Length; k++)
			{
				string fulltid = text3 + text2 + array[k];
				mythicPackage = c[(!A_2) ? 1u : 0u];
				Bitmap fromNAME = GetFromNAME(fulltid, mythicPackage, isDDS: true);
				if (fromNAME != null)
				{
					A_1 = A_2;
					return fromNAME;
				}
			}
			A_2 = !A_2;
		}
		A_1 = false;
		return null;
	}

	private Bitmap a(string A_0)
	{
		string text = A_0.Substring(A_0.IndexOf("Textures\\") + "Textures\\".Length);
		text = "data/effects/" + text;
		for (int i = 0; i < c.Length; i++)
		{
			Bitmap fromNAME = GetFromNAME(text, c[i], isDDS: false);
			if (fromNAME != null)
			{
				return fromNAME;
			}
		}
		return null;
	}

	static TextureImage()
	{
		TextureImage.m_a = new string[5]
		{
			Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Texture),
			Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.LegacyTexture),
			Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.EffectTexture),
			Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.SystemTextures),
			Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.TerrainTexture)
		};
		b = null;
	}
}
