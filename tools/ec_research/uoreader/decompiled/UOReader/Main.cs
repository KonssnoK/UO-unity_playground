using System;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Text;
using System.Threading;
using System.Windows.Forms;
using Mythic.Package;
using UOReader.Core;
using UOReader.EffectDefinition;
using UOReader.Facets;
using UOReader.Hues;
using UOReader.LocalizedString;

namespace UOReader;

public class Main : Form
{
	private static Text m_a;

	private IContainer m_b;

	private TabControl m_c;

	private TabPage m_d;

	private TabPage m_e;

	private MultiControl m_f;

	private TextureControl m_g;

	private TabPage m_h;

	private TextureControl i;

	private TabPage j;

	private TabPage k;

	private StringDictionary l;

	private ProgressBar m;

	private AnimationFrames n;

	private TabPage o;

	private TerrainDefinition p;

	private TabPage q;

	private LocalizedStrings r;

	private TabPage s;

	private EffectDefinitionCollection t;

	private Button u;

	private MenuStrip v;

	private ToolStripMenuItem w;

	private ToolStripMenuItem x;

	private FolderBrowserDialog y;

	private ToolStripMenuItem z;

	private TabPage aa;

	private Button ab;

	private TileartControlNew ac;

	private TabPage ad;

	private HuesControl ae;

	private TabPage af;

	private FacetsControl ag;

	public Main()
	{
		SplashScreen splashScreen = new SplashScreen();
		new ManualResetEvent(initialState: false);
		splashScreen.ShowDialog();
		a();
		i.SetTexture(FilePointers.ECtexture);
		this.m_g.SetTexture(FilePointers.MLtexture);
		this.m_f.Dock = DockStyle.Fill;
		this.m_g.Dock = DockStyle.Fill;
		i.Dock = DockStyle.Fill;
		l.Dock = DockStyle.Fill;
		n.Dock = DockStyle.Fill;
		p.Dock = DockStyle.Fill;
		r.Dock = DockStyle.Fill;
		t.Dock = DockStyle.Fill;
		ac.Dock = DockStyle.Fill;
		ae.Dock = DockStyle.Fill;
		ag.Dock = DockStyle.Fill;
		m.Maximum = 100;
		m.Minimum = 0;
		m.Value = 0;
		n.b();
	}

	private void h(object A_0, EventArgs A_1)
	{
		Main.m_a.Show();
	}

	private void g(object A_0, EventArgs A_1)
	{
	}

	private void f(object A_0, EventArgs A_1)
	{
		Text = Application.ProductName + " " + Application.ProductVersion + " - Kons 2011-2013 - Public build";
	}

	private void e(object A_0, EventArgs A_1)
	{
	}

	private void d(object A_0, EventArgs A_1)
	{
		u.Enabled = false;
		u.Enabled = true;
	}

	private void c(object A_0, EventArgs A_1)
	{
		Utils.ChangeInstallationFolder();
	}

	private void b(object A_0, EventArgs A_1)
	{
		if (File.Exists("settings.bin"))
		{
			File.Delete("settings.bin");
		}
	}

	private void a(object A_0, EventArgs A_1)
	{
		ab.Enabled = false;
		StringDictionary dictionary = StringDictionary.GetDictionary();
		StringBuilder stringBuilder = new StringBuilder();
		int num = 0;
		string[] array = new string[9] { "data/effects/", "data/gamedata/", "data/", "data/shaders/", "data/systemtextures/", "art/textures/effects/", "data/audio/Music/", "data/audio/Sounds/", "data/audio/" };
		for (int i = 0; i < array.Length; i++)
		{
			for (int j = 0; j < dictionary.Count; j++)
			{
				string text = dictionary.GetStringAtPosition(j);
				string text2 = "\\";
				int num2 = text.LastIndexOf(text2) + text2.Length;
				if (num2 != -1)
				{
					text = text.Substring(num2);
				}
				string text3 = array[i] + text;
				ulong hash = HashDictionary.HashFileName(text3);
				if (HashDictionary.Contains(hash))
				{
					string text4 = HashDictionary.Get(hash, add: false);
					if (text4 != text3)
					{
						stringBuilder.AppendLine("Setting <" + text4 + "> as <" + text3 + ">");
						num++;
						HashDictionary.Set(hash, text3);
					}
				}
			}
		}
		using (FileStream stream = new FileStream("newhashes.txt", FileMode.Create))
		{
			using StreamWriter streamWriter = new StreamWriter(stream);
			streamWriter.WriteLine("Lines modified: ", num);
			streamWriter.WriteLine(stringBuilder.ToString());
		}
		ab.Enabled = true;
		HashDictionary.SaveDictionary("Dictionary.dic");
		MessageBox.Show("Added " + num + " names.");
	}

	protected override void Dispose(bool disposing)
	{
		if (disposing && this.m_b != null)
		{
			this.m_b.Dispose();
		}
		base.Dispose(disposing);
	}

	private void a()
	{
		this.m_c = new TabControl();
		this.m_d = new TabPage();
		this.m_e = new TabPage();
		this.m_h = new TabPage();
		j = new TabPage();
		k = new TabPage();
		o = new TabPage();
		q = new TabPage();
		s = new TabPage();
		aa = new TabPage();
		ad = new TabPage();
		m = new ProgressBar();
		u = new Button();
		v = new MenuStrip();
		w = new ToolStripMenuItem();
		x = new ToolStripMenuItem();
		z = new ToolStripMenuItem();
		y = new FolderBrowserDialog();
		ab = new Button();
		af = new TabPage();
		this.m_f = new MultiControl();
		this.m_g = new TextureControl();
		i = new TextureControl();
		n = new AnimationFrames();
		l = new StringDictionary();
		p = new TerrainDefinition();
		r = new LocalizedStrings();
		t = new EffectDefinitionCollection();
		ac = new TileartControlNew();
		ae = new HuesControl();
		ag = new FacetsControl();
		this.m_c.SuspendLayout();
		this.m_d.SuspendLayout();
		this.m_e.SuspendLayout();
		this.m_h.SuspendLayout();
		j.SuspendLayout();
		k.SuspendLayout();
		o.SuspendLayout();
		q.SuspendLayout();
		s.SuspendLayout();
		aa.SuspendLayout();
		ad.SuspendLayout();
		v.SuspendLayout();
		af.SuspendLayout();
		SuspendLayout();
		this.m_c.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
		this.m_c.Controls.Add(this.m_d);
		this.m_c.Controls.Add(this.m_e);
		this.m_c.Controls.Add(this.m_h);
		this.m_c.Controls.Add(j);
		this.m_c.Controls.Add(k);
		this.m_c.Controls.Add(o);
		this.m_c.Controls.Add(q);
		this.m_c.Controls.Add(s);
		this.m_c.Controls.Add(aa);
		this.m_c.Controls.Add(ad);
		this.m_c.Controls.Add(af);
		this.m_c.Location = new Point(0, 41);
		this.m_c.Name = "tab_texture";
		this.m_c.SelectedIndex = 0;
		this.m_c.Size = new Size(779, 493);
		this.m_c.TabIndex = 6;
		this.m_d.BackColor = SystemColors.Control;
		this.m_d.Controls.Add(this.m_f);
		this.m_d.Location = new Point(4, 22);
		this.m_d.Name = "tab_Multi";
		this.m_d.Padding = new Padding(3);
		this.m_d.Size = new Size(771, 467);
		this.m_d.TabIndex = 0;
		this.m_d.Text = "Multi";
		this.m_e.BackColor = SystemColors.Control;
		this.m_e.Controls.Add(this.m_g);
		this.m_e.Location = new Point(4, 22);
		this.m_e.Name = "tabPage2";
		this.m_e.Padding = new Padding(3);
		this.m_e.Size = new Size(771, 467);
		this.m_e.TabIndex = 1;
		this.m_e.Text = "Texture Legacy";
		this.m_h.BackColor = SystemColors.Control;
		this.m_h.Controls.Add(i);
		this.m_h.Location = new Point(4, 22);
		this.m_h.Name = "tab_ectexture";
		this.m_h.Padding = new Padding(3);
		this.m_h.Size = new Size(771, 467);
		this.m_h.TabIndex = 2;
		this.m_h.Text = "Texture EC";
		j.BackColor = SystemColors.Control;
		j.Controls.Add(n);
		j.Location = new Point(4, 22);
		j.Name = "tabPage1";
		j.Padding = new Padding(3);
		j.Size = new Size(771, 467);
		j.TabIndex = 3;
		j.Text = "Animation Frame";
		k.BackColor = SystemColors.Control;
		k.Controls.Add(l);
		k.Location = new Point(4, 22);
		k.Name = "tabPage3";
		k.Padding = new Padding(3);
		k.Size = new Size(771, 467);
		k.TabIndex = 4;
		k.Text = "String Dictionary";
		o.BackColor = SystemColors.Control;
		o.Controls.Add(p);
		o.Location = new Point(4, 22);
		o.Name = "TerrainTab";
		o.Padding = new Padding(3);
		o.Size = new Size(771, 467);
		o.TabIndex = 5;
		o.Text = "TerrainDefinition";
		q.BackColor = SystemColors.Control;
		q.Controls.Add(r);
		q.Location = new Point(4, 22);
		q.Name = "tab_localizedString";
		q.Padding = new Padding(3);
		q.Size = new Size(771, 467);
		q.TabIndex = 6;
		q.Text = "LocalizedString";
		s.BackColor = SystemColors.Control;
		s.Controls.Add(t);
		s.Location = new Point(4, 22);
		s.Name = "tabPage4";
		s.Padding = new Padding(3);
		s.Size = new Size(771, 467);
		s.TabIndex = 7;
		s.Text = "EffectDefinitionCollection";
		aa.BackColor = SystemColors.Control;
		aa.Controls.Add(ac);
		aa.Location = new Point(4, 22);
		aa.Name = "tab_tileart";
		aa.Padding = new Padding(3);
		aa.Size = new Size(771, 467);
		aa.TabIndex = 8;
		aa.Text = "Tileart";
		ad.BackColor = SystemColors.Control;
		ad.Controls.Add(ae);
		ad.Location = new Point(4, 22);
		ad.Name = "tabPage5";
		ad.Padding = new Padding(3);
		ad.Size = new Size(771, 467);
		ad.TabIndex = 9;
		ad.Text = "Hues";
		m.Anchor = AnchorStyles.Top | AnchorStyles.Right;
		m.Location = new Point(531, 12);
		m.Name = "pBar";
		m.Size = new Size(244, 10);
		m.Style = ProgressBarStyle.Continuous;
		m.TabIndex = 11;
		u.Location = new Point(422, 1);
		u.Name = "btn_stats";
		u.Size = new Size(75, 23);
		u.TabIndex = 12;
		u.Text = "TileArtStats";
		u.UseVisualStyleBackColor = true;
		u.Click += d;
		v.Items.AddRange(new ToolStripItem[1] { w });
		v.Location = new Point(0, 0);
		v.Name = "menuStrip1";
		v.Size = new Size(779, 24);
		v.TabIndex = 13;
		v.Text = "menuStrip1";
		w.DropDownItems.AddRange(new ToolStripItem[2] { x, z });
		w.Name = "settingsToolStripMenuItem";
		w.Size = new Size(67, 20);
		w.Text = "Settings..";
		x.Name = "changeUOFolderToolStripMenuItem";
		x.Size = new Size(171, 22);
		x.Text = "Change UO Folder";
		x.Click += c;
		z.Name = "clearSettingsToolStripMenuItem";
		z.Size = new Size(171, 22);
		z.Text = "Clear settings..";
		z.Click += b;
		ab.Location = new Point(218, 1);
		ab.Name = "btn_upddic";
		ab.Size = new Size(136, 23);
		ab.TabIndex = 14;
		ab.Text = "Update dictionary";
		ab.UseVisualStyleBackColor = true;
		ab.Click += a;
		af.BackColor = SystemColors.Control;
		af.Controls.Add(ag);
		af.Location = new Point(4, 22);
		af.Name = "tab_facet";
		af.Padding = new Padding(3);
		af.Size = new Size(771, 467);
		af.TabIndex = 10;
		af.Text = "Facet";
		this.m_f.Location = new Point(73, 23);
		this.m_f.Name = "multi";
		this.m_f.Size = new Size(589, 284);
		this.m_f.TabIndex = 0;
		this.m_g.Location = new Point(49, 24);
		this.m_g.Name = "C_texture";
		this.m_g.Size = new Size(564, 328);
		this.m_g.TabIndex = 0;
		i.Location = new Point(89, 50);
		i.Name = "C_textureEC";
		i.Size = new Size(569, 329);
		i.TabIndex = 0;
		n.Location = new Point(33, 6);
		n.Name = "C_AnimationFrame";
		n.Size = new Size(422, 268);
		n.TabIndex = 0;
		l.Location = new Point(6, 6);
		l.Name = "C_StringDictonary";
		l.Size = new Size(347, 217);
		l.TabIndex = 0;
		p.Location = new Point(23, 68);
		p.Name = "C_TerrainDefinition";
		p.Size = new Size(636, 150);
		p.TabIndex = 0;
		r.Location = new Point(22, 23);
		r.Name = "C_LocalizedStrings";
		r.Size = new Size(395, 264);
		r.TabIndex = 0;
		t.Location = new Point(45, 28);
		t.Name = "C_EffectDefinitionCollection";
		t.Size = new Size(516, 341);
		t.TabIndex = 0;
		ac.Location = new Point(6, 17);
		ac.Name = "C_TileartControlNew";
		ac.Size = new Size(1117, 557);
		ac.TabIndex = 0;
		ae.Location = new Point(90, 20);
		ae.Name = "C_huesControl";
		ae.Size = new Size(422, 360);
		ae.TabIndex = 0;
		ag.Location = new Point(143, 20);
		ag.Name = "C_facetsControl";
		ag.Size = new Size(427, 255);
		ag.TabIndex = 0;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		base.ClientSize = new Size(779, 534);
		base.Controls.Add(ab);
		base.Controls.Add(u);
		base.Controls.Add(m);
		base.Controls.Add(this.m_c);
		base.Controls.Add(v);
		base.MainMenuStrip = v;
		base.Name = "Main";
		Text = "UO Reader 0.42 - Kons - 2011";
		base.Load += f;
		this.m_c.ResumeLayout(performLayout: false);
		this.m_d.ResumeLayout(performLayout: false);
		this.m_e.ResumeLayout(performLayout: false);
		this.m_h.ResumeLayout(performLayout: false);
		j.ResumeLayout(performLayout: false);
		k.ResumeLayout(performLayout: false);
		o.ResumeLayout(performLayout: false);
		q.ResumeLayout(performLayout: false);
		s.ResumeLayout(performLayout: false);
		aa.ResumeLayout(performLayout: false);
		ad.ResumeLayout(performLayout: false);
		v.ResumeLayout(performLayout: false);
		v.PerformLayout();
		af.ResumeLayout(performLayout: false);
		ResumeLayout(performLayout: false);
		PerformLayout();
	}

	static Main()
	{
		Main.m_a = new Text();
	}
}
