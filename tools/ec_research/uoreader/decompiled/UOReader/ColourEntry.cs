using System.Drawing;

namespace UOReader;

public class ColourEntry
{
	private byte a;

	private byte b;

	private byte c;

	private byte d;

	private Color e;

	public byte R => a;

	public byte G => b;

	public byte B => c;

	public byte Alpha => d;

	public Color Pixel => e;

	public ColourEntry(byte R, byte G, byte B, byte Alpha)
	{
		a = R;
		c = B;
		b = G;
		d = Alpha;
		e = Color.FromArgb(R, G, B);
	}
}
