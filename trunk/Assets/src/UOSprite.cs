using System.Collections;
using UnityEngine;
using UOReader;

namespace UOResources {
	public class UOSprite {
		public const float UOEC_HALFSIZE = 32.0f;
		public const float UO2D_HALFSIZE = 22.0f;
		public const float UOEC_SIZE = 64.0f;
		public const float UO2D_SIZE = 44.0f;
		//public const float squareRoot = Mathf.Sqrt(2.0f);
		public UOResource resource;

		public float _drawOffsetX = 0, _drawOffsetY = 0;
		protected int drawLayer = 0;	//Layer computed with flags
		protected int drawLayerTile = 0; //Layer in the tile column at loading

		private Sprite drawSprite = null;
		public Tileart tileart = null;
		//public GameObject gameObject = null;

		public UOSprite(uint spriteID) {

			tileart = UOResourceManager.getTileart(spriteID);

			if (tileart.textures[0].texturePresent == 1) {
				resource = UOResourceManager.getResource(tileart.textures[0].texturesArray[0]);
			} /*else if (tileart.textures[1].texturePresent == 1) {
				resource = UOResourceManager.getLegacyResource(tileart.textures[1].texturesArray[0]);
			} */else {
				UOConsole.Fatal("texture is not present {0}", tileart.id);
				tileart = UOResourceManager.getTileart(1);
				resource = UOResourceManager.getResource(tileart.textures[0].texturesArray[0]);
			}

			_drawOffsetX = tileart.offsetEC.offX / UOEC_SIZE;
			_drawOffsetY = tileart.offsetEC.offY / UOEC_SIZE;

		}
		public virtual GameObject getDrawItem(int x, int y, int z) {
			return getDrawItem(x, y, z, 0, 0, 0);
		}

		//This function should never return null
		public virtual GameObject getDrawItem(int x, int y, int z, int worldX, int worldY, int drawLayer) {
			float width = tileart.offsetEC.Xend - tileart.offsetEC.Xstart;
			float height = tileart.offsetEC.Yend;// +tileart.offsetEC.Ystart;

			bool flipped = false;//TEMP - to move at load
			if (width == 0) {
				//UOConsole.Debug("width {0}, height {1}", width, height);
				width = height = 64;
				flipped = true;
			}

			if (resource == null)//Not all texture are correctly named in texture.uop, We should check also in legacyTextures.uop - TODO
				return new GameObject(tileart.id.ToString());

			drawSprite = Sprite.Create(resource.getTexture(),
							new Rect(tileart.offsetEC.Xstart, resource.getTexture().height - tileart.offsetEC.Yend,
										width, height),
							new Vector2(0, 0)
						);

			float squareRoot = Mathf.Sqrt(2.0f);
			float realz = z * 6 / (UOEC_SIZE);

			x += worldX;
			y += worldY;

			float realx = (-y * 0.5f + x * 0.5f) - 0.5f + _drawOffsetX;
			float realy = (-y * 0.5f - x * 0.5f) - (flipped ? 0.5f : 1f )- _drawOffsetY + realz;

			GameObject toret = new GameObject(tileart.id.ToString());
			//Create a visible object
			realx /= 1.6525f;//Moving from 100pixel based grid to 64pixel based
			realy /= 1.6525f;

			toret.transform.Translate(realx, realy, 0);

			if (flipped) {
				toret.transform.Rotate(0, 0, -45.0f);
				toret.transform.localScale /= squareRoot;
			}

			SpriteRenderer r = (SpriteRenderer)toret.AddComponent(typeof(SpriteRenderer));
			r.sprite = drawSprite;
			r.sortingOrder = x + y + z /*- worldY - worldX*/ + drawLayer;
			return toret;
		}
	}
}