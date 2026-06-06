using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;
using UOReader.Core;
using UOReader.Core.Format;

namespace UOReader;

public class StringDictionary : UserControl
{
	private static StringDictionary m_a;

	private stringDictionaryData m_b;

	public uint Count;

	private bool c;

	private IContainer d;

	private TextBox e;

	private TextBox f;

	private Label g;

	private TextBox h;

	private Label i;

	private ListBox j;

	private TextBox k;

	private Label l;

	private CheckBox m;

	private Button n;

	public StringDictionary()
	{
		a();
		b();
		StringDictionary.m_a = this;
	}

	public static StringDictionary GetDictionary()
	{
		if (StringDictionary.m_a != null)
		{
			return StringDictionary.m_a;
		}
		return null;
	}

	private void b()
	{
		this.m_b = FilePointers.stringDictionary;
		if (this.m_b != null)
		{
			e.Text = this.m_b.unk64.ToString();
			f.Text = this.m_b.StringCount.ToString();
			h.Text = this.m_b.unk16.ToString();
			j.Items.AddRange(this.m_b.stringList.ToArray());
			Count = this.m_b.StringCount;
		}
	}

	public string GetStringAtPosition(uint n)
	{
		return GetStringAtPosition((int)n);
	}

	public string GetStringAtPosition(int n)
	{
		if (j.Items.Count == 0)
		{
			b();
		}
		if (n >= j.Items.Count)
		{
			return j.Items[0].ToString();
		}
		return j.Items[n].ToString();
	}

	private void b(object A_0, EventArgs A_1)
	{
	}

	private bool a(string A_0)
	{
		if (m.Checked)
		{
			if (A_0.Contains(k.Text))
			{
				return true;
			}
		}
		else if (A_0.IndexOf(k.Text, StringComparison.OrdinalIgnoreCase) >= 0)
		{
			return true;
		}
		return false;
	}

	private void a(object A_0, EventArgs A_1)
	{
		if (k.Text.Length <= 1)
		{
			if (c)
			{
				j.Items.Clear();
				j.Items.AddRange(this.m_b.stringList.ToArray());
				c = false;
			}
		}
		else
		{
			c = true;
			List<string> list = this.m_b.stringList.FindAll(a);
			j.Items.Clear();
			j.Items.AddRange(list.ToArray());
		}
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
		e = new TextBox();
		f = new TextBox();
		g = new Label();
		h = new TextBox();
		i = new Label();
		j = new ListBox();
		k = new TextBox();
		l = new Label();
		m = new CheckBox();
		n = new Button();
		SuspendLayout();
		e.Location = new Point(3, 3);
		e.Name = "txt_unk";
		e.Size = new Size(100, 20);
		e.TabIndex = 1;
		f.Location = new Point(3, 42);
		f.Name = "txt_count";
		f.Size = new Size(100, 20);
		f.TabIndex = 2;
		g.AutoSize = true;
		g.Location = new Point(3, 26);
		g.Name = "label1";
		g.Size = new Size(38, 13);
		g.TabIndex = 3;
		g.Text = "Count:";
		h.Location = new Point(3, 81);
		h.Name = "txt_unk2";
		h.Size = new Size(100, 20);
		h.TabIndex = 4;
		i.AutoSize = true;
		i.Location = new Point(3, 65);
		i.Name = "label2";
		i.Size = new Size(27, 13);
		i.TabIndex = 5;
		i.Text = "Unk";
		j.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		j.BorderStyle = BorderStyle.FixedSingle;
		j.FormattingEnabled = true;
		j.Location = new Point(106, 3);
		j.Name = "listBox_display";
		j.Size = new Size(238, 210);
		j.TabIndex = 0;
		k.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		k.Location = new Point(3, 193);
		k.Name = "txt_search";
		k.Size = new Size(100, 20);
		k.TabIndex = 6;
		k.TextChanged += b;
		l.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		l.AutoSize = true;
		l.Location = new Point(3, 177);
		l.Name = "label3";
		l.Size = new Size(44, 13);
		l.TabIndex = 7;
		l.Text = "Search:";
		m.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		m.AutoSize = true;
		m.Location = new Point(6, 157);
		m.Name = "chk_casesensitive";
		m.Size = new Size(96, 17);
		m.TabIndex = 8;
		m.Text = "Case Sensitive";
		m.UseVisualStyleBackColor = true;
		n.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
		n.FlatStyle = FlatStyle.Flat;
		n.Location = new Point(6, 128);
		n.Name = "btn_search";
		n.Size = new Size(94, 23);
		n.TabIndex = 9;
		n.Text = "Search";
		n.UseVisualStyleBackColor = true;
		n.Click += a;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.Controls.Add(n);
		base.Controls.Add(m);
		base.Controls.Add(l);
		base.Controls.Add(k);
		base.Controls.Add(i);
		base.Controls.Add(h);
		base.Controls.Add(g);
		base.Controls.Add(f);
		base.Controls.Add(e);
		base.Controls.Add(j);
		base.Name = "StringDictionary";
		base.Size = new Size(347, 217);
		ResumeLayout(performLayout: false);
		PerformLayout();
	}
}
