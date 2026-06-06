using System.IO;
using System.Text;

namespace UOReader;

public class StackAlias
{
	public int amount;

	public int amountid;

	public static StackAlias ReadStackAlias(BinaryReader r)
	{
		StackAlias stackAlias = new StackAlias();
		stackAlias.amount = r.ReadInt32();
		stackAlias.amountid = r.ReadInt32();
		return stackAlias;
	}

	public static string PrintStackAlias(StackAlias s, int i)
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("#" + i + "\tAmount: " + s.amount + " - ID: " + s.amountid);
		return stringBuilder.ToString();
	}
}
