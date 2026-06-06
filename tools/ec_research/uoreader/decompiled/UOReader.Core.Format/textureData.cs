using System.Collections.Generic;
using System.Windows.Forms;

namespace UOReader.Core.Format;

public class textureData
{
	public List<TreeNode> TextureNodes = new List<TreeNode>();

	public Textures texture;

	public TextureType type;

	public static void LoadUOP(Textures tex, TextureType tt)
	{
		textureData textureData2 = new textureData();
		textureData2.texture = tex;
		for (int i = 0; i < textureData2.texture.UOP.Blocks.Count; i++)
		{
			TreeNode treeNode = new TreeNode();
			treeNode.Text = "Block " + i;
			treeNode.Tag = i;
			textureData2.TextureNodes.Add(treeNode);
		}
		switch (tt)
		{
		case TextureType.ECTexture:
			FilePointers.ECtexture = textureData2;
			textureData2.type = TextureType.ECTexture;
			break;
		case TextureType.MLTexture:
			FilePointers.MLtexture = textureData2;
			textureData2.type = TextureType.MLTexture;
			break;
		case TextureType.EffectTexture:
			FilePointers.EFtexture = textureData2;
			textureData2.type = TextureType.EffectTexture;
			break;
		}
	}
}
