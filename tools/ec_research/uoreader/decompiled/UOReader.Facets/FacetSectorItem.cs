using System.Drawing;
using System.Text;

namespace UOReader.Facets;

public class FacetSectorItem
{
	private const int a = 64;

	public byte facetID;

	public ushort sectorID;

	public FacetSectorTile[][] tiles = new FacetSectorTile[64][];

	private byte[] b;

	public FacetSectorItem(byte[] data)
	{
		b = data;
		Load();
	}

	public void Load()
	{
	}

	public override string ToString()
	{
		StringBuilder stringBuilder = new StringBuilder();
		stringBuilder.AppendLine("facet: " + facetID);
		stringBuilder.AppendLine("sector: " + sectorID);
		stringBuilder.AppendLine();
		for (int i = 0; i < 64; i++)
		{
			for (int j = 0; j < 64; j++)
			{
				stringBuilder.AppendLine("x " + i + " y " + j + " z " + tiles[i][j].z + "\t land " + tiles[i][j].landgraphic + "\t delC " + tiles[i][j].delimitersCount + "\t staC " + tiles[i][j].staticsCount);
			}
		}
		return stringBuilder.ToString();
	}

	public Bitmap getImage()
	{
		Bitmap bitmap = new Bitmap(1024, 1024);
		Graphics graphics = Graphics.FromImage(bitmap);
		Pen pen = new Pen(Color.Black);
		SolidBrush solidBrush = new SolidBrush(Color.Black);
		graphics.DrawRectangle(pen, 0, 0, 1024, 1024);
		for (int i = 0; i < 64; i++)
		{
			for (int j = 0; j < 64; j++)
			{
				Bitmap image = new Bitmap(16, 16);
				Graphics graphics2 = Graphics.FromImage(image);
				int red = 255 * tiles[i][j].landgraphic / 17000;
				int green = 255 * tiles[i][j].landgraphic / 17000;
				int blue = 255;
				solidBrush.Color = Color.FromArgb(red, green, blue);
				graphics2.FillRectangle(solidBrush, 0, 0, 16, 16);
				graphics2.Dispose();
				int x = i * 16;
				int y = j * 16;
				graphics.DrawImage(image, x, y);
			}
		}
		graphics.Dispose();
		return bitmap;
	}
}
