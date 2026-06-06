namespace UOReader;

public class FrameEntry
{
	private ushort a;

	private ushort b;

	private short c;

	private short d;

	private short e;

	private short f;

	private uint g;

	private int h;

	private int i;

	public ushort ID => a;

	public ushort Frame => b;

	public short InitCoordsX => c;

	public short InitCoordsY => d;

	public short EndCoordsX => e;

	public short EndCoordsY => f;

	public uint DataOffset => g;

	public int Width => h;

	public int Height => i;

	public FrameEntry(ushort ID, ushort Frame, short initcoordsX, short InitCoordsY, short EndCoordsX, short EndcoordsY, uint DataOffset, uint Colournumber)
	{
		a = ID;
		b = Frame;
		c = initcoordsX;
		d = InitCoordsY;
		e = EndCoordsX;
		f = EndcoordsY;
		g = DataOffset;
		i = f - d;
		h = e - c;
	}
}
