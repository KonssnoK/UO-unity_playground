using System.Collections.Generic;
using System.Windows.Forms;
using Mythic.Package;

namespace UOReader.Core.Format;

public class terrainDefinitionData
{
	public List<TreeNode> TerrainNodes = new List<TreeNode>();

	public int FileCount;

	public static void LoadUOP(string path)
	{
		MythicPackage mythicPackage = new MythicPackage(path);
		terrainDefinitionData terrainDefinitionData2 = new terrainDefinitionData();
		int num = 0;
		for (int i = 0; i < mythicPackage.Blocks.Count; i++)
		{
			num += mythicPackage.Blocks[i].Files.Count;
			for (int j = 0; j < mythicPackage.Blocks[i].Files.Count; j++)
			{
				TreeNode treeNode = new TreeNode();
				string text = null;
				if (HashDictionary.Contains(mythicPackage.Blocks[i].Files[j].FileHash))
				{
					text = HashDictionary.Get(mythicPackage.Blocks[i].Files[j].FileHash, add: false);
					if (text != null && (text.Length == 0 || text.Trim().Length == 0))
					{
						HashDictionary.Unset(mythicPackage.Blocks[i].Files[j].FileHash);
						HashDictionary.SaveDictionary("Dictionary.dic");
						text = mythicPackage.Blocks[i].Files[j].FileHash.ToString();
					}
					else if (text == null)
					{
						text = mythicPackage.Blocks[i].Files[j].FileHash.ToString();
					}
				}
				else
				{
					text = mythicPackage.Blocks[i].Files[j].FileHash.ToString();
				}
				treeNode.Text = text;
				treeNode.Tag = mythicPackage.Blocks[i].Files[j].Unpack(mythicPackage.FileInfo.FullName);
				terrainDefinitionData2.TerrainNodes.Add(treeNode);
			}
		}
		terrainDefinitionData2.FileCount = num;
		FilePointers.terrainDefinition = terrainDefinitionData2;
	}
}
