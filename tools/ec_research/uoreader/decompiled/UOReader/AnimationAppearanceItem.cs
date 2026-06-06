using System.IO;
using System.Text;

namespace UOReader;

public class AnimationAppearanceItem
{
	public int count4;

	public AnimationAppearanceItemSub[] sub;

	public static AnimationAppearanceItem ReadAnimationAppearance(BinaryReader r)
	{
		AnimationAppearanceItem animationAppearanceItem = new AnimationAppearanceItem();
		animationAppearanceItem.count4 = r.ReadInt32();
		animationAppearanceItem.sub = new AnimationAppearanceItemSub[animationAppearanceItem.count4];
		for (int i = 0; i < animationAppearanceItem.count4; i++)
		{
			animationAppearanceItem.sub[i] = new AnimationAppearanceItemSub();
			animationAppearanceItem.sub[i].subval = r.ReadByte();
			if (animationAppearanceItem.sub[i].subval != 0)
			{
				if (animationAppearanceItem.sub[i].subval == 1)
				{
					animationAppearanceItem.sub[i].sub1 = new AnimationAppearanceItemSub1();
					animationAppearanceItem.sub[i].sub1.unk1 = r.ReadByte();
					animationAppearanceItem.sub[i].sub1.unk2 = r.ReadInt32();
				}
				continue;
			}
			uint num = r.ReadUInt32();
			animationAppearanceItem.sub[i].sub2 = new AnimationAppearanceItemSub2[num];
			for (int j = 0; j < animationAppearanceItem.sub[i].sub2.Length; j++)
			{
				animationAppearanceItem.sub[i].sub2[j] = new AnimationAppearanceItemSub2();
				animationAppearanceItem.sub[i].sub2[j].unk1 = r.ReadInt32();
				animationAppearanceItem.sub[i].sub2[j].unk2 = r.ReadInt32();
			}
		}
		return animationAppearanceItem;
	}

	public static string PrintAnimationAppearance(AnimationAppearanceItem aa)
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("C4\t" + aa.count4);
		for (int i = 0; i < aa.count4; i++)
		{
			stringBuilder.AppendLine("val\t" + aa.sub[i].subval + " animation appearance filter");
			if (aa.sub[i].subval != 0)
			{
				if (aa.sub[i].subval == 1)
				{
					stringBuilder.AppendLine("\t\t" + aa.sub[i].sub1.unk1 + " " + aa.sub[i].sub1.unk2);
				}
				continue;
			}
			stringBuilder.AppendLine("\tSubC\t" + aa.sub[i].sub2.Length);
			for (int j = 0; j < aa.sub[i].sub2.Length; j++)
			{
				stringBuilder.AppendLine("\t\t" + aa.sub[i].sub2[j].unk1 + " " + aa.sub[i].sub2[j].unk2);
			}
		}
		return stringBuilder.ToString();
	}
}
