using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using KUtility;
using UOReader.Core;

namespace UOReader.Hues;

public class HuesControl : UserControl
{
	private IContainer m_a;

	private TreeView b;

	private Label c;

	private TextBox d;

	private PictureBox e;

	public HuesControl()
	{
		a();
		if (FilePointers.hues != null)
		{
			d.Text = FilePointers.hues.HueNodes.Count().ToString();
			b.Nodes.AddRange(FilePointers.hues.HueNodes.ToArray());
		}
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		Image image;
		if (A_1.Node.Text.Contains(".dds"))
		{
			DDSImage dDSImage = new DDSImage((byte[])A_1.Node.Tag);
			image = dDSImage.images[0];
		}
		else
		{
			if (!A_1.Node.Text.Contains(".bmp"))
			{
				return;
			}
			using MemoryStream stream = new MemoryStream((byte[])A_1.Node.Tag);
			Image image2 = Image.FromStream(stream);
			image = new Bitmap(image2.Width, image2.Height * 100);
			Graphics graphics = Graphics.FromImage(image);
			for (int i = 0; i < 50; i++)
			{
				Rectangle destRect = new Rectangle(0, i, image2.Width, 1);
				Rectangle srcRect = new Rectangle(0, 0, image2.Width, 1);
				Rectangle destRect2 = new Rectangle(0, i + 50, image2.Width, 1);
				Rectangle srcRect2 = new Rectangle(0, 1, image2.Width, 1);
				graphics.DrawImage(image2, destRect, srcRect, GraphicsUnit.Pixel);
				graphics.DrawImage(image2, destRect2, srcRect2, GraphicsUnit.Pixel);
			}
			graphics.Dispose();
		}
		e.BackgroundImageLayout = ImageLayout.Center;
		e.Image = image;
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
		c = new Label();
		d = new TextBox();
		e = new PictureBox();
		((ISupportInitialize)e).BeginInit();
		SuspendLayout();
		b.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		b.Location = new Point(10, 29);
		b.Name = "tree_hues";
		b.Size = new Size(216, 328);
		b.TabIndex = 8;
		b.AfterSelect += a;
		c.AutoSize = true;
		c.Location = new Point(7, 6);
		c.Name = "label1";
		c.Size = new Size(38, 13);
		c.TabIndex = 7;
		c.Text = "Count:";
		d.Location = new Point(51, 3);
		d.Name = "txt_count";
		d.ReadOnly = true;
		d.Size = new Size(175, 20);
		d.TabIndex = 6;
		e.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		e.BorderStyle = BorderStyle.FixedSingle;
		e.Location = new Point(232, 29);
		e.Name = "pBox";
		e.Size = new Size(187, 328);
		e.TabIndex = 9;
		e.TabStop = false;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(e);
		base.Controls.Add(b);
		base.Controls.Add(c);
		base.Controls.Add(d);
		base.Name = "HuesControl";
		base.Size = new Size(422, 360);
		((ISupportInitialize)e).EndInit();
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
