using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Mythic.Package;
using UOReader.Core;

namespace UOReader;

public class TileartControlNew : UserControl
{
	private byte[] m_a;

	private IContainer b;

	private SplitContainer c;

	private TreeView d;

	private RichTextBox e;

	private PictureBox f;

	private Panel g;

	private CheckBox h;

	public TileartControlNew()
	{
		a();
		if (FilePointers.TileartNEW != null)
		{
			d.Nodes.AddRange(FilePointers.TileartNEW.TileartNodes.ToArray());
		}
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		if (A_1.Node.Level == 0)
		{
			int i;
			for (i = 0; i < d.Nodes.Count; i++)
			{
				d.Nodes[i].Collapse();
				d.Nodes[i].Nodes.Clear();
			}
			i = (int)A_1.Node.Tag;
			MythicPackage uOP = FilePointers.TileartNEW.UOP;
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
				d.Nodes[i].Nodes.Add(treeNode);
			}
			d.Nodes[i].Expand();
		}
		else if (A_1.Node.Level == 1)
		{
			this.m_a = (byte[])A_1.Node.Tag;
			a(this.m_a);
			d.Focus();
		}
	}

	private void a(byte[] A_0)
	{
		foreach (Control control in g.Controls)
		{
			control.Dispose();
		}
		g.Controls.Clear();
		TileartItem tileartItem = new TileartItem(A_0);
		e.Text = tileartItem.DumpDatas();
		int num = 0;
		for (int i = 0; i < tileartItem.m_textures.Length; i++)
		{
			TextureItem textureItem = tileartItem.m_textures[i];
			if (textureItem.TexturePresent != 0)
			{
				num += a(textureItem, tileartItem, num);
			}
		}
		Bitmap image = new Bitmap(50, 50);
		if (tileartItem.m_radarCol != null)
		{
			Graphics graphics = Graphics.FromImage(image);
			SolidBrush brush = new SolidBrush(Color.FromArgb(tileartItem.m_radarCol.A, tileartItem.m_radarCol.R, tileartItem.m_radarCol.G, tileartItem.m_radarCol.B));
			graphics.FillRectangle(brush, new Rectangle(0, 0, 49, 49));
			graphics.Dispose();
		}
		f.Image = image;
	}

	private int a(TextureItem A_0, TileartItem A_1, int A_2)
	{
		int num = 0;
		int num2 = 0;
		for (int i = 0; i < A_0.tiArray.Length; i++)
		{
			PictureBox pictureBox = new PictureBox();
			pictureBox.Location = new Point(num, A_2);
			pictureBox.BorderStyle = BorderStyle.FixedSingle;
			g.Controls.Add(pictureBox);
			string stringAtPosition = StringDictionary.GetDictionary().GetStringAtPosition(A_0.tiArray[i].strDic);
			Bitmap fromTGA = TextureImage.GetTextureImage().GetFromTGA(stringAtPosition, out var isEC);
			if (fromTGA == null)
			{
				pictureBox.Width = 50;
				pictureBox.Height = 50;
				num += pictureBox.Width + 10;
				if (pictureBox.Height > num2)
				{
					num2 = pictureBox.Height;
				}
				continue;
			}
			if (stringAtPosition.Contains("noise"))
			{
				fromTGA = (Bitmap)(pictureBox.Image = ResizeBitmap(fromTGA, 100, 100));
				pictureBox.Width = fromTGA.Width;
				pictureBox.Height = fromTGA.Height;
				if (pictureBox.Height > num2)
				{
					num2 = pictureBox.Height;
				}
				num += pictureBox.Width + 10;
				continue;
			}
			int num3 = 0;
			int num4 = 0;
			if (h.Checked)
			{
				if (isEC)
				{
					num3 = A_1.m_imgoffEC[4];
					num4 = A_1.m_imgoffEC[5];
				}
				else
				{
					num3 = A_1.m_imgoff2D[4];
					num4 = A_1.m_imgoff2D[5];
				}
			}
			pictureBox.Width = fromTGA.Width + Math.Abs(num3);
			pictureBox.Height = fromTGA.Height + Math.Abs(num4);
			if (pictureBox.Height > num2)
			{
				num2 = pictureBox.Height;
			}
			num += pictureBox.Width + 10;
			Bitmap bitmap = new Bitmap(pictureBox.Width, pictureBox.Height);
			Graphics graphics = Graphics.FromImage(bitmap);
			if (num4 < 0)
			{
				num4 = 0;
			}
			if (num3 < 0)
			{
				num3 = 0;
			}
			graphics.DrawImage(fromTGA, num3, num4);
			TileartItem.DrawBorders(bitmap, isEC, A_1, h.Checked);
			Pen pen = new Pen(Color.Red);
			graphics.DrawRectangle(pen, 0, pictureBox.Height / 2 - 3, num3, 6);
			graphics.DrawRectangle(pen, pictureBox.Width / 2 - 3, 0, 6, num4);
			pictureBox.Image = bitmap;
		}
		return num2 + 5;
	}

	public Bitmap ResizeBitmap(Bitmap b, int nWidth, int nHeight)
	{
		Bitmap bitmap = new Bitmap(nWidth, nHeight);
		using Graphics graphics = Graphics.FromImage(bitmap);
		graphics.DrawImage(b, 0, 0, nWidth, nHeight);
		return bitmap;
	}

	private void a(object A_0, EventArgs A_1)
	{
		if (this.m_a != null)
		{
			a(this.m_a);
			d.Focus();
		}
	}

	protected override void Dispose(bool disposing)
	{
		if (disposing && b != null)
		{
			b.Dispose();
		}
		base.Dispose(disposing);
	}

	private void a()
	{
		c = new SplitContainer();
		g = new Panel();
		f = new PictureBox();
		d = new TreeView();
		e = new RichTextBox();
		h = new CheckBox();
		((ISupportInitialize)c).BeginInit();
		c.Panel1.SuspendLayout();
		c.Panel2.SuspendLayout();
		c.SuspendLayout();
		((ISupportInitialize)f).BeginInit();
		SuspendLayout();
		c.Dock = DockStyle.Fill;
		c.Location = new Point(0, 0);
		c.Name = "splitContainer1";
		c.Panel1.Controls.Add(h);
		c.Panel1.Controls.Add(g);
		c.Panel1.Controls.Add(f);
		c.Panel1.Controls.Add(d);
		c.Panel2.Controls.Add(e);
		c.Size = new Size(1117, 557);
		c.SplitterDistance = 816;
		c.TabIndex = 35;
		g.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		g.AutoScroll = true;
		g.BorderStyle = BorderStyle.FixedSingle;
		g.Location = new Point(201, 3);
		g.Name = "panelTextures";
		g.Size = new Size(612, 491);
		g.TabIndex = 38;
		f.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		f.BorderStyle = BorderStyle.FixedSingle;
		f.Location = new Point(212, 500);
		f.Name = "pBox_RadarCol";
		f.Size = new Size(50, 50);
		f.TabIndex = 37;
		f.TabStop = false;
		d.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		d.Location = new Point(3, 3);
		d.Name = "tree_texture";
		d.Size = new Size(192, 551);
		d.TabIndex = 36;
		d.AfterSelect += a;
		e.BorderStyle = BorderStyle.FixedSingle;
		e.Dock = DockStyle.Fill;
		e.Location = new Point(0, 0);
		e.Name = "txt_display";
		e.ReadOnly = true;
		e.Size = new Size(297, 557);
		e.TabIndex = 31;
		e.Text = "";
		e.WordWrap = false;
		h.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		h.AutoSize = true;
		h.Location = new Point(268, 500);
		h.Name = "chk_offsets";
		h.Size = new Size(85, 17);
		h.TabIndex = 39;
		h.Text = "Draw offsets";
		h.UseVisualStyleBackColor = true;
		h.CheckedChanged += a;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(c);
		base.Name = "TileartControlNew";
		base.Size = new Size(1117, 557);
		c.Panel1.ResumeLayout(performLayout: false);
		c.Panel1.PerformLayout();
		c.Panel2.ResumeLayout(performLayout: false);
		((ISupportInitialize)c).EndInit();
		c.ResumeLayout(performLayout: false);
		((ISupportInitialize)f).EndInit();
		ResumeLayout(performLayout: false);
	}
}
