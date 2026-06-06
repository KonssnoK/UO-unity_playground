using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using UOReader.Core;

namespace UOReader;

public class TerrainDefinition : UserControl
{
	private IContainer m_a;

	private RichTextBox b;

	private TextBox c;

	private Label d;

	private TreeView e;

	private PictureBox f;

	public TerrainDefinition()
	{
		a();
		if (FilePointers.terrainDefinition != null)
		{
			c.Text = FilePointers.terrainDefinition.FileCount.ToString();
			e.Nodes.AddRange(FilePointers.terrainDefinition.TerrainNodes.ToArray());
		}
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		byte[] data = (byte[])A_1.Node.Tag;
		TerrainDefinitionItem terrainDefinitionItem = new TerrainDefinitionItem(data);
		b.Text = terrainDefinitionItem.ToString();
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
		b = new RichTextBox();
		c = new TextBox();
		d = new Label();
		e = new TreeView();
		f = new PictureBox();
		((ISupportInitialize)f).BeginInit();
		SuspendLayout();
		b.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		b.BorderStyle = BorderStyle.FixedSingle;
		b.Location = new Point(172, 14);
		b.Name = "txt_display";
		b.ReadOnly = true;
		b.ScrollBars = RichTextBoxScrollBars.Vertical;
		b.Size = new Size(277, 304);
		b.TabIndex = 0;
		b.Text = "";
		b.WordWrap = false;
		c.Location = new Point(53, 14);
		c.Name = "txt_count";
		c.ReadOnly = true;
		c.Size = new Size(114, 20);
		c.TabIndex = 2;
		d.AutoSize = true;
		d.Location = new Point(9, 17);
		d.Name = "label1";
		d.Size = new Size(38, 13);
		d.TabIndex = 3;
		d.Text = "Count:";
		e.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		e.Location = new Point(12, 40);
		e.Name = "tree_terr";
		e.Size = new Size(155, 278);
		e.TabIndex = 4;
		e.AfterSelect += a;
		f.Location = new Point(455, 14);
		f.Name = "pBox";
		f.Size = new Size(141, 104);
		f.TabIndex = 5;
		f.TabStop = false;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(f);
		base.Controls.Add(e);
		base.Controls.Add(d);
		base.Controls.Add(c);
		base.Controls.Add(b);
		base.Name = "TerrainDefinition";
		base.Size = new Size(599, 333);
		((ISupportInitialize)f).EndInit();
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
