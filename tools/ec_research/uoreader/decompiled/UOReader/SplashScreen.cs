using System;
using System.ComponentModel;
using System.Drawing;
using System.IO;
using System.Threading;
using System.Windows.Forms;
using Mythic.Package;
using UOReader.Core;
using UOReader.Core.Format;

namespace UOReader;

public class SplashScreen : Form
{
	private IContainer m_a;

	private TextBox m_b;

	private BackgroundWorker m_c;

	private ProgressBar d;

	public SplashScreen()
	{
		a();
		d.Maximum = 100;
		d.Minimum = 0;
		d.Value = 0;
	}

	private void a(object A_0, EventArgs A_1)
	{
		Start();
	}

	public void Start()
	{
		bool flag = true;
		this.m_b.Text = "Loading settings..";
		if (!c())
		{
			this.m_b.Text = "Seeking UO folder..";
			flag = Utils.SeekUOFolder();
		}
		if (flag)
		{
			this.m_b.Text = "Loading files..";
			b();
			return;
		}
		this.m_b.Text = "No Ultima Online folder found!!!";
		Utils.ChangeInstallationFolder();
		Thread.Sleep(2000);
		Close();
	}

	public void SaveSettings()
	{
		using FileStream output = new FileStream("settings.bin", FileMode.Create);
		using BinaryWriter binaryWriter = new BinaryWriter(output);
		binaryWriter.Write(Utils.InstallationFolder);
	}

	private bool c()
	{
		if (File.Exists("settings.bin"))
		{
			using (FileStream input = new FileStream("settings.bin", FileMode.Open))
			{
				using BinaryReader binaryReader = new BinaryReader(input);
				Utils.InstallationFolder = binaryReader.ReadString();
			}
			if (Utils.IsValidInstallationFolder())
			{
				return true;
			}
		}
		return false;
	}

	private void b()
	{
		if (Utils.IsValidInstallationFolder())
		{
			this.m_b.Text = "Loading dictionary..";
			this.m_c.RunWorkerAsync("load");
		}
		else
		{
			MessageBox.Show("Error!");
		}
	}

	private void a(object A_0, DoWorkEventArgs A_1)
	{
		if ((string)A_1.Argument == "load")
		{
			int num = Enum.GetNames(typeof(Utils.FileNames)).Length;
			int num2 = 100 / num;
			int num3 = 0;
			HashDictionary.LoadDictionary("Dictionary.dic");
			this.m_c.ReportProgress(num2 * num3++);
			FilePointers.tileart = new Tileart(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Tileart));
			this.m_c.ReportProgress(num2 * num3++);
			textureData.LoadUOP(new Textures(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.LegacyTexture)), TextureType.MLTexture);
			this.m_c.ReportProgress(num2 * num3++);
			textureData.LoadUOP(new Textures(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Texture)), TextureType.ECTexture);
			tileartData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Tileart));
			this.m_c.ReportProgress(num2 * num3++);
			if (File.Exists(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.EffectTexture)))
			{
				textureData.LoadUOP(new Textures(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.EffectTexture)), TextureType.EffectTexture);
			}
			this.m_c.ReportProgress(num2 * num3++);
			if (File.Exists(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.MultiCollection)))
			{
				multiCollectionData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.MultiCollection));
			}
			this.m_c.ReportProgress(num2 * num3++);
			stringDictionaryData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.StringDictionary));
			this.m_c.ReportProgress(num2 * num3++);
			animationFrameData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.AnimationFrame));
			this.m_c.ReportProgress(num2 * num3++);
			terrainDefinitionData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.TerrainDefinition));
			this.m_c.ReportProgress(num2 * num3++);
			localizedStringData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.LocalizedStrings));
			this.m_c.ReportProgress(num2 * num3++);
			if (File.Exists(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.EffectDefinitionCol)))
			{
				effectDefinitionData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.EffectDefinitionCol));
			}
			this.m_c.ReportProgress(num2 * num3++);
			huesData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Hues));
			this.m_c.ReportProgress(num2 * num3++);
			if (File.Exists(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Facet)))
			{
				facetData.LoadUOP(Utils.InstallationFolder + Utils.GetStringValue(Utils.FileNames.Facet));
			}
			this.m_c.ReportProgress(100);
			A_1.Result = "load";
		}
	}

	private void a(object A_0, ProgressChangedEventArgs A_1)
	{
		d.Value = A_1.ProgressPercentage;
		int num = A_1.ProgressPercentage / (100 / Enum.GetNames(typeof(Utils.FileNames)).Length);
		if (num < Enum.GetNames(typeof(Utils.FileNames)).Length)
		{
			this.m_b.Text = "Loading " + Enum.GetNames(typeof(Utils.FileNames))[num] + "..";
		}
	}

	private void a(object A_0, RunWorkerCompletedEventArgs A_1)
	{
		if ((string)A_1.Result == "load")
		{
			d.Value = d.Maximum;
			Close();
		}
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
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(SplashScreen));
		this.m_b = new TextBox();
		this.m_c = new BackgroundWorker();
		d = new ProgressBar();
		SuspendLayout();
		this.m_b.BorderStyle = BorderStyle.FixedSingle;
		this.m_b.Location = new Point(12, 125);
		this.m_b.Name = "txt_display";
		this.m_b.ReadOnly = true;
		this.m_b.Size = new Size(396, 20);
		this.m_b.TabIndex = 0;
		this.m_c.WorkerReportsProgress = true;
		this.m_c.DoWork += a;
		this.m_c.ProgressChanged += a;
		this.m_c.RunWorkerCompleted += a;
		d.Location = new Point(12, 12);
		d.Name = "pBar";
		d.Size = new Size(396, 10);
		d.TabIndex = 1;
		base.AutoScaleDimensions = new SizeF(6f, 13f);
		base.AutoScaleMode = AutoScaleMode.Font;
		BackgroundImage = (Image)componentResourceManager.GetObject("$this.BackgroundImage");
		BackgroundImageLayout = ImageLayout.Center;
		base.ClientSize = new Size(420, 157);
		base.Controls.Add(d);
		base.Controls.Add(this.m_b);
		Cursor = Cursors.AppStarting;
		base.FormBorderStyle = FormBorderStyle.None;
		base.Name = "SplashScreen";
		base.StartPosition = FormStartPosition.CenterScreen;
		Text = "SplashScreen";
		ResumeLayout(performLayout: false);
		PerformLayout();
		base.Shown += a;
	}
}
