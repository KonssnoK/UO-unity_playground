using System.IO;

namespace UOReader;

public class TileartPropItem
{
	public TileArtProperties prop;

	public int value;

	public static TileartPropItem ReadProp(BinaryReader r)
	{
		TileartPropItem tileartPropItem = new TileartPropItem();
		tileartPropItem.prop = (TileArtProperties)r.ReadByte();
		tileartPropItem.value = r.ReadInt32();
		return tileartPropItem;
	}
}
