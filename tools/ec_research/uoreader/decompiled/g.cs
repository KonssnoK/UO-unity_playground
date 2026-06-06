using System;
using System.Windows.Forms;
using UOReader;

internal static class g
{
	[STAThread]
	private static void a()
	{
		Application.EnableVisualStyles();
		Application.SetCompatibleTextRenderingDefault(defaultValue: false);
		Application.Run(new Main());
	}
}
