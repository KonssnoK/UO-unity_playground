using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Text;
using System.Windows.Forms;
using UOReader.Core;

namespace UOReader.LocalizedString;

public class LocalizedStrings : UserControl
{
	private BackgroundWorker m_a = new BackgroundWorker();

	private IContainer b;

	private TreeView c;

	private TextBox d;

	private Label e;

	private DataGridView f;

	private DataGridViewTextBoxColumn g;

	private DataGridViewTextBoxColumn h;

	private DataGridViewTextBoxColumn i;

	private TextBox j;

	private ProgressBar k;

	public LocalizedStrings()
	{
		this.m_a.WorkerReportsProgress = true;
		this.m_a.DoWork += a;
		this.m_a.RunWorkerCompleted += a;
		this.m_a.ProgressChanged += a;
		a();
		if (FilePointers.localizedString != null)
		{
			c.Nodes.AddRange(FilePointers.localizedString.ClilocsNodes.ToArray());
			d.Text = FilePointers.localizedString.FileCount.ToString();
		}
	}

	private void a(object A_0, ProgressChangedEventArgs A_1)
	{
		k.Value = A_1.ProgressPercentage;
	}

	private void a(object A_0, DoWorkEventArgs A_1)
	{
		byte[] buffer = A_1.Argument as byte[];
		int index = f.Columns["col_ID"].Index;
		int index2 = f.Columns["col_unk"].Index;
		int index3 = f.Columns["col_string"].Index;
		List<DataGridViewRow> list = new List<DataGridViewRow>();
		using MemoryStream input = new MemoryStream(buffer);
		using BinaryReader binaryReader = new BinaryReader(input);
		binaryReader.ReadUInt16();
		binaryReader.ReadUInt32();
		while (binaryReader.BaseStream.Position < binaryReader.BaseStream.Length)
		{
			uint num = binaryReader.ReadUInt32();
			uint num2 = binaryReader.ReadByte();
			ushort count = binaryReader.ReadUInt16();
			byte[] bytes = binaryReader.ReadBytes(count);
			string value = Encoding.ASCII.GetString(bytes);
			DataGridViewRow dataGridViewRow = new DataGridViewRow();
			dataGridViewRow.CreateCells(f);
			dataGridViewRow.Cells[index].Value = num.ToString();
			dataGridViewRow.Cells[index2].Value = num2.ToString();
			dataGridViewRow.Cells[index3].Value = value;
			list.Add(dataGridViewRow);
			this.m_a.ReportProgress((int)(binaryReader.BaseStream.Position * 100 / binaryReader.BaseStream.Length));
		}
		A_1.Result = list;
	}

	private void a(object A_0, RunWorkerCompletedEventArgs A_1)
	{
		f.Rows.AddRange((A_1.Result as List<DataGridViewRow>).ToArray());
		j.Text = (A_1.Result as List<DataGridViewRow>).Count.ToString();
	}

	private void a(object A_0, TreeViewEventArgs A_1)
	{
		byte[] argument = (byte[])A_1.Node.Tag;
		f.Rows.Clear();
		this.m_a.RunWorkerAsync(argument);
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
		c = new TreeView();
		d = new TextBox();
		e = new Label();
		f = new DataGridView();
		g = new DataGridViewTextBoxColumn();
		h = new DataGridViewTextBoxColumn();
		i = new DataGridViewTextBoxColumn();
		j = new TextBox();
		k = new ProgressBar();
		((ISupportInitialize)f).BeginInit();
		SuspendLayout();
		c.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left;
		c.Location = new Point(6, 29);
		c.Name = "tree_cliloc";
		c.Size = new Size(115, 225);
		c.TabIndex = 1;
		c.AfterSelect += a;
		d.Location = new Point(44, 3);
		d.Name = "txt_count";
		d.Size = new Size(77, 20);
		d.TabIndex = 2;
		e.AutoSize = true;
		e.Location = new Point(3, 6);
		e.Name = "label1";
		e.Size = new Size(35, 13);
		e.TabIndex = 3;
		e.Text = "Count";
		f.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		f.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
		f.Columns.AddRange(g, h, i);
		f.Location = new Point(127, 29);
		f.Name = "data_display";
		f.Size = new Size(256, 225);
		f.TabIndex = 4;
		g.AutoSizeMode = DataGridViewAutoSizeColumnMode.None;
		g.HeaderText = "ID";
		g.Name = "col_id";
		g.ReadOnly = true;
		g.Resizable = DataGridViewTriState.False;
		g.Width = 150;
		h.AutoSizeMode = DataGridViewAutoSizeColumnMode.None;
		h.HeaderText = "unk";
		h.Name = "col_unk";
		h.ReadOnly = true;
		h.Width = 30;
		i.AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill;
		i.HeaderText = "String value";
		i.Name = "col_string";
		i.ReadOnly = true;
		i.Resizable = DataGridViewTriState.False;
		j.Anchor = AnchorStyles.Top | AnchorStyles.Right;
		j.Location = new Point(299, 3);
		j.Name = "txt_subcount";
		j.Size = new Size(84, 20);
		j.TabIndex = 5;
		k.Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right;
		k.Location = new Point(127, 6);
		k.Name = "pBar";
		k.Size = new Size(166, 13);
		k.TabIndex = 6;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(k);
		base.Controls.Add(j);
		base.Controls.Add(f);
		base.Controls.Add(e);
		base.Controls.Add(d);
		base.Controls.Add(c);
		base.Name = "LocalizedStrings";
		base.Size = new Size(395, 264);
		((ISupportInitialize)f).EndInit();
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
