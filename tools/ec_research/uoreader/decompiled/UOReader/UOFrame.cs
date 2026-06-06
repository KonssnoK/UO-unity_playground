using System;
using System.Collections.Generic;
using System.Drawing;
using System.Text;

namespace UOReader;

public class UOFrame
{
	private bool a(ref int A_0, ref int A_1, int A_2, int A_3)
	{
		A_0++;
		if (A_0 >= A_2)
		{
			A_0 = 0;
			A_1++;
		}
		if (A_1 < A_3 && A_0 < A_2)
		{
			return true;
		}
		return false;
	}

	private Color a(Color A_0, Color A_1, int A_2)
	{
		long num = A_0.ToArgb();
		long num2 = A_1.ToArgb();
		long num3 = (num & 0xFF00FF) * A_2;
		long num4 = (num2 & 0xFF00FF) * (16 - A_2);
		long num5 = num3 + num4;
		long num6 = ((num >> 4) & 0xFFF00FF0u) * A_2;
		long num7 = ((num2 >> 4) & 0xFFF00FF0u) * (16 - A_2);
		long num8 = num6 + num7;
		long num9 = ((num >> 4) & 0xFF00FF0) * A_2;
		long num10 = ((num2 >> 4) & 0xFF00FF0) * (16 - A_2);
		long num11 = num9 + num10;
		long num12 = (((num5 >> 4) ^ num8) & 0xFF00FF) ^ num11;
		return Color.FromArgb((int)num12);
	}

	public Bitmap LoadFrameImage(FrameEntry fromframe, byte[] _ImageData, long _ImageDataOffset, List<ColourEntry> m_Colours)
	{
		int num = Math.Abs(fromframe.EndCoordsX - fromframe.InitCoordsX);
		int num2 = Math.Abs(fromframe.EndCoordsY - fromframe.InitCoordsY);
		Bitmap bitmap = new Bitmap(num, num2);
		int i;
		int j;
		for (i = 0; i < num; i++)
		{
			for (j = 0; j < num2; j++)
			{
				bitmap.SetPixel(i, j, Color.PaleGreen);
			}
		}
		int num3 = (int)(fromframe.DataOffset - _ImageDataOffset);
		i = 0;
		j = 0;
		while (j < num2)
		{
			if (num3 >= _ImageData.Length)
			{
				continue;
			}
			byte b = _ImageData[num3++];
			if (b < 128)
			{
				while (b > 0)
				{
					a(ref i, ref j, num, num2);
					b--;
				}
				continue;
			}
			byte b2 = _ImageData[num3++];
			int num4 = b2 / 16;
			int num5 = b2 % 16;
			if (num4 > 0)
			{
				byte index = _ImageData[num3++];
				Color pixel = m_Colours[index].Pixel;
				Color pixel2 = bitmap.GetPixel(i, j);
				pixel = a(pixel, pixel2, num4);
				bitmap.SetPixel(i, j, pixel);
				a(ref i, ref j, num, num2);
			}
			for (b -= 128; b > 0; b--)
			{
				byte index = _ImageData[num3++];
				Color pixel = m_Colours[index].Pixel;
				bitmap.SetPixel(i, j, pixel);
				a(ref i, ref j, num, num2);
			}
			if (num5 > 0)
			{
				byte index = _ImageData[num3++];
				Color pixel = m_Colours[index].Pixel;
				Color pixel2 = bitmap.GetPixel(i, j);
				pixel = a(pixel, pixel2, num5);
				bitmap.SetPixel(i, j, pixel);
				a(ref i, ref j, num, num2);
			}
		}
		return bitmap;
	}

	public string FillTxtInfos(FrameEntry fe)
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.Append("X:\t" + fe.InitCoordsX + " ->\t" + fe.EndCoordsX + "\n");
		stringBuilder.Append("Y:\t" + fe.InitCoordsY + " ->\t" + fe.EndCoordsY + "\n");
		stringBuilder.Append("\nWidth: " + fe.Width + " Height: " + fe.Height);
		stringBuilder.Append("\n\nSize: " + fe.Width * fe.Height);
		return stringBuilder.ToString() + "\nOffset: " + fe.DataOffset;
	}
}
