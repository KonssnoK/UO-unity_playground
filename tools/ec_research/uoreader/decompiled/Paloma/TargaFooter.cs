namespace Paloma;

public class TargaFooter
{
	private int a;

	private int b;

	private string c = string.Empty;

	private string d = string.Empty;

	public int ExtensionAreaOffset => a;

	public int DeveloperDirectoryOffset => b;

	public string Signature => c;

	public string ReservedCharacter => d;

	protected internal void SetExtensionAreaOffset(int intExtensionAreaOffset)
	{
		a = intExtensionAreaOffset;
	}

	protected internal void SetDeveloperDirectoryOffset(int intDeveloperDirectoryOffset)
	{
		b = intDeveloperDirectoryOffset;
	}

	protected internal void SetSignature(string strSignature)
	{
		c = strSignature;
	}

	protected internal void SetReservedCharacter(string strReservedCharacter)
	{
		d = strReservedCharacter;
	}
}
