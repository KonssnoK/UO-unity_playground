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
		private TileartImageOffset _imageOffset;

		public UOSprite(uint spriteID) {

			tileart = UOResourceManager.getTileart(spriteID);
			resource = UOResourceManager.getResource(tileart);

			if (resource.isLegacy) {
				_imageOffset = tileart.offset2D;
			} else
				_imageOffset = tileart.offsetEC;

			_drawOffsetX = tileart.offsetEC.offX / UOEC_SIZE;
			_drawOffsetY = tileart.offsetEC.offY / UOEC_SIZE;

		}
		public virtual GameObject getDrawItem(int x, int y, int z) {
			return getDrawItem(x, y, z, 0, 0, 0);
		}

		//This function should never return null
		public virtual GameObject getDrawItem(int x, int y, int z, int worldX, int worldY, int drawLayer) {
			if (resource == null)
				return new GameObject(tileart.id.ToString());

			float width,height;
			width = _imageOffset.Xend - _imageOffset.Xstart;
			height = _imageOffset.Yend;// _imageOffset.Ystart;
			

			bool flipped = false;//TEMP - to move at load

			if (width == 0) {
				string tow = "", tow2 = "";
				for (int i = 0; i < tileart.textures[0].texturesCount; ++i) {
					tow += tileart.textures[0].texturesArray[i].unk6 + " ";
					tow2 += tileart.textures[0].texturesArray[i].unk7 + " ";
				}
				UOConsole.Debug("id {0}, width {1} height {2} unk6 {3} unk7 {4}", tileart.id, width, height, tow, tow2);
				width = height = 64;
				flipped = true;
			}

			drawSprite = Sprite.Create(resource.getTexture(),
							new Rect(_imageOffset.Xstart, resource.getTexture().height - _imageOffset.Yend,
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