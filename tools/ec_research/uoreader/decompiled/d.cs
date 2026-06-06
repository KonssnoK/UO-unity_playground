using System.Drawing;

internal static class d
{
	internal static int a(byte A_0, int A_1, int A_2)
	{
		return (A_0 >> A_1) & ((1 << A_2) - 1);
	}

	internal static Color a(byte A_0, byte A_1)
	{
		int num = a(A_0, 2, 5);
		int red = num << 3;
		int num2 = a(A_0, 0, 2);
		int num3 = num2 << 6;
		num2 = a(A_1, 5, 3);
		int num4 = num2 << 3;
		int green = num3 + num4;
		int num5 = a(A_1, 0, 5);
		int blue = num5 << 3;
		int num6 = a(A_0, 7, 1);
		int alpha = num6 * 255;
		return Color.FromArgb(alpha, red, green, blue);
	}

	internal static string a(int A_0)
	{
		char[] array = new char[32];
		int num = 31;
		for (int i = 0; i < 32; i++)
		{
			if ((A_0 & (1 << i)) != 0)
			{
				array[num] = '1';
			}
			else
			{
				array[num] = '0';
			}
			num--;
		}
		return new string(array);
	}

	internal static string a(short A_0)
	{
		char[] array = new char[16];
		int num = 15;
		for (int i = 0; i < 16; i++)
		{
			if ((A_0 & (1 << i)) != 0)
			{
				array[num] = '1';
			}
			else
			{
				array[num] = '0';
			}
			num--;
		}
		return new string(array);
	}
}
