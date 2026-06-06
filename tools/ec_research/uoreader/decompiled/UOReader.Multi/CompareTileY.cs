using System.Collections.Generic;

namespace UOReader.Multi;

public class CompareTileY : IComparer<MultiTile>
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
		if (x.YOffset == y.YOffset)
		{
			return 0;
		}
		if (x.YOffset <= y.YOffset)
		{
			return -1;
		}
		return 1;
	}
}
