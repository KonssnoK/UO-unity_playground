using UnityEngine;
using System.Collections;

public class TileMouseOver : MonoBehaviour {
	public Color highlightColor;
	Color normalColor;

	void Start() {
		highlightColor = Color.blue;
		normalColor = GetComponent<Renderer>().material.color;
	}
	
	// Update is called once per frame
	void Update() {

		Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);
		RaycastHit hitInfo;
		if (GetComponent<Collider>().Raycast(ray, out hitInfo, Mathf.Infinity)) {
			GetComponent<Renderer>().material.color = highlightColor;
		} else
			GetComponent<Renderer>().material.color = normalColor;

	}

}
