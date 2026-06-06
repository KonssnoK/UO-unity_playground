using System;

public class StringValueAttribute : Attribute
{
	private string a;

	public string Value => a;

	public StringValueAttribute(string value)
	{
		a = value;
	}
}
