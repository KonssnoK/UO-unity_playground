using System;
using System.Collections.Generic;
using System.Drawing;

namespace Paloma;

public class TargaExtensionArea
{
	private int a;

	private string b = string.Empty;

	private string c = string.Empty;

	private DateTime d = DateTime.Now;

	private string e = string.Empty;

	private TimeSpan f = TimeSpan.Zero;

	private string g = string.Empty;

	private string h = string.Empty;

	private Color i = Color.Empty;

	private int j;

	private int k;

	private int l;

	private int m;

	private int n;

	private int o;

	private int p;

	private int q;

	private List<int> r = new List<int>();

	private List<Color> s = new List<Color>();

	public int ExtensionSize => a;

	public string AuthorName => b;

	public string AuthorComments => c;

	public DateTime DateTimeStamp => d;

	public string JobName => e;

	public TimeSpan JobTime => f;

	public string SoftwareID => g;

	public string SoftwareVersion => h;

	public Color KeyColor => i;

	public int PixelAspectRatioNumerator => j;

	public int PixelAspectRatioDenominator => k;

	public float PixelAspectRatio
	{
		get
		{
			if (k > 0)
			{
				return (float)j / (float)k;
			}
			return 0f;
		}
	}

	public int GammaNumerator => l;

	public int GammaDenominator => m;

	public float GammaRatio
	{
		get
		{
			if (m > 0)
			{
				float num = (float)l / (float)m;
				return (float)Math.Round(num, 1);
			}
			return 1f;
		}
	}

	public int ColorCorrectionOffset => n;

	public int PostageStampOffset => o;

	public int ScanLineOffset => p;

	public int AttributesType => q;

	public List<int> ScanLineTable => r;

	public List<Color> ColorCorrectionTable => s;

	protected internal void SetExtensionSize(int intExtensionSize)
	{
		a = intExtensionSize;
	}

	protected internal void SetAuthorName(string strAuthorName)
	{
		b = strAuthorName;
	}

	protected internal void SetAuthorComments(string strAuthorComments)
	{
		c = strAuthorComments;
	}

	protected internal void SetDateTimeStamp(DateTime dtDateTimeStamp)
	{
		d = dtDateTimeStamp;
	}

	protected internal void SetJobName(string strJobName)
	{
		e = strJobName;
	}

	protected internal void SetJobTime(TimeSpan dtJobTime)
	{
		f = dtJobTime;
	}

	protected internal void SetSoftwareID(string strSoftwareID)
	{
		g = strSoftwareID;
	}

	protected internal void SetSoftwareVersion(string strSoftwareVersion)
	{
		h = strSoftwareVersion;
	}

	protected internal void SetKeyColor(Color cKeyColor)
	{
		i = cKeyColor;
	}

	protected internal void SetPixelAspectRatioNumerator(int intPixelAspectRatioNumerator)
	{
		j = intPixelAspectRatioNumerator;
	}

	protected internal void SetPixelAspectRatioDenominator(int intPixelAspectRatioDenominator)
	{
		k = intPixelAspectRatioDenominator;
	}

	protected internal void SetGammaNumerator(int intGammaNumerator)
	{
		l = intGammaNumerator;
	}

	protected internal void SetGammaDenominator(int intGammaDenominator)
	{
		m = intGammaDenominator;
	}

	protected internal void SetColorCorrectionOffset(int intColorCorrectionOffset)
	{
		n = intColorCorrectionOffset;
	}

	protected internal void SetPostageStampOffset(int intPostageStampOffset)
	{
		o = intPostageStampOffset;
	}

	protected internal void SetScanLineOffset(int intScanLineOffset)
	{
		p = intScanLineOffset;
	}

	protected internal void SetAttributesType(int intAttributesType)
	{
		q = intAttributesType;
	}
}
