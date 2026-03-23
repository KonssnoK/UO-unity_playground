using UnityEngine;
using UOResources;

public class UOGraphic : MonoBehaviour {

	// Use this for initialization
	void Start () {
		UOConsole.Init();

		UnityEngine.Debug.Log("Starting UOP preload..");
		UOResourceManager.loadUOPs();
		SectorsLoader.startLoader();
		//1367 is the britain cemetery
		//int sector = 1368;
	}

	//private UOFacetManager.Position playerPos = new UOFacetManager.Position(1400, 1500);

	// Update is called once per frame
	private bool _loggedPlayerNull = false;
	void Update () {
		playerScript player = playerScript.getPlayer();
		if (player == null) {
			if (!_loggedPlayerNull) {
				UnityEngine.Debug.LogWarning("playerScript.getPlayer() is null - is the playerScript component attached to the Player GameObject?");
				_loggedPlayerNull = true;
			}
			return;
		}
		UOFacetManager.updateMap(player.position);
	}


	void OnDestroy() {
		SectorsLoader.endLoader();
		UOConsole.Release();
	}


}
