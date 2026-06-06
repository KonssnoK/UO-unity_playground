using System.IO;
using System.Text;
using UOReader.TextureContainer;

namespace UOReader;

public class EffectItem
{
	public EffectsID effectID;

	public string effectData;

	public static EffectItem ReadEffect(BinaryReader r)
	{
		EffectItem effectItem = new EffectItem();
		effectItem.effectID = (EffectsID)r.ReadInt32();
		StringBuilder stringBuilder = new StringBuilder();
		switch (effectItem.effectID)
		{
		case EffectsID.EFFECT00:
			EffectsCollection.Effect0(r, stringBuilder);
			break;
		case EffectsID.EFFECT01:
			EffectsCollection.Effect1(r, stringBuilder);
			break;
		case EffectsID.EFFECT02:
			EffectsCollection.Effect2(r, stringBuilder);
			break;
		case EffectsID.EFFECT07:
			EffectsCollection.Effect7(r, stringBuilder);
			break;
		case EffectsID.EFFECT10:
			EffectsCollection.Effect10(r, stringBuilder);
			break;
		case EffectsID.EFFECT11:
			EffectsCollection.Effect11(r, stringBuilder);
			break;
		case EffectsID.EFFECT12:
			EffectsCollection.Effect12(r, stringBuilder);
			break;
		case EffectsID.EFFECT15:
			EffectsCollection.Effect15(r, stringBuilder);
			break;
		case EffectsID.EFFECT16:
			EffectsCollection.Effect16(r, stringBuilder);
			break;
		case EffectsID.EFFECT17:
			EffectsCollection.Effect17(r, stringBuilder);
			break;
		default:
			stringBuilder.Append("not implemented yet");
			break;
		}
		effectItem.effectData = stringBuilder.ToString();
		return effectItem;
	}

	public static string PrintEffect(EffectItem e)
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine(e.effectID.ToString());
		stringBuilder.AppendLine(e.effectData);
		return stringBuilder.ToString();
	}
}
