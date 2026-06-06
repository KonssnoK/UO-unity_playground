using System.IO;
using System.Text;

namespace UOReader;

public class SittingAnimationItem
{
	public byte HasSittingAnimation;

	public int unk1;

	public int unk2;

	public int unk3;

	public int unk4;

	public static SittingAnimationItem ReadSittingAnimation(BinaryReader r)
	{
		SittingAnimationItem sittingAnimationItem = new SittingAnimationItem();
		sittingAnimationItem.HasSittingAnimation = r.ReadByte();
		if (sittingAnimationItem.HasSittingAnimation != 0)
		{
			sittingAnimationItem.unk1 = r.ReadInt32();
			sittingAnimationItem.unk2 = r.ReadInt32();
			sittingAnimationItem.unk3 = r.ReadInt32();
			sittingAnimationItem.unk4 = r.ReadInt32();
		}
		return sittingAnimationItem;
	}

	public static string PrintSittingAnimation(SittingAnimationItem sa)
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("ChairRelated\t" + sa.HasSittingAnimation + " sitting data count(0:1)");
		if (sa.HasSittingAnimation != 0)
		{
			stringBuilder.AppendLine("Unk\t" + sa.unk1 + " " + sa.unk2 + " " + sa.unk3 + " " + sa.unk4);
		}
		return stringBuilder.ToString();
	}
}
