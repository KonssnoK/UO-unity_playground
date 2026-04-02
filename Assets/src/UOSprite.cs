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
		public bool isWet => _isWet;

		// Shared water material for all wet statics
		private static Material _waterMaterial;
		private static Material getWaterMaterial() {
			if (_waterMaterial != null) return _waterMaterial;
			Shader shader = Shader.Find("UO/WaterSprite");
			if (shader == null) return null;
			_waterMaterial = new Material(shader);
			_waterMaterial.SetTexture("_MainTex", Texture2D.whiteTexture);
			return _waterMaterial;
		}

		// Shared quad mesh for water tiles (unit quad, 1x1)
		private static Mesh _waterQuadMesh;
		private static Mesh getWaterQuadMesh() {
			if (_waterQuadMesh != null) return _waterQuadMesh;
			_waterQuadMesh = new Mesh();
			_waterQuadMesh.vertices = new Vector3[] {
				new Vector3(0, 0, 0),
				new Vector3(1, 0, 0),
				new Vector3(0, -1, 0),
				new Vector3(1, -1, 0)
			};
			_waterQuadMesh.uv = new Vector2[] {
				new Vector2(0, 1),
				new Vector2(1, 1),
				new Vector2(0, 0),
				new Vector2(1, 0)
			};
			_waterQuadMesh.triangles = new int[] { 0, 1, 2, 1, 3, 2 };
			_waterQuadMesh.normals = new Vector3[] {
				Vector3.back, Vector3.back, Vector3.back, Vector3.back
			};
			return _waterQuadMesh;
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

			// Generated resources (water placeholder) or wet statics: use full texture as flat tile
			if (resource.isGenerated || _isWet) {
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

		/// <summary>
		/// Create a 3D quad for water statics in terrain mesh local space.
		/// Uses the same vertex formula as buildTerrainMesh so it shares the depth buffer.
		/// Must be parented to the terrain object (not statics).
		/// </summary>
		public GameObject getWaterQuad(int x, int y, int z, int worldX, int worldY) {
			const float Z_SCALE = 6f / UOEC_SIZE;
			float gz = z * Z_SCALE;
			int px = x + worldX;
			int py = y + worldY;

			// Match terrain vertex formula: Vector3(px - gz, -py + gz, 100 - gz)
			// Use same x/y shift from elevation so quad aligns with terrain mesh.
			// Nudge z slightly closer to camera so water renders in front of terrain.
			float zNudge = 0.05f;
			Vector3 v00 = new Vector3(px - gz,     -(py) + gz,     100 - gz - zNudge);
			Vector3 v10 = new Vector3((px+1) - gz, -(py) + gz,     100 - gz - zNudge);
			Vector3 v01 = new Vector3(px - gz,     -(py+1) + gz,   100 - gz - zNudge);
			Vector3 v11 = new Vector3((px+1) - gz, -(py+1) + gz,   100 - gz - zNudge);

			Mesh quad = new Mesh();
			quad.vertices = new Vector3[] { v00, v10, v01, v11 };
			quad.uv = new Vector2[] {
				new Vector2(0, 1), new Vector2(1, 1),
				new Vector2(0, 0), new Vector2(1, 0)
			};
			quad.triangles = new int[] { 0, 1, 2, 1, 3, 2 };
			quad.normals = new Vector3[] { Vector3.back, Vector3.back, Vector3.back, Vector3.back };
			quad.RecalculateBounds();

			GameObject go = new GameObject("water_" + tileart.id);
			MeshFilter mf = go.AddComponent<MeshFilter>();
			MeshRenderer mr = go.AddComponent<MeshRenderer>();
			mf.mesh = quad;

			Material wmat = getWaterMaterial();
			if (wmat != null) {
				if (resource != null && wmat.GetTexture("_MainTex") == Texture2D.whiteTexture)
					wmat.SetTexture("_MainTex", resource.getTexture());
				mr.sharedMaterial = wmat;
			}

			// No transform needed — vertices are already in terrain local space.
			// This object will be parented to the terrain GameObject.
			return go;
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

			return toret;
		}
	}
}
