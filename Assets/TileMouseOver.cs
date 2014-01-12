using UnityEngine;
using System.Collections;

public class TileMouseOver : MonoBehaviour {
	public Color highlightColor;
	Color normalColor;

	void Start() {
		highlightColor = Color.blue;
		normalColor = renderer.material.color;
	}
	
	// Update is called once per frame
	void Update() {

		Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
		RaycastHit hitInfo;
		if (collider.Raycast(ray, out hitInfo, Mathf.Infinity)) {
			renderer.material.color = highlightColor;
		} else
			renderer.material.color = normalColor;

	}

}
