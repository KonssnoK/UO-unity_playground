using System.Collections.Generic;
using System.Drawing;

namespace Paloma;

public class TargaHeader
{
	private byte a;

	private ColorMapType b;

	private ImageType c;

	private short d;

	private short e;

	private byte f;

	private short g;

	private short h;

	private short i;

	private short j;

	private byte k;

	private byte l;

	private VerticalTransferOrder m = VerticalTransferOrder.UNKNOWN;

	private HorizontalTransferOrder n = HorizontalTransferOrder.UNKNOWN;

	private byte o;

	private string p = string.Empty;

	private List<Color> q = new List<Color>();

	public byte ImageIDLength => a;

	public ColorMapType ColorMapType => b;

	public ImageType ImageType => c;

	public short ColorMapFirstEntryIndex => d;

	public short ColorMapLength => e;

	public byte ColorMapEntrySize => f;

	public short XOrigin => g;

	public short YOrigin => h;

	public short Width => i;

	public short Height => j;

	public byte PixelDepth => k;

	protected internal byte ImageDescriptor
	{
		get
		{
			return l;
		}
		set
		{
			l = value;
		}
	}

	public FirstPixelDestination FirstPixelDestination
	{
		get
		{
			if (m == VerticalTransferOrder.UNKNOWN || n == HorizontalTransferOrder.UNKNOWN)
			{
				return FirstPixelDestination.UNKNOWN;
			}
			if (m == VerticalTransferOrder.BOTTOM && n == HorizontalTransferOrder.LEFT)
			{
				return FirstPixelDestination.BOTTOM_LEFT;
			}
			if (m == VerticalTransferOrder.BOTTOM && n == HorizontalTransferOrder.RIGHT)
			{
				return FirstPixelDestination.BOTTOM_RIGHT;
			}
			if (m == VerticalTransferOrder.TOP && n == HorizontalTransferOrder.LEFT)
			{
				return FirstPixelDestination.TOP_LEFT;
			}
			return FirstPixelDestination.TOP_RIGHT;
		}
	}

	public VerticalTransferOrder VerticalTransferOrder => m;

	public HorizontalTransferOrder HorizontalTransferOrder => n;

	public byte AttributeBits => o;

	public string ImageIDValue => p;

	public List<Color> ColorMap => q;

	public int ImageDataOffset
	{
		get
		{
			int num = 18;
			num += a;
			int num2 = 0;
			switch (f)
			{
			case 15:
				num2 = 2;
				break;
			case 16:
				num2 = 2;
				break;
			case 24:
				num2 = 3;
				break;
			case 32:
				num2 = 4;
				break;
			}
			return num + e * num2;
		}
	}

	public int BytesPerPixel => k / 8;

	protected internal void SetImageIDLength(byte bImageIDLength)
	{
		a = bImageIDLength;
	}

	protected internal void SetColorMapType(ColorMapType eColorMapType)
	{
		b = eColorMapType;
	}

	protected internal void SetImageType(ImageType eImageType)
	{
		c = eImageType;
	}

	protected internal void SetColorMapFirstEntryIndex(short sColorMapFirstEntryIndex)
	{
		d = sColorMapFirstEntryIndex;
	}

	protected internal void SetColorMapLength(short sColorMapLength)
	{
		e = sColorMapLength;
	}

	protected internal void SetColorMapEntrySize(byte bColorMapEntrySize)
	{
		f = bColorMapEntrySize;
	}

	protected internal void SetXOrigin(short sXOrigin)
	{
		g = sXOrigin;
	}

	protected internal void SetYOrigin(short sYOrigin)
	{
		h = sYOrigin;
	}

	protected internal void SetWidth(short sWidth)
	{
		i = sWidth;
	}

	protected internal void SetHeight(short sHeight)
	{
		j = sHeight;
	}

	protected internal void SetPixelDepth(byte bPixelDepth)
	{
		k = bPixelDepth;
	}

	protected internal void SetVerticalTransferOrder(VerticalTransferOrder eVerticalTransferOrder)
	{
		m = eVerticalTransferOrder;
	}

	protected internal void SetHorizontalTransferOrder(HorizontalTransferOrder eHorizontalTransferOrder)
	{
		n = eHorizontalTransferOrder;
	}

	protected internal void SetAttributeBits(byte bAttributeBits)
	{
		o = bAttributeBits;
	}

	protected internal void SetImageIDValue(string strImageIDValue)
	{
		p = strImageIDValue;
	}
}
