using System.Collections.Generic;
using System.IO;
using Mythic.Package;
using UnityEngine;
using UOReader;
using System.Threading;
using System.Collections;

///
/// Kons - 2013/2014
///

namespace UOResources {
	public class UOFacetManager {

		public class uvStatus{
			public float u;
			public float v;
			public uvStatus(){}
		}


		public class facetSectorMesh{
			public Vector3[] vertices;
			public int[] triangles;
			public Vector3[] normals;
			public Vector2[] uvs;
			public Dictionary<uint, List<int>> subMeshes = new Dictionary<uint, List<int>>();
			public Dictionary<uint, uvStatus> subMeshTextureOffset = new Dictionary<uint, uvStatus>();
			public List<Material> materials = new List<Material>();
			public facetSectorMesh() {
			}
		};


		private const string fileDirectory = "Assets\\UOPs\\";


		private static Dictionary<int, FacetSector> facetSectors = new Dictionary<int, FacetSector>();
		private static Dictionary<uint, UOSprite> facetSprites = new Dictionary<uint, UOSprite>();

		/// <summary>
		/// Given coordinates returns the current sectorID
		/// </summary>
		/// <param name="x"></param>
		/// <param name="y"></param>
		/// <returns></returns>
		public static int getSectorID(int x, int y) {
			return (y / 64) + (x / 64) * 64; 
		}

		public static FacetSector getSector(int x, int y) {
			return getSector(getSectorID(x, y));
		}

		/// <summary>
		/// Get a FacetSector given an ID. FacetSector contains tile information about current block.
		/// UOPs related.
		/// </summary>
		/// <param name="sector"></param>
		/// <returns></returns>
		public static FacetSector getSector(int sector) {
			//Fast search
			if(facetSectors.ContainsKey(sector))
				return facetSectors[sector];

			int currentFacet = 0;
			//Look for the file in facet hashes
			string toHash = string.Format("build/sectors/facet_{0:D2}/{1:D8}.bin", currentFacet , sector);
			ulong hash = HashDictionary.HashFileName(toHash);

			if(!UOResourceManager.uopHashes.facet0Hashes.ContainsKey(hash)){
				UOConsole.Fatal("Cannot find {0} in facet0Hashes", toHash);
				return null;
			}
			UOResourceManager.uopMapping_t map = UOResourceManager.uopHashes.facet0Hashes[hash];

			MythicPackage _uop = new MythicPackage(fileDirectory + "facet0.uop");
			byte[] raw = _uop.Blocks[map.block].Files[map.file].Unpack(_uop.FileInfo.FullName);

			FacetSector fs;

			using(MemoryStream ms = new MemoryStream(raw)){
				using (BinaryReader r = new BinaryReader(ms)) {
					fs = FacetSector.readSector(r);
				}
			}

			facetSectors[sector] = fs;
			return fs;
		}

		#region terrain
		/// <summary>
		/// MAIN THREAD
		/// This function loads a sector and puts the resulting terrain mesh into a GameObject
		/// </summary>
		/// <param name="sectorID"></param>
		/// <returns></returns>
		public static GameObject buildTerrain(int sectorID) {
			GameObject terrain = new GameObject("terrain" + sectorID);
			MeshFilter mf = (MeshFilter)terrain.AddComponent(typeof(MeshFilter));
			MeshRenderer mr = (MeshRenderer)terrain.AddComponent(typeof(MeshRenderer));
			//MeshCollider mc = (MeshCollider)terrain.AddComponent(typeof(MeshCollider));

			//Load a facet sector
			UOReader.FacetSector sec = UOFacetManager.getSector(sectorID);
			
			//Set the data to a mesh
			Mesh mesh = new Mesh();
			UOFacetManager.facetSectorMesh m = UOFacetManager.buildTerrainMesh(sec);
			//Copy values from the specific class.... i tried using directly a mesh but didn't worked..
			mesh.vertices = m.vertices;
			mesh.triangles = m.triangles;
			mesh.normals = m.normals;
			mesh.uv = m.uvs;
			int i = 0;
			mesh.subMeshCount = m.subMeshes.Values.Count;
			UOConsole.Fatal("terrain: {0} subMeshes", mesh.subMeshCount);
			foreach (uint k in m.subMeshes.Keys) {
				//UOConsole.Fatal(string.Format("idx {0} texture {1} count: {2}", i, k, m.subMeshes[k].Count));
				mesh.SetTriangles(m.subMeshes[k].ToArray(), i++);
			}

			mf.mesh = mesh;
			mr.materials = m.materials.ToArray();

			float sq = Mathf.Sqrt(2.0f);
			terrain.transform.Rotate(0, 0, -45.0f);
			terrain.transform.localScale *= 1 / sq;
			terrain.transform.localScale /= 1.6525f;//Moving from 100pixel based to 64pixel based
			return terrain;
		}

		/// <summary>
		/// MAIN THREAD -> TODO : Separate loading from GameObjects.
		/// Build the terrain mesh for the current sectorID
		/// </summary>
		/// <param name="fs"></param>
		/// <returns></returns>
		private static facetSectorMesh buildTerrainMesh(FacetSector fs) {
			facetSectorMesh mesh = new facetSectorMesh();

			int worldY = (fs.sectorID % 64) * 64;
			int worldX = (fs.sectorID / 64) * 64;

			mesh.vertices = new Vector3[4 * (64 * 64)];
			mesh.normals = new Vector3[4 * (64 * 64)];
			mesh.uvs = new Vector2[4 * 64 * 64];

			mesh.triangles = new int[3 * (64 * 64 * 2)];

			int flipper = -1;
			for (int x = 0; x < fs.tiles.Length; ++x) {
				for (int y = 0; y < fs.tiles[x].Length; ++y) {
					float z = +fs.tiles[x][y].z * 6 / UOSprite.UOEC_SIZE;
					int idxVertices = 4 * (x + y * 64);

					float z0, z1, z2, z3;
					z0 = z;
					z1 = z;
					z2 = z;
					z3 = z;
					if(x == 0){
						//TODO: take information from other sector delimiters
					} else if (y == 0) {
					} else {
						z0 = (fs.tiles[x - 1][y - 1].z) * 6 / (UOSprite.UOEC_SIZE);
						z1 = (fs.tiles[x][y - 1].z) * 6 / (UOSprite.UOEC_SIZE);
						z2 = (fs.tiles[x - 1][y].z) * 6 / (UOSprite.UOEC_SIZE);
						z3 = (fs.tiles[x][y].z) * 6 / (UOSprite.UOEC_SIZE);
					}

					int _x = x + worldX, _y = y + worldY;
					// 0	1
					// |  \ |
					// 2	3
					//Vertices
					mesh.vertices[idxVertices + 0] = new Vector3(_x - z0, flipper * _y + z0, 100 - z0);
					mesh.vertices[idxVertices + 1] = new Vector3(_x + 1 - z1, flipper * _y + z1, 100 - z1);
					mesh.vertices[idxVertices + 2] = new Vector3(_x - z2, flipper * (_y + 1) + z2, 100 - z2);
					mesh.vertices[idxVertices + 3] = new Vector3(_x + 1 - z3, flipper * (_y + 1) + z3, 100 - z3);

					//Normals
					mesh.normals[idxVertices + 0] = mesh.normals[idxVertices + 1] = mesh.normals[idxVertices + 2] = mesh.normals[idxVertices + 3] = Vector3.up;


					//Triangles - Clockwise
					List<int> subTriangles;// List containin all indices of sametexture
					uvStatus uvOffset;

					TextureImageInfo textureInfo = UOResourceManager.getLandtileTextureID(fs.tiles[x][y].landtileGraphic);
					if (mesh.subMeshes.ContainsKey(textureInfo.textureIDX)) {
						subTriangles = mesh.subMeshes[textureInfo.textureIDX];//Get the already instanced list
						uvOffset = mesh.subMeshTextureOffset[textureInfo.textureIDX];
					} else {
						//Create a new list and set it
						subTriangles = new List<int>();
						mesh.subMeshes.Add(textureInfo.textureIDX, subTriangles);
						//Each subMesh has a material 
						Material mat = UOResourceManager.getResource(textureInfo, ShaderTypes.Terrain).getMaterial();
						mesh.materials.Add(mat);
						//
						uvOffset = new uvStatus();
						uvOffset.u = 0;
						uvOffset.v = 0;
						mesh.subMeshTextureOffset[textureInfo.textureIDX] = uvOffset;
					}

					//Bottom triangles
					int offset = idxVertices;
					subTriangles.Add(offset);
					subTriangles.Add(offset + 3);
					subTriangles.Add(offset + 2);
					//Upper triangles
					subTriangles.Add(offset);
					subTriangles.Add(offset + 1);
					subTriangles.Add(offset + 3);
					//End Triangles

					//UVs
					float us, ue, vs, ve;
					float texSize = 1.0f / textureInfo.repetition;
					us = uvOffset.u;
					ue = uvOffset.u + texSize;
					vs = uvOffset.v;
					ve = uvOffset.v + texSize;

					if (ue > 1.0f)
						ue -= 1.0f;
					if (ve > 1.0f)
						ve -= 1.0f;
					mesh.uvs[idxVertices + 0] = new Vector2(us, ve);
					mesh.uvs[idxVertices + 1] = new Vector2(ue, ve);
					mesh.uvs[idxVertices + 2] = new Vector2(us, vs);
					mesh.uvs[idxVertices + 3] = new Vector2(ue, vs);

					//TODO Correct handling
					//uvOffset.u += texSize;
					//uvOffset.v += texSize;
					if (uvOffset.v >= 1.0f)
						uvOffset.v = 0;
					if (uvOffset.u >= 1.0f)
						uvOffset.u = 0;
				}
			}

			
			return mesh;
		}
		#endregion terrain

		/// <summary>
		/// LOADER THREAD
		/// loads the sprites of a given sector to the faceSprites Dictionary
		/// </summary>
		/// <param name="sectorID"></param>
		public static void loadSprites(int sectorID) {
			int totalStatics = 0;//Just for info 
			int totalStaticsSingle = 0;//Just for info

			UOReader.FacetSector fs = UOFacetManager.getSector(sectorID);

			for (int x = 0; x < fs.tiles.Length; ++x) {
				for (int y = 0; y < fs.tiles[x].Length; ++y) {

					if (fs.tiles[x][y].staticsCount <= 0)
						continue;

					for (int i = 0; i < fs.tiles[x][y].statics.Length; ++i) {
						facetStatic_t st = fs.tiles[x][y].statics[i];

						if (!facetSprites.ContainsKey(st.graphic)) {
							facetSprites.Add(st.graphic, new UOStatic(st.graphic));
							totalStaticsSingle++;
						}

						totalStatics++;
					}
				}
			}

			UOConsole.Debug("LOADER: instanced {0} statics, based on {1} uniques.", totalStatics, totalStaticsSingle);

			return;
		}

		/// <summary>
		/// Client sensing range for updating surrounding blocks
		/// </summary>
		public const int UPDATE_RANGE = 22;

		/// <summary>
		/// MAIN THREAD - Called each frame
		/// Given a position updates the current block and the surrounding ones
		/// - Get sectors IDs
		/// - Enqueue loading to LOADER
		/// - Updates visible blocks
		/// </summary>
		/// <param name="p"></param>
		public static void updateMap(Position p) {

			int currentSector = getSectorID(p.x, p.y);
			SectorsLoader.Enqueue(currentSector);

			/*	West	North
			 *		  x
			 *	South	East
			 */
			
			int west = getSectorID(p.x - UPDATE_RANGE, p.y - UPDATE_RANGE);
			int north = getSectorID(p.x + UPDATE_RANGE, p.y - UPDATE_RANGE);
			int east = getSectorID(p.x + UPDATE_RANGE, p.y + UPDATE_RANGE);
			int south = getSectorID(p.x - UPDATE_RANGE, p.y + UPDATE_RANGE);

			//Updates sectors to load
			visibleMapIDX[0] = currentSector;
			if (currentSector != west) {
				SectorsLoader.Enqueue(west);
				visibleMapIDX[1] = west;
			} else 
				visibleMapIDX[1] = -1;//Removes the block from the "toDraw" list
			if (currentSector != north) {
				SectorsLoader.Enqueue(north);
				visibleMapIDX[2] = north;
			} else
				visibleMapIDX[2] = -1;
			if (currentSector != east) {
				SectorsLoader.Enqueue(east);
				visibleMapIDX[3] = east;
			} else
				visibleMapIDX[3] = -1;
			if (currentSector != south) {
				SectorsLoader.Enqueue(south);
				visibleMapIDX[4] = south;
			} else
				visibleMapIDX[4] = -1;

			/*graphicSector g = graphicSectors[currentSector];
			if (g == null) {
				g = new graphicSector(currentSector);
				graphicSectors[currentSector] = g;
			}
			if (!g.fullLoaded) {
				g.loadObjects();
			}*/


			//Updates all the blocks currently used - (to be drawn)
			for (int i = 0; i < 5; ++i) {
				if (visibleMapIDX[i] != -1) {
					visibleMap[i] = graphicSectors[visibleMapIDX[i]];
					if (visibleMap[i] == null) {
						visibleMap[i] = new graphicSector(visibleMapIDX[i]);
						graphicSectors[visibleMapIDX[i]] = visibleMap[i];
					}
					if (!visibleMap[i].fullLoaded) {
						visibleMap[i].loadObjects(p);
					}
				}
			}
			return;
		}


		public static graphicSector[] visibleMap = new graphicSector[5];
		/// <summary>
		/// Currently drawn sectors IDs. -1 = no drawing.
		/// </summary>
		public static int[] visibleMapIDX = new int[5] { -1, -1, -1, -1, -1 };
		/// <summary>
		/// GameObject containing the current facet
		/// </summary>
		public static GameObject theMap = new GameObject("facet");
		public static GameObject[] statics = new GameObject[SectorsLoader.SECTORS_COUNT];
		public static GameObject[] terrains = new GameObject[SectorsLoader.SECTORS_COUNT];

		public static graphicSector[] graphicSectors = new graphicSector[SectorsLoader.SECTORS_COUNT];

		public class graphicSector {
			#region Destroy Timer - TODO
			private System.Timers.Timer _destroyTimer = new System.Timers.Timer(30000);

			public bool referenced {
				set {
					if (value) {
						_destroyTimer.Stop();
					} else {
						_destroyTimer.Start();
					}
				}
			}

			private static void OnTimedEvent(object source, System.Timers.ElapsedEventArgs e) {
				graphicSector gs = (graphicSector)source;
				UOConsole.Debug("UPDATE: block {0} is being deallocated.. TODO", gs.sectorID);
			}
			#endregion

			/// <summary>
			/// True if we have loaded all the sprites contained in this sector
			/// </summary>
			public bool fullLoaded = false;
			public GameObject terrain;
			public GameObject[,][] goArray = new GameObject[64, 64][];
			public int sectorID;
			public graphicSector(int _sectorID) {
				sectorID = _sectorID;

				// Hook up the Elapsed event for the timer.
				_destroyTimer.Elapsed += new System.Timers.ElapsedEventHandler(OnTimedEvent);

			}

			/// <summary>
			/// MAIN THREAD
			/// load the already cached sprites into GameObjects. 
			/// This function ignores not-yet loaded sprites.
			/// </summary>
			public void loadObjects(Position p) {
				UOReader.FacetSector fs = UOFacetManager.getSector(sectorID);
				int worldY = (fs.sectorID % 64) * 64;
				int worldX = (fs.sectorID / 64) * 64;

				//Check if the block does not exit yet
				if (statics[fs.sectorID] == null) {
					statics[fs.sectorID] = new GameObject(fs.sectorID.ToString() + " statics");
					statics[fs.sectorID].transform.parent = theMap.transform;
					terrains[fs.sectorID] = buildTerrain(fs.sectorID);
					terrains[fs.sectorID].transform.parent = theMap.transform;
				}

				bool needsAnotherRun = false;//Wheter the SectorLoader thread has not finished yet.
				for (int x = 0; x < fs.tiles.Length; ++x) {
					for (int y = 0; y < fs.tiles[x].Length; ++y) {

						if (Mathf.Abs(worldX + x - p.x) > UPDATE_RANGE || Mathf.Abs(worldY + y - p.y) > UPDATE_RANGE) {
							needsAnotherRun = true;
							continue;
						}
						if (fs.tiles[x][y].staticsCount <= 0)
							continue;

						if (goArray[x, y] == null) {
							goArray[x, y] = new GameObject[fs.tiles[x][y].statics.Length];
						}
								
						for (int i = 0; i < fs.tiles[x][y].statics.Length; ++i) {
							facetStatic_t st = fs.tiles[x][y].statics[i];

							if (facetSprites.ContainsKey(st.graphic)) {
								if (goArray[x, y][i] == null) {
									UOStatic si = facetSprites[st.graphic] as UOStatic;

									if (si == null) {
										facetSprites.Remove(st.graphic);
										UOConsole.Fatal("UPDATE: Removing {0} cause it's null", st.graphic);
									}

									goArray[x, y][i] = si.getDrawItem(x, y, st.z, worldX, worldY);
									goArray[x, y][i].transform.parent = statics[fs.sectorID].transform;
								}
								//Else we already have the tile loaded!
							} else {
								//We need another run
								needsAnotherRun = true;
							}
						}//End statics
					}//End y
				}//End x
				if (!needsAnotherRun) {
					fullLoaded = true;
					UOConsole.Debug("UPDATE: Finished loading {0}", sectorID);
				}
				return;
			}
		}


		/// <summary>
		/// TO BE MOVED
		/// Simply position class 
		/// </summary>
		public class Position{
			public int x;
			public int y;
			public int z;
			public Position(int _x, int _y) :
				this(_x, _y, 0) {
			}
			public Position(int _x, int _y, int _z) {
				x = _x;
				y = _y;
				z = _z;
			}
			/*public static bool operator ==(Position a, Position b){
				return (a.x == b.x) && (a.y == b.y) && (a.z == b.z);
			}*/
		}

	}
}