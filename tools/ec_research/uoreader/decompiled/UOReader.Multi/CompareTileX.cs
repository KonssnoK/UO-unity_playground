using System.Collections.Generic;

namespace UOReader.Multi;

public class CompareTileX : IComparer<MultiTile>
{
	public int Compare(MultiTile x, MultiTile y)
	{
		if (x == null || y == null)
		{
			if (y == null && x == null)
			{
				return 0;
			}
			if (x == null)
			{
				return -1;
			}
			return 1;
		}
		if (x.XOffset == y.XOffset)
		{
			return 0;
		}
		if (x.XOffset <= y.XOffset)
		{
			return -1;
		}
		return 1;
	}
}
