using System.IO;
using System.Text;

namespace UOReader;

public class RadarColItem
{
	public byte R;

	public byte G;

	public byte B;

	public byte A;

	public static RadarColItem ReadRadarCol(BinaryReader r)
	{
		RadarColItem radarColItem = new RadarColItem();
		radarColItem.R = r.ReadByte();
		radarColItem.G = r.ReadByte();
		radarColItem.B = r.ReadByte();
		radarColItem.A = r.ReadByte();
		return radarColItem;
	}

	public static string PrintRadarColInfo(RadarColItem rc)
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("RadarCol\n\tR" + rc.R + " G" + rc.G + " B" + rc.B + " A" + rc.A);
		stringBuilder.AppendLine();
		return stringBuilder.ToString();
	}
}
