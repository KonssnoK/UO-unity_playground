using System.Collections.Generic;
using System.Drawing;
using System.IO;
using UnityEngine;
using UOResources;

[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]
[RequireComponent(typeof(MeshCollider))]
public class tilemap : MonoBehaviour {

	public static byte[] ImageToByte2(Bitmap img) {
		byte[] byteArray;
		using (MemoryStream stream = new MemoryStream()) {
			img.Save(stream, System.Drawing.Imaging.ImageFormat.Png);
			byteArray = stream.ToArray();
		}
		return byteArray;
	}

	// Use this for initialization
	void Start() {

	}

	void BuildMesh() {
	}

	// Update is called once per frame
	void Update() {
	}

}