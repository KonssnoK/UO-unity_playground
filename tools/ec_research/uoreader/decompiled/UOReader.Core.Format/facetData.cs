using System.Collections.Generic;
using System.Windows.Forms;
using Mythic.Package;

namespace UOReader.Core.Format;

public class facetData
{
	public List<TreeNode> BlocksNodes = new List<TreeNode>();

	public MythicPackage UOP;

	public static void LoadUOP(string path)
	{
	}
}
