using UnityEngine;
using UOReader;

namespace UOResources {
	public class UOSprite {
		public const float UOEC_HALFSIZE = 32.0f;
		public const float UO2D_HALFSIZE = 22.0f;
		public const float UOEC_SIZE = 64.0f;
		public const float UO2D_SIZE = 44.0f;
		public UOResource resource;

		public float _drawOffsetX = 0, _drawOffsetY = 0;
		protected int drawLayer = 0;
		protected int drawLayerTile = 0;

		private Sprite drawSprite = null;
		private bool _spriteCreated = false;
		protected bool _flipped = false;
		public Tileart tileart = null;
		private TileartImageOffset _imageOffset;
		protected bool _isWet = false;

		// Shared water material for all wet statics
		private static Material _waterMaterial;
		private static Material getWaterMaterial() {
			if (_waterMaterial != null) return _waterMaterial;
			Shader shader = Shader.Find("UO/WaterSprite");
			if (shader == null) return null;
			_waterMaterial = new Material(shader);
			_waterMaterial.SetTexture("_MainTex", Texture2D.whiteTexture); // will be overridden by sprite
			return _waterMaterial;
		}

		public UOSprite(uint spriteID) {
			tileart = UOResourceManager.getTileart(spriteID);
			resource = UOResourceManager.getResource(tileart);

			if (resource == null || tileart == null) return;

			_isWet = (tileart.flags & TileFlag.Wet) != 0;

			if (resource.isLegacy) {
				_imageOffset = tileart.offset2D;
			} else
				_imageOffset = tileart.offsetEC;

			_drawOffsetX = tileart.offsetEC.offX / UOEC_SIZE;
			_drawOffsetY = tileart.offsetEC.offY / UOEC_SIZE;
		}

		// Create the sprite once and cache it — called lazily on main thread
		private Sprite getOrCreateSprite() {
			if (_spriteCreated) return drawSprite;
			_spriteCreated = true;

			if (resource == null) return null;

			int texH = resource.getTexture().height;
			int texW = resource.getTexture().width;

			// Generated resources (water placeholder): use full texture as a flat tile
			if (resource.isGenerated) {
				_flipped = true;
				drawSprite = Sprite.Create(resource.getTexture(),
								new Rect(0, 0, texW, texH),
								new Vector2(0, 0));
				return drawSprite;
			}

			float width = _imageOffset.Xend - _imageOffset.Xstart;
			float height = _imageOffset.Yend;

			if (width == 0) {
				width = height = 64;
				_flipped = true;
			}

			float rectY = texH - height;
			if (rectY < 0) rectY = 0;
			if (rectY + height > texH) height = texH - rectY;
			if (_imageOffset.Xstart + width > texW)
				width = texW - _imageOffset.Xstart;

			if (width <= 0 || height <= 0) return null;

			drawSprite = Sprite.Create(resource.getTexture(),
							new Rect(_imageOffset.Xstart, rectY, width, height),
							new Vector2(0, 0));
			return drawSprite;
		}

		public virtual GameObject getDrawItem(int x, int y, int z) {
			return getDrawItem(x, y, z, 0, 0, 0);
		}

		public virtual GameObject getDrawItem(int x, int y, int z, int worldX, int worldY, int drawLayer) {
			Sprite sprite = getOrCreateSprite();
			if (sprite == null) {
				// Debug: create a visible magenta marker for statics with no sprite
				GameObject dbg = new GameObject(tileart != null ? "DBG_" + tileart.id.ToString() : "DBG_null");
				float dz = z * 6 / UOEC_SIZE;
				int dx = x + worldX, dy = y + worldY;
				float drx = ((-dy * 0.5f + dx * 0.5f) - 0.5f) / 1.6525f;
				float dry = ((-dy * 0.5f - dx * 0.5f) - 0.5f + dz) / 1.6525f;
				dbg.transform.Translate(drx, dry, 0);
				SpriteRenderer dbgR = dbg.AddComponent<SpriteRenderer>();
				// Create a small colored square sprite
				Texture2D dbgTex = new Texture2D(2, 2);
				dbgTex.SetPixels(new Color[] { Color.magenta, Color.magenta, Color.magenta, Color.magenta });
				dbgTex.Apply();
				dbgR.sprite = Sprite.Create(dbgTex, new Rect(0, 0, 2, 2), new Vector2(0.5f, 0.5f), 4f);
				dbgR.sortingOrder = dx + dy + z + drawLayer;
				return dbg;
			}

			float squareRoot = Mathf.Sqrt(2.0f);
			float realz = z * 6 / (UOEC_SIZE);

			x += worldX;
			y += worldY;

			float realx = (-y * 0.5f + x * 0.5f) - 0.5f + _drawOffsetX;
			float realy = (-y * 0.5f - x * 0.5f) - (_flipped ? 0.5f : 1f) - _drawOffsetY + realz;

			GameObject toret = new GameObject(tileart.id.ToString());
			realx /= 1.6525f;
			realy /= 1.6525f;

			toret.transform.Translate(realx, realy, 0);

			if (_flipped) {
				toret.transform.Rotate(0, 0, -45.0f);
				toret.transform.localScale /= squareRoot;
			}

			SpriteRenderer r = toret.AddComponent<SpriteRenderer>();
			r.sprite = sprite;
			r.sortingOrder = x + y + z + drawLayer;

			// Water statics: use animated water material
			if (_isWet) {
				Material wmat = getWaterMaterial();
				if (wmat != null)
					r.material = wmat;
			}

			return toret;
		}
	}
}
