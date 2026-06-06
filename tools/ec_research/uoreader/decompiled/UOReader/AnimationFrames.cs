using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using Mythic.Package;
using UOReader.Core;

namespace UOReader;

public class AnimationFrames : UserControl
{
	private List<MythicPackage> m_a;

	private UOFrameBin m_b;

	private List<TreeNode> c = new List<TreeNode>();

	private IContainer d;

	private TreeView e;

	private RichTextBox f;

	private Label g;

	private PictureBox h;

	private Label i;

	private PictureBox j;

	private BackgroundWorker k;

	private ProgressBar l;

	public AnimationFrames()
	{
		a();
		if (FilePointers.animationFrame != null)
		{
			this.m_a = FilePointers.animationFrame.UOPs;
			e.Nodes.AddRange(FilePointers.animationFrame.UOPCollection.ToArray());
		}
	}

	internal void b()
	{
	}

	public void LoadFrameContainer(int index)
	{
		c.Clear();
		for (int i = 0; i < this.m_a[index].Blocks.Count; i++)
		{
			for (int j = 0; j < this.m_a[index].Blocks[i].Files.Count; j++)
			{
				string text = "UnknownName";
				ulong fileHash = this.m_a[index].Blocks[i].Files[j].FileHash;
				string text2 = "";
				string text3 = "UnkID";
				string[] array = new string[4];
				if (HashDictionary.Contains(fileHash))
				{
					text2 = HashDictionary.Get(fileHash, add: false);
					if (text2 == null)
					{
						Dump("Problem at block " + i + ", file " + j + ". NULL Value!");
						continue;
					}
					array = text2.Split('.');
					array = array[0].Split('/');
					text = array[2];
					text3 = array[3];
				}
				int num = -1;
				for (int k = 0; k < c.Count; k++)
				{
					if ((string)c[k].Tag == text)
					{
						num = k;
						break;
					}
				}
				int index2 = num;
				if (num == -1)
				{
					TreeNode treeNode = new TreeNode();
					treeNode.Text = text;
					treeNode.Tag = text;
					c.Add(treeNode);
					index2 = c.Count - 1;
				}
				TreeNode treeNode2 = new TreeNode();
				treeNode2.Text = text3;
				treeNode2.Tag = this.m_a[index].Blocks[i].Files[j].Unpack(this.m_a[index].FileInfo.FullName);
				c[index2].Nodes.Add(treeNode2);
			}
			this.k.ReportProgress(i + 1);
		}
	}

	public void Dump(string text)
	{
		using FileStream stream = new FileStream("AnimationFrameDump", FileMode.Append);
		using StreamWriter streamWriter = new StreamWriter(stream);
		streamWriter.WriteLine(DateTime.Now.ToString() + "\t" + text);
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		if (A_1.Node == null)
		{
			return;
		}
		A_1.Node.BackColor = Color.LightGray;
		A_1.Node.Expand();
		if (A_1.Node.Level == 0)
		{
			for (int i = 0; i < e.Nodes.Count; i++)
			{
				e.Nodes[i].Collapse();
				e.Nodes[i].Nodes.Clear();
			}
			int num = (int)A_1.Node.Tag;
			l.Minimum = 0;
			l.Maximum = this.m_a[num].Blocks.Count;
			l.Value = 0;
			e.Enabled = false;
			k.RunWorkerAsync(num);
		}
		else if (A_1.Node.Tag is FrameEntry)
		{
			a(A_1.Node.Tag as FrameEntry);
		}
		else if (A_1.Node.Tag is byte[])
		{
			this.m_b = new UOFrameBin();
			this.m_b.Load((byte[])A_1.Node.Tag);
			A_1.Node.Nodes.AddRange(this.m_b.Frames.ToArray());
			A_1.Node.Expand();
			j.Size = new Size((int)(this.m_b.ColoursCount + 100), j.Size.Height);
			j.Image = this.m_b.ColoursIMG;
			f.Text = this.m_b.FillTxtInfos();
			h.BackgroundImage = null;
		}
	}

	private void a(object A_0, TreeViewCancelEventArgs A_1)
	{
		if (e.SelectedNode == null)
		{
			return;
		}
		e.SelectedNode.BackColor = Color.Transparent;
		if (e.SelectedNode == A_1.Node)
		{
			A_1.Node.Nodes.Clear();
		}
		else if (e.SelectedNode.Parent == null && A_1.Node.Parent == null)
		{
			e.SelectedNode.Nodes.Clear();
		}
		else
		{
			if (e.SelectedNode.Tag is FrameEntry && A_1.Node.Tag is FrameEntry && A_1.Node.Parent == e.SelectedNode.Parent)
			{
				e.SelectedNode.Collapse();
				return;
			}
			if (e.SelectedNode.Tag is FrameEntry && A_1.Node.Tag is byte[] && A_1.Node != e.SelectedNode)
			{
				A_1.Node.Collapse();
				e.SelectedNode.Parent.Nodes.Clear();
			}
			else if (e.SelectedNode.Tag is byte[] && A_1.Node.Tag is byte[])
			{
				e.SelectedNode.Nodes.Clear();
			}
			else if (e.SelectedNode.Tag is byte[] && A_1.Node.Tag is FrameEntry && A_1.Node.Parent != e.SelectedNode)
			{
				e.SelectedNode.Nodes.Clear();
			}
			else if (e.SelectedNode.Tag is FrameEntry && A_1.Node.Parent != null && A_1.Node.Parent.Parent == null)
			{
				e.SelectedNode.Parent.Nodes.Clear();
			}
		}
		if (A_1.Node.Level == 1)
		{
			if (e.SelectedNode.Tag is byte[])
			{
				e.SelectedNode.Parent.Collapse();
			}
			if (e.SelectedNode.Tag is FrameEntry)
			{
				e.SelectedNode.Parent.Nodes.Clear();
				e.SelectedNode.Parent.Parent.Collapse();
			}
		}
	}

	private void a(object A_0, TreeNodeMouseClickEventArgs A_1)
	{
	}

	private void a(object A_0, DoWorkEventArgs A_1)
	{
		if (A_1.Argument is int)
		{
			LoadFrameContainer((int)A_1.Argument);
			A_1.Result = (int)A_1.Argument;
		}
	}

	private void a(object A_0, RunWorkerCompletedEventArgs A_1)
	{
		if (A_1.Result is int)
		{
			e.Nodes[(int)A_1.Result].Nodes.AddRange(c.ToArray());
			e.Nodes[(int)A_1.Result].Expand();
			e.Enabled = true;
		}
	}

	private void a(object A_0, ProgressChangedEventArgs A_1)
	{
		l.Value = A_1.ProgressPercentage;
	}

	private void a(FrameEntry A_0)
	{
		UOFrame uOFrame = new UOFrame();
		if (this.m_b == null)
		{
			MessageBox.Show("ERROR: Animation NULL");
			return;
		}
		Bitmap bitmap = uOFrame.LoadFrameImage(A_0, this.m_b.ImageData, this.m_b.ImageDataOffset, this.m_b.Colours);
		int num = this.m_b.GetWidth();
		int num2 = this.m_b.GetHeight();
		Bitmap bitmap2 = new Bitmap(num, num2);
		for (int i = 0; i < num; i++)
		{
			for (int j = 0; j < num2; j++)
			{
				bitmap2.SetPixel(i, j, Color.Black);
			}
		}
		if (h.Size.Width >= num)
		{
			_ = h.Size.Height;
		}
		for (int k = 0; k < bitmap.Width; k++)
		{
			for (int l = 0; l < bitmap.Height; l++)
			{
				int num3 = Math.Abs(this.m_b.InitCoordsX - A_0.InitCoordsX);
				int num4 = Math.Abs(this.m_b.InitCoordsY - A_0.InitCoordsY);
				bitmap2.SetPixel(num3 + k, num4 + l, bitmap.GetPixel(k, l));
			}
		}
		h.BackgroundImageLayout = ImageLayout.Center;
		Graphics graphics = Graphics.FromImage(bitmap2);
		Font font = new Font("Arial", 20f);
		SolidBrush brush = new SolidBrush(Color.FromArgb(90, 255, 255, 255));
		StringFormat format = new StringFormat();
		float num5 = ((bitmap2.Width / 2 - 30 >= 0) ? (bitmap2.Width / 2 - 30) : 0);
		float num6 = ((bitmap2.Height / 2 - 20 >= 0) ? (bitmap2.Height / 2 - 20) : 0);
		graphics.DrawString("OSI", font, brush, num5, num6, format);
		h.BackgroundImage = bitmap2;
		f.Text = this.m_b.FillTxtInfos() + "\n" + uOFrame.FillTxtInfos(A_0);
	}

	protected override void Dispose(bool disposing)
	{
		if (disposing && d != null)
		{
			d.Dispose();
		}
		base.Dispose(disposing);
	}

	private void a()
	{
		e = new TreeView();
		f = new RichTextBox();
		g = new Label();
		h = new PictureBox();
		i = new Label();
		j = new PictureBox();
		k = new BackgroundWorker();
		l = new ProgressBar();
		((ISupportInitialize)h).BeginInit();
		((ISupportInitialize)j).BeginInit();
		SuspendLayout();
		e.Dock = DockStyle.Left;
		e.Location = new Point(0, 0);
		e.Name = "tree_frames";
		e.Size = new Size(182, 325);
		e.TabIndex = 0;
		e.BeforeSelect += a;
		e.AfterSelect += a;
		e.NodeMouseClick += a;
		f.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right;
		f.BackColor = SystemColors.ControlLightLight;
		f.BorderStyle = BorderStyle.None;
		f.Location = new Point(520, 150);
		f.Name = "txt_info";
		f.ReadOnly = true;
		f.Size = new Size(189, 143);
		f.TabIndex = 12;
		f.Text = "";
		g.AutoSize = true;
		g.Location = new Point(188, 134);
		g.Name = "label2";
		g.Size = new Size(39, 13);
		g.TabIndex = 11;
		g.Text = "Frame:";
		h.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		h.BackColor = Color.AliceBlue;
		h.BackgroundImageLayout = ImageLayout.None;
		h.BorderStyle = BorderStyle.FixedSingle;
		h.Location = new Point(188, 150);
		h.MinimumSize = new Size(10, 10);
		h.Name = "pictureBox2";
		h.Size = new Size(326, 143);
		h.TabIndex = 10;
		h.TabStop = false;
		h.WaitOnLoad = true;
		i.AutoSize = true;
		i.Location = new Point(188, 7);
		i.Name = "label1";
		i.Size = new Size(75, 13);
		i.TabIndex = 9;
		i.Text = "Colours Table:";
		j.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
		j.BackColor = SystemColors.HighlightText;
		j.BackgroundImageLayout = ImageLayout.None;
		j.BorderStyle = BorderStyle.FixedSingle;
		j.Location = new Point(188, 23);
		j.Name = "pictureBox1";
		j.Size = new Size(521, 101);
		j.TabIndex = 8;
		j.TabStop = false;
		k.WorkerReportsProgress = true;
		k.DoWork += a;
		k.ProgressChanged += a;
		k.RunWorkerCompleted += a;
		l.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		l.Location = new Point(188, 311);
		l.Name = "progressBar1";
		l.Size = new Size(521, 11);
		l.TabIndex = 13;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(l);
		base.Controls.Add(f);
		base.Controls.Add(g);
		base.Controls.Add(h);
		base.Controls.Add(i);
		base.Controls.Add(j);
		base.Controls.Add(e);
		base.Name = "AnimationFrames";
		base.Size = new Size(721, 325);
		((ISupportInitialize)h).EndInit();
		((ISupportInitialize)j).EndInit();
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
