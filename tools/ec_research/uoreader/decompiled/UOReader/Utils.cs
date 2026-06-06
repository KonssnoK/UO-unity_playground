using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System.Windows.Forms;
using Microsoft.Win32;

namespace UOReader;

public class Utils
{
	public enum FileNames
	{
		[StringValue("\\MultiCollection.uop")]
		MultiCollection = 1,
		[StringValue("\\string_dictionary.uop")]
		StringDictionary,
		[StringValue("\\animationframe")]
		AnimationFrame,
		[StringValue("\\TerrainDefinition.uop")]
		TerrainDefinition,
		[StringValue("\\LocalizedStrings.uop")]
		LocalizedStrings,
		[StringValue("\\EffectDefinitionCollection.uop")]
		EffectDefinitionCol,
		[StringValue("\\LegacyTexture.uop")]
		LegacyTexture,
		[StringValue("\\Texture.uop")]
		Texture,
		[StringValue("\\tileart.uop")]
		Tileart,
		[StringValue("\\EffectTexture.uop")]
		EffectTexture,
		[StringValue("\\SystemTextures.uop")]
		SystemTextures,
		[StringValue("\\TerrainTexture.uop")]
		TerrainTexture,
		[StringValue("\\Hues.uop")]
		Hues,
		[StringValue("\\facet0.uop")]
		Facet
	}

	public class NodeSorter : IComparer
	{
		public int Compare(object x, object y)
		{
			TreeNode treeNode = (TreeNode)x;
			TreeNode treeNode2 = (TreeNode)y;
			return treeNode.Text.CompareTo(treeNode2.Text);
		}
	}

	private const string m_a = "\\uosa.exe";

	private const string b = "\\uosa.patched.exe";

	private const string c = "Electronic Arts\\EA Games\\Ultima Online Stygian Abyss";

	private const string d = "Electronic Arts\\EA Games\\Ultima Online High Seas Enhanced BETA";

	private const string e = "Electronic Arts\\EA Games\\Ultima Online Enhanced";

	public const string SettingsFile = "settings.bin";

	public static string InstallationFolder = "";

	public static int ClientVersion = 0;

	private static Dictionary<Enum, StringValueAttribute> f = new Dictionary<Enum, StringValueAttribute>();

	public static bool IsValidInstallationFolder()
	{
		if (Directory.Exists(InstallationFolder))
		{
			return CheckFolderForFiles(InstallationFolder) == null;
		}
		ChangeInstallationFolder();
		return false;
	}

	public static void ChangeInstallationFolder()
	{
		FolderBrowserDialog folderBrowserDialog = new FolderBrowserDialog();
		folderBrowserDialog.SelectedPath = InstallationFolder;
		DialogResult dialogResult = folderBrowserDialog.ShowDialog();
		if (dialogResult != DialogResult.OK)
		{
			return;
		}
		string text = CheckFolderForFiles(folderBrowserDialog.SelectedPath);
		if (text == null)
		{
			InstallationFolder = folderBrowserDialog.SelectedPath;
			using FileStream output = new FileStream("settings.bin", FileMode.Create);
			using BinaryWriter binaryWriter = new BinaryWriter(output);
			binaryWriter.Write(InstallationFolder);
			return;
		}
		MessageBox.Show($"The folder you selected does not contains '{text}', required file.\nNo changes have been made.");
	}

	public static string CheckFolderForFiles(string f)
	{
		if (Directory.Exists(f))
		{
			string stringValue = GetStringValue(FileNames.LegacyTexture);
			if (!File.Exists(f + stringValue))
			{
				return stringValue;
			}
			stringValue = GetStringValue(FileNames.Texture);
			if (!File.Exists(f + stringValue))
			{
				return stringValue;
			}
			stringValue = GetStringValue(FileNames.Tileart);
			if (!File.Exists(f + stringValue))
			{
				return stringValue;
			}
		}
		return null;
	}

	public static bool SeekUOFolder()
	{
		string text = a("Electronic Arts\\EA Games\\Ultima Online Enhanced");
		if (text == null)
		{
			text = a("Electronic Arts\\EA Games\\Ultima Online High Seas Enhanced BETA");
			if (text == null)
			{
				text = a("Electronic Arts\\EA Games\\Ultima Online Stygian Abyss");
				if (text == null)
				{
					return false;
				}
			}
		}
		InstallationFolder = text;
		return true;
	}

	private static string a(string A_0)
	{
		bool flag = IntPtr.Size == 8;
		try
		{
			if (flag)
			{
				A_0 = "Wow6432Node\\" + A_0;
			}
			RegistryKey registryKey = Registry.LocalMachine.OpenSubKey($"SOFTWARE\\{A_0}");
			if (registryKey == null)
			{
				registryKey = Registry.CurrentUser.OpenSubKey($"SOFTWARE\\{A_0}");
				if (registryKey == null)
				{
					return null;
				}
			}
			string text2;
			if (!(registryKey.GetValue("ExePath") is string { Length: >0 } text) || (!Directory.Exists(text) && !File.Exists(text)))
			{
				text2 = registryKey.GetValue("InstallDir") as string;
				if (text2 == null || text2.Length <= 0 || (!Directory.Exists(text2) && !File.Exists(text2)))
				{
					return null;
				}
			}
			else
			{
				text2 = Path.GetDirectoryName(text);
			}
			if (text2 == null || !Directory.Exists(text2))
			{
				return null;
			}
			return text2;
		}
		catch
		{
			return null;
		}
	}

	public static string GetStringValue(Enum value)
	{
		string result = null;
		Type type = value.GetType();
		if (f.ContainsKey(value))
		{
			result = f[value].Value;
		}
		else
		{
			FieldInfo field = type.GetField(value.ToString());
			StringValueAttribute[] array = field.GetCustomAttributes(typeof(StringValueAttribute), inherit: false) as StringValueAttribute[];
			if (array.Length > 0)
			{
				f.Add(value, array[0]);
				result = array[0].Value;
			}
		}
		return result;
	}
}
