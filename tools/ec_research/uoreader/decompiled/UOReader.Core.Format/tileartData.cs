using System.Collections.Generic;
using System.Windows.Forms;
using Mythic.Package;

namespace UOReader.Core.Format;

public class tileartData
{
	public List<TreeNode> TileartNodes = new List<TreeNode>();

	public MythicPackage UOP;

	public static void LoadUOP(string path)
	{
		MythicPackage mythicPackage = new MythicPackage(path);
		tileartData tileartData2 = new tileartData();
		tileartData2.UOP = mythicPackage;
		for (int i = 0; i < mythicPackage.Blocks.Count; i++)
		{
			TreeNode treeNode = new TreeNode();
			treeNode.Text = "Block " + i;
			treeNode.Tag = i;
			tileartData2.TileartNodes.Add(treeNode);
		}
		FilePointers.TileartNEW = tileartData2;
	}
}
