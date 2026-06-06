using System.Collections.Generic;
using System.Drawing;

namespace UOReader.Multi;

public class MultiTile
{
	private Bitmap a;

	private ushort b;

	private short c;

	private short d;

	private short e;

	private byte f;

	private byte g;

	private List<string> h;

	private ushort i;

	private short j;

	private short k;

	private short l;

	private byte m;

	public Bitmap Graphic
	{
		get
		{
			return a;
		}
		set
		{
			a = value;
		}
	}

	public ushort ID => b;

	public short XOffset => c;

	public short YOffset => d;

	public short ZOffset => e;

	public byte Unk1 => f;

	public byte Unk2 => g;

	public List<string> UnkList => h;

	public MultiTile(ushort graphic, short x, short y, short z, byte unk, byte unk2)
	{
		b = graphic;
		c = x;
		d = y;
		e = z;
		f = unk;
		g = unk2;
		h = new List<string>();
	}
}
