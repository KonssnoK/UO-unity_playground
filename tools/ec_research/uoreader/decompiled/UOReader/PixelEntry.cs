namespace UOReader;

public class PixelEntry
{
	private ushort a;

	private ushort b;

	private byte[] c;

	public ushort RowHeader => a;

	public ushort RowOffset => b;

	public PixelEntry(ushort RowHead, ushort RowOff)
	{
		a = RowHead;
		b = RowOff;
	}
}
