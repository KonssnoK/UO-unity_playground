using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;
using Mythic.Package;

namespace UOReader.Core.Format;

public class animationFrameData
{
	public List<TreeNode> UOPCollection = new List<TreeNode>();

	public List<MythicPackage> UOPs = new List<MythicPackage>();

	public static void LoadUOP(string path)
	{
		animationFrameData animationFrameData2 = new animationFrameData();
		for (int i = 1; i < 7; i++)
		{
			string text = path + i + ".uop";
			if (!File.Exists(text))
			{
				return;
			}
			animationFrameData2.UOPs.Add(new MythicPackage(text));
			int num = animationFrameData2.UOPs.Count - 1;
			TreeNode treeNode = new TreeNode(animationFrameData2.UOPs[num].FileInfo.Name);
			treeNode.Tag = num;
			animationFrameData2.UOPCollection.Add(treeNode);
		}
		FilePointers.animationFrame = animationFrameData2;
	}
}
