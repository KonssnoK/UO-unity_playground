using UnityEngine;
using System.Collections;
using UOResources;

public class playerScript : MonoBehaviour {

	private static playerScript _player;
	public UOFacetManager.Position position = new UOFacetManager.Position(0, 0);
	public int X;
	public int Y;
	public int Z;

	// Use this for initialization
	void Start () {
		_player = this;
		position = new UOFacetManager.Position(1400, 1500);
		float realx = (-position.y * 0.5f + position.x * 0.5f) / 1.6525f;
		float realy = (-position.y * 0.5f - position.x * 0.5f) / 1.6525f;
		this.transform.Translate(new Vector3(realx, realy));
	}
	
	// Update is called once per frame
	void FixedUpdate () {
		float moveHorizontal = Input.GetAxis("Horizontal");
		float moveVertical = Input.GetAxis("Vertical");

		float realx = (-moveVertical * 0.5f + moveHorizontal * 0.5f) * Time.deltaTime;
		float realy = (-moveVertical * 0.5f - moveHorizontal * 0.5f) * Time.deltaTime;

		float speed = 3.0f;
		this.transform.Translate(new Vector3(realx, realy) * speed);

		this.position.x = (int)((this.transform.position.x - this.transform.position.y) * 1.6525f);
		this.position.y = (int)((- this.transform.position.x - this.transform.position.y) * 1.6525f);

		X = this.position.x;
		Y = this.position.y;
	}

	public static playerScript getPlayer() {
		return _player;
	}
}
