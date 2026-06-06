using System;
using System.Collections.Generic;
using System.IO;

namespace UOReader;

public class Logger
{
	private Dictionary<string, DateTime> a;

	public void LoadKnownDates()
	{
		if (!File.Exists("LatestConfiguration.bin"))
		{
			a = new Dictionary<string, DateTime>();
			return;
		}
		using FileStream input = new FileStream("LatestConfiguration.bin", FileMode.Open);
		using (new BinaryReader(input))
		{
		}
	}
}
