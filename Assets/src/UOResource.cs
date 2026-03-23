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
		uint references;//todo
		public bool isLegacy;

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

			switch (type) {
				case ShaderTypes.Sprite: stype = "Sprites/Default"; break;
				case ShaderTypes.Terrain: stype = "Diffuse"; break;
				default: stype = "Sprites/Default"; break;
			}
		}

		public Texture2D getTexture(){
			if (texture != null)
				return texture;

			texture = new Texture2D(_ddsData.width, _ddsData.height, _ddsData.format, false);
			texture.LoadRawTextureData(_ddsData.rawData);
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
