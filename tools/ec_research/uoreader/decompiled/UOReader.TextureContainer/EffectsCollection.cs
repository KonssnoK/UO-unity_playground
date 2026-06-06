using System.IO;
using System.Text;

namespace UOReader.TextureContainer;

public class EffectsCollection
{
	public static void Sub_4_6_30(BinaryReader r, StringBuilder sb)
	{
		EffectsID effectsID = (EffectsID)r.ReadInt32();
		sb.AppendLine(effectsID.ToString());
		switch (effectsID)
		{
		case EffectsID.EFFECT00:
			Effect0(r, sb);
			break;
		case EffectsID.EFFECT01:
			Effect1(r, sb);
			break;
		case EffectsID.EFFECT02:
			Effect2(r, sb);
			break;
		case EffectsID.EFFECT07:
			Effect7(r, sb);
			break;
		case EffectsID.EFFECT10:
			Effect10(r, sb);
			break;
		case EffectsID.EFFECT11:
			Effect11(r, sb);
			break;
		case EffectsID.EFFECT12:
			Effect12(r, sb);
			break;
		case EffectsID.EFFECT15:
			Effect15(r, sb);
			break;
		case EffectsID.EFFECT16:
			Effect16(r, sb);
			break;
		case EffectsID.EFFECT17:
			Effect17(r, sb);
			break;
		default:
			sb.Append("not implemented yet");
			break;
		}
	}

	public static void Effect1XSub(BinaryReader r, StringBuilder sb)
	{
		int num = r.ReadInt32();
		for (int i = 0; i < num; i++)
		{
			Sub_4_6_30(r, sb);
		}
	}

	public static void Effect_11_12_sub(BinaryReader r, StringBuilder sb)
	{
		int num = r.ReadInt32();
		sb.AppendLine("FX11_12_SC: " + num);
		sb.AppendLine();
		for (int i = 0; i < num; i++)
		{
			sb.AppendLine("Color:" + r.ReadInt32());
			Effect1XSub(r, sb);
			sb.AppendLine();
		}
	}

	public static void Effect0(BinaryReader r, StringBuilder sb)
	{
		int n = r.ReadInt32();
		int num = r.ReadInt32();
		int num2 = r.ReadInt32();
		int num3 = r.ReadInt32();
		int num4 = r.ReadInt32();
		byte b = r.ReadByte();
		int num5 = r.ReadInt32();
		byte b2 = r.ReadByte();
		byte b3 = r.ReadByte();
		byte b4 = r.ReadByte();
		sb.AppendLine(StringDictionary.GetDictionary().GetStringAtPosition(n));
		sb.Append(" " + num.ToString("X") + " " + num2.ToString("X") + " " + num3.ToString("X") + " " + num4.ToString("X") + " " + b + " " + num5.ToString("X") + " " + b2 + " " + b3 + " " + b4);
		sb.AppendLine();
	}

	public static void Effect1(BinaryReader r, StringBuilder sb)
	{
		int num = r.ReadInt32();
		int num2 = r.ReadInt32();
		sb.Append(num + " " + num2);
		sb.AppendLine();
	}

	public static void Effect2(BinaryReader r, StringBuilder sb)
	{
		int num = r.ReadInt32();
		for (int i = 1; i < num; i++)
		{
			Sub_4_6_30(r, sb);
			sb.AppendLine();
		}
	}

	public static void Effect7(BinaryReader r, StringBuilder sb)
	{
		for (int i = 0; i < 9; i++)
		{
			r.ReadByte();
			r.ReadByte();
		}
		sb.AppendLine();
	}

	public static void Effect10(BinaryReader r, StringBuilder sb)
	{
		Effect1XSub(r, sb);
		r.ReadInt32();
		r.ReadInt32();
		r.ReadByte();
	}

	public static void Effect11(BinaryReader r, StringBuilder sb)
	{
		Effect_11_12_sub(r, sb);
	}

	public static void Effect12(BinaryReader r, StringBuilder sb)
	{
		byte b = r.ReadByte();
		long num = r.ReadInt64();
		int num2 = r.ReadInt32();
		sb.Append(b + " " + num + " " + num2 + " ");
		sb.AppendLine();
		Effect1XSub(r, sb);
		Effect_11_12_sub(r, sb);
	}

	public static void Effect15(BinaryReader r, StringBuilder sb)
	{
		long num = r.ReadInt64();
		long num2 = r.ReadInt64();
		long num3 = r.ReadInt64();
		sb.AppendLine(num + " " + num2 + " " + num3);
	}

	public static void Effect16(BinaryReader r, StringBuilder sb)
	{
		int num = r.ReadInt32();
		sb.AppendLine("C:" + num);
		for (int i = 0; i < num; i++)
		{
			int num2 = r.ReadInt32();
			sb.Append(num2 + " ");
			Effect1XSub(r, sb);
		}
	}

	public static void Effect17(BinaryReader r, StringBuilder sb)
	{
		int num = r.ReadInt32();
		sb.Append(num + " ");
		Effect1XSub(r, sb);
	}
}
