using KUtility;
using System.IO;
using UnityEngine;

namespace UOResources {
	public enum ShaderTypes{
		Sprite,
		Terrain
	};
	public class UOResource{
		public struct ddsData {
			public byte[] rawData;
			public int width;
			public int height;
			public TextureFormat format;
		};
		private ddsData _ddsData = new ddsData();
		private Texture2D texture = null;
		private Material material = null;
		private string stype;
		private ShaderTypes shaderType;
		uint references;//todo
		public bool isLegacy;

		// Cached generated water resource for statics with no textures
		private static UOResource _waterResource;
		private bool _isGeneratedWater;
		public bool isGenerated { get { return _isGeneratedWater; } }
		public static UOResource WaterResource {
			get {
				if (_waterResource == null)
					_waterResource = new UOResource(true);
				return _waterResource;
			}
		}

		/// <summary>
		/// Create a generated water resource — texture created lazily on main thread
		/// </summary>
		private UOResource(bool isWater) {
			_isGeneratedWater = true;
			isLegacy = false;
			shaderType = ShaderTypes.Sprite;
			stype = "Sprites/Default";
			// Texture will be created on main thread in getTexture()
		}

		public UOResource(byte[] raw, ShaderTypes type) :
			this(raw, type, false) {
		}

		public UOResource(byte[] raw, ShaderTypes type, bool _isLegacy) {
			DDSImage img = new DDSImage(raw);
			_ddsData.width = img.width;
			_ddsData.height = img.height;
			_ddsData.format = img.format;
			_ddsData.rawData = img.rawTextureData;
			isLegacy = _isLegacy;
			shaderType = type;

			switch (type) {
				case ShaderTypes.Sprite: stype = "Sprites/Default"; break;
				case ShaderTypes.Terrain: stype = "UO/TerrainTile"; break;
				default: stype = "Sprites/Default"; break;
			}
		}

		public Texture2D getTexture(){
			if (texture != null)
				return texture;

			if (_isGeneratedWater) {
				texture = new Texture2D(64, 64, TextureFormat.RGBA32, false);
				Color32 waterCol = new Color32(0, 40, 90, 220);
				var pixels = texture.GetPixelData<Color32>(0);
				for (int i = 0; i < pixels.Length; i++)
					pixels[i] = waterCol;
				texture.Apply();
				return texture;
			}

			texture = new Texture2D(_ddsData.width, _ddsData.height, _ddsData.format, false);
			texture.LoadRawTextureData(_ddsData.rawData);
			if (shaderType == ShaderTypes.Terrain) {
				texture.wrapMode = TextureWrapMode.Repeat;
				texture.filterMode = FilterMode.Bilinear;
			}
			texture.Apply();

			return texture;
		}

		public Material getMaterial() {
			if (material != null)
				return material;

			material = new Material(Shader.Find(stype));
			material.mainTexture = getTexture();

			return material;
		}
	}

}
