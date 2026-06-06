using System.Collections.Generic;
using System.Windows.Forms;
using Mythic.Package;

namespace UOReader.Core.Format;

public class localizedStringData
{
	public List<TreeNode> ClilocsNodes = new List<TreeNode>();

	public int FileCount;

	public static void LoadUOP(string path)
	{
		MythicPackage mythicPackage = new MythicPackage(path);
		localizedStringData localizedStringData2 = new localizedStringData();
		int num = 0;
		for (int i = 0; i < mythicPackage.Blocks.Count; i++)
		{
			num += mythicPackage.Blocks[i].Files.Count;
			for (int j = 0; j < mythicPackage.Blocks[i].Files.Count; j++)
			{
				string text = "UnknownName";
				TreeNode treeNode = new TreeNode(text);
				if (HashDictionary.Contains(mythicPackage.Blocks[i].Files[j].FileHash))
				{
					string text2 = HashDictionary.Get(mythicPackage.Blocks[i].Files[j].FileHash, add: false);
					treeNode.Text = text2.Substring(text2.LastIndexOf('/'));
				}
				treeNode.Tag = mythicPackage.Blocks[i].Files[j].Unpack(mythicPackage.FileInfo.FullName);
				localizedStringData2.ClilocsNodes.Add(treeNode);
			}
		}
		localizedStringData2.FileCount = num;
		FilePointers.localizedString = localizedStringData2;
	}
}
