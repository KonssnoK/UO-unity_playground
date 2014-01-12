using KUtility;
using System.Drawing;
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
		private ddsData _ddsData = new ddsData();//Used in the loading process
		private Texture2D texture = null;
		private Material material = null;
		private string stype;
		uint references;//todo

		public UOResource(byte[] raw, ShaderTypes type) {
			DDSImage img = new DDSImage(raw);
			_ddsData.width = img.images[0].Width;
			_ddsData.height = img.images[0].Height;
			_ddsData.format = img.format;
			_ddsData.rawData = ImageToByte2(img.images[0]);

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
			texture.LoadImage(_ddsData.rawData);

			return texture;
		}

		public Material getMaterial() {
			if (material != null)
				return material;

			material = new Material(Shader.Find(stype));
			material.mainTexture = getTexture();

			return material;
		}

		#region TEMP
		//THIS MUST BE CHANGED!!
		public static byte[] ImageToByte2(Bitmap img) {
			byte[] byteArray;
			using (MemoryStream stream = new MemoryStream()) {
				img.Save(stream, System.Drawing.Imaging.ImageFormat.Png);
				byteArray = stream.ToArray();
			}
			return byteArray;
		}
		#endregion
	}

}