using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Mythic.Package;
using UOReader.Core;

namespace UOReader.Facets;

public class FacetsControl : UserControl
{
	private IContainer m_a;

	private TreeView b;

	private RichTextBox c;

	private PictureBox d;

	public FacetsControl()
	{
		a();
		if (FilePointers.facet != null)
		{
			b.Nodes.AddRange(FilePointers.facet.BlocksNodes.ToArray());
		}
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		if (A_1.Node.Level == 0)
		{
			int i;
			for (i = 0; i < b.Nodes.Count; i++)
			{
				b.Nodes[i].Collapse();
				b.Nodes[i].Nodes.Clear();
			}
			i = (int)A_1.Node.Tag;
			MythicPackage uOP = FilePointers.facet.UOP;
			for (int j = 0; j < uOP.Blocks[i].Files.Count; j++)
			{
				TreeNode treeNode = new TreeNode();
				string text = null;
				if (HashDictionary.Contains(uOP.Blocks[i].Files[j].FileHash))
				{
					text = HashDictionary.Get(uOP.Blocks[i].Files[j].FileHash, add: false);
					if (text != null && (text.Length == 0 || text.Trim().Length == 0))
					{
						HashDictionary.Unset(uOP.Blocks[i].Files[j].FileHash);
						HashDictionary.SaveDictionary("Dictionary.dic");
						text = uOP.Blocks[i].Files[j].FileHash.ToString();
					}
					else if (text == null)
					{
						text = uOP.Blocks[i].Files[j].FileHash.ToString();
					}
				}
				else
				{
					text = uOP.Blocks[i].Files[j].FileHash.ToString();
				}
				treeNode.Text = text;
				treeNode.Tag = uOP.Blocks[i].Files[j].Unpack(uOP.FileInfo.FullName);
				b.Nodes[i].Nodes.Add(treeNode);
			}
			b.Nodes[i].Expand();
		}
		else if (A_1.Node.Level == 1)
		{
			byte[] data = (byte[])A_1.Node.Tag;
			FacetSectorItem a_ = new FacetSectorItem(data);
			a(a_);
			b.Focus();
		}
	}

	private void a(FacetSectorItem A_0)
	{
		c.Text = A_0.ToString();
		d.Image = A_0.getImage();
	}

	protected override void Dispose(bool disposing)
	{
		if (disposing && this.m_a != null)
		{
			this.m_a.Dispose();
		}
		base.Dispose(disposing);
	}

	private void a()
	{
		b = new TreeView();
		c = new RichTextBox();
		d = new PictureBox();
		((ISupportInitialize)d).BeginInit();
		SuspendLayout();
		b.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		b.Location = new Point(12, 13);
		b.Name = "tree_facets";
		b.Size = new Size(141, 227);
		b.TabIndex = 0;
		b.AfterSelect += a;
		c.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		c.BorderStyle = BorderStyle.FixedSingle;
		c.Location = new Point(159, 13);
		c.Name = "txt_display";
		c.ReadOnly = true;
		c.Size = new Size(109, 227);
		c.TabIndex = 1;
		c.Text = "";
		c.WordWrap = false;
		d.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		d.Location = new Point(274, 13);
		d.Name = "pBox_display";
		d.Size = new Size(150, 227);
		d.TabIndex = 2;
		d.TabStop = false;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(d);
		base.Controls.Add(c);
		base.Controls.Add(b);
		base.Name = "FacetsControl";
		base.Size = new Size(427, 255);
		((ISupportInitialize)d).EndInit();
		ResumeLayout(performLayout: false);
	}
}
