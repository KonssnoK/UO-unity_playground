using System;
using UnityEngine;
using UOResources;

public class UOGraphic : MonoBehaviour {

	// Use this for initialization
	void Start () {
		UOConsole.Init();

		Console.WriteLine("Starting UOP preload..");
		UOResourceManager.loadUOPs();
		SectorsLoader.startLoader();
		//1367 is the britain cemetery
		//int sector = 1368;
	}

	//private UOFacetManager.Position playerPos = new UOFacetManager.Position(1400, 1500);

	// Update is called once per frame
	void Update () {
		UOFacetManager.updateMap(playerScript.getPlayer().position);
	}


	void OnDestroy() {
		SectorsLoader.endLoader();
		UOConsole.Release();
	}


}
