using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;
using UOReader.Core;

namespace UOReader.EffectDefinition;

public class EffectDefinitionCollection : UserControl
{
	private IContainer m_a;

	private RichTextBox b;

	private TextBox c;

	private Label d;

	private TreeView e;

	public EffectDefinitionCollection()
	{
		a();
		if (FilePointers.effectDefinition != null)
		{
			e.Nodes.AddRange(FilePointers.effectDefinition.EffectDefinitionNodes.ToArray());
			c.Text = FilePointers.effectDefinition.FileCount.ToString();
		}
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		byte[] buffer = (byte[])A_1.Node.Tag;
		StringBuilder stringBuilder = new StringBuilder();
		using (MemoryStream input = new MemoryStream(buffer))
		{
			using BinaryReader binaryReader = new BinaryReader(input);
			while (binaryReader.BaseStream.Position < binaryReader.BaseStream.Length)
			{
				stringBuilder.Append(binaryReader.ReadByte().ToString("X") + " ");
			}
		}
		b.Text = stringBuilder.ToString();
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
		SuspendLayout();
		b.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		b.Location = new Point(251, 3);
		b.Name = "txt_display";
		b.ReadOnly = true;
		b.Size = new Size(262, 335);
		b.TabIndex = 0;
		b.Text = "";
		c.Location = new Point(65, 3);
		c.Name = "txt_count";
		c.Size = new Size(180, 20);
		c.TabIndex = 2;
		d.AutoSize = true;
		d.Location = new Point(21, 6);
		d.Name = "label1";
		d.Size = new Size(38, 13);
		d.TabIndex = 3;
		d.Text = "Count:";
		e.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		e.Location = new Point(3, 29);
		e.Name = "tree_effect";
		e.Size = new Size(242, 309);
		e.TabIndex = 4;
		e.AfterSelect += a;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(e);
		base.Controls.Add(d);
		base.Controls.Add(c);
		base.Controls.Add(b);
		base.Name = "EffectDefinitionCollection";
		base.Size = new Size(516, 341);
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
