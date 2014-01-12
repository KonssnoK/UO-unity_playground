using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using UOReader;

namespace UOResources {
	public class UOStatic : UOSprite {
		public UOStatic(uint spriteID)
			: base(spriteID) {

			//Layer positioning
			if ((tileart.flags & TileFlag.Background) == 0)
				drawLayer++;
			foreach (TileartPropItem p in tileart.props) {
				if (p.prop == TileArtProperties.Height) {
					if (p.value != 0)
						drawLayer++;
				}
			}
			if ((tileart.flags & TileFlag.Surface) != 0)
				drawLayer--;

		}

		public GameObject getDrawItem(int x, int y, int z, int worldX, int worldY) {
			return base.getDrawItem(x, y, z, worldX, worldY, drawLayer);

		}
	}
}
