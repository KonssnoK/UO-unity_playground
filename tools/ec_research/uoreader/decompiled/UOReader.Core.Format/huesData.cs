using System.Collections.Generic;
using System.Windows.Forms;
using Mythic.Package;

namespace UOReader.Core.Format;

public class huesData
{
	public List<TreeNode> HueNodes = new List<TreeNode>();

	public static void LoadUOP(string path)
	{
		MythicPackage mythicPackage = new MythicPackage(path);
		huesData huesData2 = new huesData();
		for (int i = 0; i < mythicPackage.Blocks.Count; i++)
		{
			for (int j = 0; j < mythicPackage.Blocks[i].FileCount; j++)
			{
				TreeNode treeNode = new TreeNode();
				if (HashDictionary.Contains(mythicPackage.Blocks[i].Files[j].FileHash))
				{
					treeNode.Text = HashDictionary.Get(mythicPackage.Blocks[i].Files[j].FileHash, add: false);
					if (treeNode.Text != null && (treeNode.Text.Length == 0 || treeNode.Text.Trim().Length == 0))
					{
						HashDictionary.Unset(mythicPackage.Blocks[i].Files[j].FileHash);
						HashDictionary.SaveDictionary("Dictionary.dic");
						treeNode.Text = mythicPackage.Blocks[i].Files[j].FileHash.ToString();
					}
				}
				else
				{
					treeNode.Text = mythicPackage.Blocks[i].Files[j].FileHash.ToString();
				}
				treeNode.Tag = mythicPackage.Blocks[i].Files[j].Unpack(mythicPackage.FileInfo.FullName);
				huesData2.HueNodes.Add(treeNode);
			}
		}
		FilePointers.hues = huesData2;
	}
}
