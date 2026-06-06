using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using Mythic.Package;
using UOReader.Core;
using UOReader.Multi;

namespace UOReader;

public class MultiControl : UserControl
{
	private MultiItem m_a;

	private Text m_b;

	private Textures m_c;

	private Textures m_d;

	private MythicPackage e;

	private bool f = true;

	private IContainer g;

	private TrackBar h;

	private PictureBox i;

	private TreeView j;

	private CheckBox k;

	private RichTextBox l;

	private BackgroundWorker m;

	private ProgressBar n;

	private SplitContainer o;

	public Text Display => this.m_b;

	public MultiControl()
	{
		Text display = new Text();
		this.m_a = new MultiItem(display);
		a();
		m.RunWorkerCompleted += a;
		m.ProgressChanged += a;
		if (FilePointers.multiCollection != null)
		{
			j.Nodes.AddRange(FilePointers.multiCollection.MultisNodes.ToArray());
		}
		if (FilePointers.MLtexture != null)
		{
			this.m_c = FilePointers.MLtexture.texture;
		}
		if (FilePointers.ECtexture != null)
		{
			this.m_d = FilePointers.ECtexture.texture;
		}
	}

	public void SetDisplay(Text in_display)
	{
		this.m_b = in_display;
	}

	private void a(object A_0, EventArgs A_1)
	{
		if (!f)
		{
			h.Enabled = false;
			WorkerParams workerParams = new WorkerParams();
			workerParams.command = "changeZ";
			workerParams.maxHeight = h.Value;
			d();
			m.RunWorkerAsync(workerParams);
		}
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		j.Enabled = false;
		h.Enabled = false;
		WorkerParams workerParams = new WorkerParams();
		workerParams.command = "load";
		workerParams.rawData = (byte[])A_1.Node.Tag;
		workerParams.maxHeight = h.Value;
		d();
		f = true;
		m.RunWorkerAsync(workerParams);
	}

	private void d()
	{
		n.Minimum = 0;
		n.Maximum = 4;
		n.Value = 0;
	}

	private void c()
	{
		n.Value = n.Maximum;
	}

	private void b()
	{
		h.Maximum = this.m_a.MaxZ + 1;
		h.Minimum = 0;
		h.Value = h.Maximum;
		h.Enabled = h.Maximum - h.Minimum > 1;
	}

	private void a(object A_0, DoWorkEventArgs A_1)
	{
		WorkerParams workerParams = A_1.Argument as WorkerParams;
		if (workerParams.command == "load")
		{
			this.m_a.a();
			m.ReportProgress(1);
			this.m_a.Load(workerParams.rawData);
			m.ReportProgress(2);
			this.m_a.Order();
			m.ReportProgress(3);
			workerParams.maxHeight = this.m_a.MaxZ + 1;
		}
		WorkerResult workerResult = ((!k.Checked) ? this.m_a.GetFinalBitmap2(workerParams.maxHeight, usingEC: false) : this.m_a.GetFinalBitmap2(workerParams.maxHeight, usingEC: true));
		workerResult.command = workerParams.command;
		A_1.Result = workerResult;
	}

	private void a(object A_0, ProgressChangedEventArgs A_1)
	{
		n.Value = A_1.ProgressPercentage;
	}

	private void a(object A_0, RunWorkerCompletedEventArgs A_1)
	{
		c();
		WorkerResult workerResult = A_1.Result as WorkerResult;
		i.Image = workerResult.image;
		l.Text = workerResult.description;
		h.Enabled = true;
		j.Enabled = true;
		if (workerResult.command != "changeZ")
		{
			b();
			f = false;
		}
	}

	protected override void Dispose(bool disposing)
	{
		if (disposing && g != null)
		{
			g.Dispose();
		}
		base.Dispose(disposing);
	}

	private void a()
	{
		h = new TrackBar();
		i = new PictureBox();
		j = new TreeView();
		k = new CheckBox();
		l = new RichTextBox();
		m = new BackgroundWorker();
		n = new ProgressBar();
		o = new SplitContainer();
		((ISupportInitialize)h).BeginInit();
		((ISupportInitialize)i).BeginInit();
		((ISupportInitialize)o).BeginInit();
		o.Panel1.SuspendLayout();
		o.Panel2.SuspendLayout();
		o.SuspendLayout();
		SuspendLayout();
		h.Anchor = AnchorStyles.Top | AnchorStyles.Right;
		h.LargeChange = 1;
		h.Location = new Point(593, 3);
		h.Name = "trackZ";
		h.Size = new Size(233, 45);
		h.TabIndex = 9;
		h.Value = 10;
		h.ValueChanged += a;
		i.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		i.BorderStyle = BorderStyle.FixedSingle;
		i.Location = new Point(3, 3);
		i.Name = "pictureBox1";
		i.Size = new Size(370, 448);
		i.SizeMode = PictureBoxSizeMode.Zoom;
		i.TabIndex = 5;
		i.TabStop = false;
		j.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Right;
		j.Location = new Point(379, 3);
		j.Name = "tree_multi";
		j.Size = new Size(205, 448);
		j.TabIndex = 10;
		j.AfterSelect += a;
		k.AutoSize = true;
		k.Location = new Point(3, 9);
		k.Name = "chk_UseECtexture";
		k.Size = new Size(62, 17);
		k.TabIndex = 11;
		k.Text = "Use EC";
		k.UseVisualStyleBackColor = true;
		l.BorderStyle = BorderStyle.FixedSingle;
		l.Dock = DockStyle.Fill;
		l.Location = new Point(0, 0);
		l.Name = "txt_Multi_display";
		l.ReadOnly = true;
		l.Size = new Size(246, 454);
		l.TabIndex = 12;
		l.Text = "";
		l.WordWrap = false;
		m.WorkerReportsProgress = true;
		m.DoWork += a;
		n.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
		n.Location = new Point(137, 16);
		n.Name = "pbar_multi";
		n.Size = new Size(440, 10);
		n.TabIndex = 13;
		o.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		o.Location = new Point(0, 32);
		o.Name = "splitContainer1";
		o.Panel1.Controls.Add(l);
		o.Panel2.Controls.Add(i);
		o.Panel2.Controls.Add(j);
		o.Size = new Size(837, 454);
		o.SplitterDistance = 246;
		o.TabIndex = 14;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(o);
		base.Controls.Add(n);
		base.Controls.Add(k);
		base.Controls.Add(h);
		base.Name = "MultiControl";
		base.Size = new Size(837, 486);
		((ISupportInitialize)h).EndInit();
		((ISupportInitialize)i).EndInit();
		o.Panel1.ResumeLayout(performLayout: false);
		o.Panel2.ResumeLayout(performLayout: false);
		((ISupportInitialize)o).EndInit();
		o.ResumeLayout(performLayout: false);
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
