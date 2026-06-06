using System.Collections.Generic;
using System.Windows.Forms;
using Mythic.Package;

namespace UOReader.Core.Format;

public class multiCollectionData
{
	public List<TreeNode> MultisNodes = new List<TreeNode>();

	public static void LoadUOP(string path)
	{
		MythicPackage mythicPackage = new MythicPackage(path);
		multiCollectionData multiCollectionData2 = new multiCollectionData();
		for (int i = 0; i < mythicPackage.Blocks.Count; i++)
		{
			for (int j = 0; j < mythicPackage.Blocks[i].FileCount; j++)
			{
				string text = "UnknownName";
				TreeNode treeNode = new TreeNode(text);
				if (HashDictionary.Contains(mythicPackage.Blocks[i].Files[j].FileHash))
				{
					treeNode.Text = HashDictionary.Get(mythicPackage.Blocks[i].Files[j].FileHash, add: false);
				}
				if (treeNode.Text.Length == 0 || treeNode.Text.Trim().Length == 0)
				{
					HashDictionary.Unset(mythicPackage.Blocks[i].Files[j].FileHash);
					HashDictionary.SaveDictionary("Dictionary.dic");
					treeNode.Text = "UnknownName";
				}
				treeNode.Tag = mythicPackage.Blocks[i].Files[j].Unpack(mythicPackage.FileInfo.FullName);
				multiCollectionData2.MultisNodes.Add(treeNode);
			}
		}
		FilePointers.multiCollection = multiCollectionData2;
	}
}
