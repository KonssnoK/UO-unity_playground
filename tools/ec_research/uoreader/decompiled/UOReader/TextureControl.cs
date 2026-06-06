using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Mythic.Package;
using UOReader.Core.Format;
using UOReader.TextureContainer;

namespace UOReader;

public class TextureControl : UserControl
{
	private textureData m_a;

	private IContainer b;

	private PictureBox c;

	private TreeView d;

	private TextBox e;

	private TextBox f;

	private Label g;

	private Label h;

	private Label i;

	private RichTextBox j;

	private RichTextBox k;

	private PictureBox l;

	private CheckBox m;

	private CheckBox n;

	public TextureControl()
	{
		a();
	}

	public void SetTexture(textureData tex)
	{
		if (tex != null)
		{
			this.m_a = tex;
			d.Nodes.AddRange(this.m_a.TextureNodes.ToArray());
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
			MythicPackage uOP = this.m_a.texture.UOP;
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
				if (m.Checked)
				{
					int num = treeNode.Text.LastIndexOf("/");
					if (num != -1)
					{
						int num2 = int.Parse(treeNode.Text.Substring(num + 1, 8));
						if (num2 < 39213)
						{
							continue;
						}
					}
				}
				treeNode.Tag = uOP.Blocks[i].Files[j].Unpack(uOP.FileInfo.FullName);
				d.Nodes[i].Nodes.Add(treeNode);
			}
			if (this.m_a.type == TextureType.ECTexture && n.Checked)
			{
				d.TreeViewNodeSorter = new Utils.NodeSorter();
				d.Sort();
			}
			d.Nodes[i].Expand();
		}
		else if (A_1.Node.Level == 1)
		{
			a(A_1.Node.Text);
		}
	}

	private void a(string A_0)
	{
		Texture texture = this.m_a.texture.GetFromNAME(A_0);
		if (texture.Image == null)
		{
			texture = this.m_a.texture.GetFromHASH(A_0);
		}
		if (texture.Image == null)
		{
			c.Image = new Bitmap(1, 1);
			return;
		}
		Bitmap image = texture.Image;
		Tileprops props = texture.Props;
		e.Text = image.Width.ToString();
		f.Text = image.Height.ToString();
		if (props == null)
		{
			j.Text = "No tiledata Found.";
			this.i.Text = A_0;
			k.Text = "";
		}
		else
		{
			this.i.Text = props.ID.ToString();
			j.Text = props.Dump;
			k.Text = props.FlagsDump;
		}
		lock (image)
		{
			for (int i = 0; i < image.Width; i++)
			{
				image.SetPixel(i, 0, Color.Black);
				image.SetPixel(i, image.Height - 1, Color.Black);
			}
			for (int i = 0; i < image.Height; i++)
			{
				image.SetPixel(0, i, Color.Black);
				image.SetPixel(image.Width - 1, i, Color.Black);
			}
		}
		Bitmap image2 = new Bitmap(50, 50);
		if (props != null)
		{
			Graphics graphics = Graphics.FromImage(image2);
			SolidBrush brush = new SolidBrush(Color.FromArgb(props.RadarCol[3], props.RadarCol[0], props.RadarCol[1], props.RadarCol[2]));
			graphics.FillRectangle(brush, new Rectangle(0, 0, 49, 49));
			graphics.Dispose();
		}
		l.Image = image2;
		if (props != null)
		{
			Graphics graphics2 = Graphics.FromImage(image);
			Pen pen = new Pen(Brushes.Pink);
			int num;
			int num2;
			int num3;
			int num4;
			if (texture.IsEC)
			{
				num = props.ImageOffsetEC[0];
				num2 = props.ImageOffsetEC[1];
				num3 = props.ImageOffsetEC[2];
				num4 = props.ImageOffsetEC[3];
			}
			else
			{
				num = props.ImageOffset2D[0];
				num2 = props.ImageOffset2D[1];
				num3 = props.ImageOffset2D[2];
				num4 = props.ImageOffset2D[3];
			}
			graphics2.DrawRectangle(pen, new Rectangle(num, num2, num3, num4));
			graphics2.Dispose();
		}
		c.Image = image;
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
		c = new PictureBox();
		d = new TreeView();
		e = new TextBox();
		f = new TextBox();
		g = new Label();
		h = new Label();
		i = new Label();
		j = new RichTextBox();
		k = new RichTextBox();
		l = new PictureBox();
		m = new CheckBox();
		n = new CheckBox();
		((ISupportInitialize)c).BeginInit();
		((ISupportInitialize)l).BeginInit();
		SuspendLayout();
		c.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		c.BorderStyle = BorderStyle.FixedSingle;
		c.Location = new Point(218, 3);
		c.Name = "pbox_display";
		c.Size = new Size(362, 355);
		c.SizeMode = PictureBoxSizeMode.CenterImage;
		c.TabIndex = 0;
		c.TabStop = false;
		d.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		d.Location = new Point(3, 3);
		d.Name = "tree_texture";
		d.Size = new Size(209, 436);
		d.TabIndex = 1;
		d.AfterSelect += a;
		e.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		e.Location = new Point(245, 386);
		e.Name = "txt_width";
		e.ReadOnly = true;
		e.Size = new Size(100, 20);
		e.TabIndex = 2;
		f.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		f.Location = new Point(245, 412);
		f.Name = "txt_height";
		f.ReadOnly = true;
		f.Size = new Size(100, 20);
		f.TabIndex = 3;
		g.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		g.AutoSize = true;
		g.Location = new Point(218, 389);
		g.Name = "label1";
		g.Size = new Size(21, 13);
		g.TabIndex = 4;
		g.Text = "W:";
		h.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		h.AutoSize = true;
		h.Location = new Point(218, 415);
		h.Name = "label2";
		h.Size = new Size(18, 13);
		h.TabIndex = 5;
		h.Text = "H:";
		i.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		i.AutoSize = true;
		i.Location = new Point(229, 336);
		i.Name = "txt_ID";
		i.Size = new Size(41, 13);
		i.TabIndex = 20;
		i.Text = "label10";
		j.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right;
		j.BorderStyle = BorderStyle.FixedSingle;
		j.Location = new Point(586, 3);
		j.Name = "txt_display";
		j.ReadOnly = true;
		j.Size = new Size(250, 377);
		j.TabIndex = 25;
		j.Text = "";
		j.WordWrap = false;
		k.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		k.BorderStyle = BorderStyle.FixedSingle;
		k.Location = new Point(351, 386);
		k.Name = "txt_flags";
		k.ReadOnly = true;
		k.Size = new Size(485, 46);
		k.TabIndex = 26;
		k.Text = "";
		k.WordWrap = false;
		l.Anchor = AnchorStyles.Top | AnchorStyles.Right;
		l.BorderStyle = BorderStyle.FixedSingle;
		l.Location = new Point(515, 12);
		l.Name = "pBox_RadarCol";
		l.Size = new Size(50, 50);
		l.TabIndex = 27;
		l.TabStop = false;
		m.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		m.AutoSize = true;
		m.Checked = true;
		m.CheckState = CheckState.Checked;
		m.Location = new Point(221, 363);
		m.Name = "chk_notileart";
		m.Size = new Size(71, 17);
		m.TabIndex = 28;
		m.Text = "No tileart.";
		m.UseVisualStyleBackColor = true;
		n.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		n.AutoSize = true;
		n.Checked = true;
		n.CheckState = CheckState.Checked;
		n.Location = new Point(298, 363);
		n.Name = "chk_sort";
		n.Size = new Size(90, 17);
		n.TabIndex = 29;
		n.Text = "Sort (EC only)";
		n.UseVisualStyleBackColor = true;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(n);
		base.Controls.Add(m);
		base.Controls.Add(l);
		base.Controls.Add(k);
		base.Controls.Add(j);
		base.Controls.Add(i);
		base.Controls.Add(h);
		base.Controls.Add(g);
		base.Controls.Add(f);
		base.Controls.Add(e);
		base.Controls.Add(d);
		base.Controls.Add(c);
		base.Name = "TextureControl";
		base.Size = new Size(839, 442);
		((ISupportInitialize)c).EndInit();
		((ISupportInitialize)l).EndInit();
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
