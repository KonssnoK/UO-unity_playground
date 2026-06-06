using System;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace UOReader;

public class Text : Form
{
	private IContainer m_a;

	private RichTextBox b;

	private Button c;

	public Text()
	{
		a();
	}

	public void print(string text)
	{
		b.AppendText(text);
	}

	public void clear()
	{
		b.Clear();
	}

	private void a(object A_0, EventArgs A_1)
	{
		Hide();
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
		c = new Button();
		SuspendLayout();
		b.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		b.Location = new Point(2, 29);
		b.Name = "richTextBox1";
		b.ScrollBars = RichTextBoxScrollBars.ForcedBoth;
		b.Size = new Size(813, 206);
		b.TabIndex = 0;
		b.Text = "";
		b.WordWrap = false;
		c.Anchor = AnchorStyles.Top | AnchorStyles.Right;
		c.Location = new Point(787, 0);
		c.Name = "btn_close";
		c.Size = new Size(28, 23);
		c.TabIndex = 1;
		c.Text = "X";
		c.UseVisualStyleBackColor = true;
		c.Click += a;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.ClientSize = new Size(815, 235);
		base.ControlBox = false;
		base.Controls.Add(c);
		base.Controls.Add(b);
		base.FormBorderStyle = FormBorderStyle.SizableToolWindow;
		base.Name = "Text";
		base.ShowIcon = false;
		Text = "Text";
		ResumeLayout(performLayout: false);
	}
}
