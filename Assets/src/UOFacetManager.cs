using System.Collections.Concurrent;
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

		public class facetSectorMesh{
			public Vector3[] vertices;
			public int[] triangles;
			public Vector3[] normals;
			public Vector2[] uvs;
			public Material terrainMaterial;
			public facetSectorMesh() {
			}
		};


		private const string fileDirectory = "Assets\\UOPs\\";


		private static ConcurrentDictionary<int, FacetSector> facetSectors = new ConcurrentDictionary<int, FacetSector>();
		private static ConcurrentDictionary<uint, UOSprite> facetSprites = new ConcurrentDictionary<uint, UOSprite>();

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
			if(facetSectors.TryGetValue(sector, out FacetSector cached))
				return cached;

			int currentFacet = 0;
			//Look for the file in facet hashes
			string toHash = string.Format("build/sectors/facet_{0:D2}/{1:D8}.bin", currentFacet , sector);
			ulong hash = HashDictionary.HashFileName(toHash);

			if(!UOResourceManager.uopHashes.facet0Hashes.ContainsKey(hash)){
				UOConsole.Fatal("Cannot find {0} in facet0Hashes", toHash);
				return null;
			}
			UOResourceManager.uopMapping_t map = UOResourceManager.uopHashes.facet0Hashes[hash];

			MythicPackage _uop = MythicPackageCache.Get(fileDirectory + "facet0.uop");
			byte[] raw = _uop.Blocks[map.block].Files[map.file].Unpack(_uop.FileInfo.FullName);

			FacetSector fs;

			using(MemoryStream ms = new MemoryStream(raw)){
				using (BinaryReader r = new BinaryReader(ms)) {
					fs = FacetSector.readSector(r);
				}
			}

			facetSectors.TryAdd(sector, fs);
			return fs;
		}

		/// <summary>
		/// Silent version of getSector — returns null without logging if sector doesn't exist
		/// </summary>
		private static FacetSector tryGetSector(int sectorID) {
			if (sectorID < 0) return null;
			if (facetSectors.TryGetValue(sectorID, out FacetSector cached))
				return cached;
			int currentFacet = 0;
			string toHash = string.Format("build/sectors/facet_{0:D2}/{1:D8}.bin", currentFacet, sectorID);
			ulong hash = HashDictionary.HashFileName(toHash);
			if (!UOResourceManager.uopHashes.facet0Hashes.ContainsKey(hash))
				return null;
			return getSector(sectorID);
		}

		/// <summary>
		/// Add a texture to the collection if not already present; return its array index
		/// </summary>
		private static int addTexInfo(TextureImageInfo info, Dictionary<uint, int> map, List<TextureImageInfo> list) {
			if (info == null) return 0;
			int idx;
			if (!map.TryGetValue(info.textureIDX, out idx)) {
				idx = list.Count;
				map[info.textureIDX] = idx;
				list.Add(info);
			}
			return idx;
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

			mesh.vertices = m.vertices;
			mesh.normals = m.normals;
			mesh.uv = m.uvs;
			mesh.triangles = m.triangles;

			mf.mesh = mesh;
			if (m.terrainMaterial != null)
				mr.material = m.terrainMaterial;
			else
				mr.material = new Material(Shader.Find("Diffuse"));

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

			const int GRID = 65; // 65x65 shared vertices for 64x64 tiles
			const float Z_SCALE = 6f / UOSprite.UOEC_SIZE;

			// Build Z grid — vertex(gx,gy) gets Z from tiles[gx-1][gy-1]
			float[,] zGrid = new float[GRID, GRID];
			for (int gx = 1; gx < GRID; gx++)
				for (int gy = 1; gy < GRID; gy++)
					zGrid[gx, gy] = fs.tiles[gx - 1][gy - 1].z * Z_SCALE;
			for (int g = 1; g < GRID; g++) {
				zGrid[0, g] = zGrid[1, g];
				zGrid[g, 0] = zGrid[g, 1];
			}
			zGrid[0, 0] = zGrid[1, 1];

			// Create shared vertex grid
			int vertCount = GRID * GRID;
			mesh.vertices = new Vector3[vertCount];
			mesh.normals = new Vector3[vertCount];
			mesh.uvs = new Vector2[vertCount];

			for (int gx = 0; gx < GRID; gx++) {
				for (int gy = 0; gy < GRID; gy++) {
					int idx = gx * GRID + gy;
					float z = zGrid[gx, gy];
					int px = gx + worldX;
					int py = gy + worldY;
					mesh.vertices[idx] = new Vector3(px - z, -py + z, 100 - z);
					mesh.normals[idx] = Vector3.up;
					mesh.uvs[idx] = new Vector2(gx, gy);
				}
			}

			// Collect unique textures and build tile→index mapping
			Dictionary<uint, int> texIdxMap = new Dictionary<uint, int>();
			List<TextureImageInfo> uniqueTexInfos = new List<TextureImageInfo>();
			int[,] tileTexIdx = new int[64, 64];

			for (int x = 0; x < 64; x++) {
				for (int y = 0; y < 64; y++) {
					TextureImageInfo info = UOResourceManager.getLandtileTextureID(fs.tiles[x][y].landtileGraphic);
					if (info == null) {
						tileTexIdx[x, y] = 0;
						continue;
					}
					int arrayIdx;
					if (!texIdxMap.TryGetValue(info.textureIDX, out arrayIdx)) {
						arrayIdx = uniqueTexInfos.Count;
						texIdxMap[info.textureIDX] = arrayIdx;
						uniqueTexInfos.Add(info);
					}
					tileTexIdx[x, y] = arrayIdx;
				}
			}

			// Build single triangle list (no submeshes)
			int[] triangles = new int[64 * 64 * 6];
			int ti = 0;
			for (int x = 0; x < 64; x++) {
				for (int y = 0; y < 64; y++) {
					int v0 = x * GRID + y;
					int v1 = (x + 1) * GRID + y;
					int v2 = x * GRID + (y + 1);
					int v3 = (x + 1) * GRID + (y + 1);
					triangles[ti++] = v0; triangles[ti++] = v3; triangles[ti++] = v2;
					triangles[ti++] = v0; triangles[ti++] = v1; triangles[ti++] = v3;
				}
			}
			mesh.triangles = triangles;

			// Build 66x66 expanded index map — includes 1-pixel border from neighbor sectors
			const int MAP_SIZE = 66;
			byte[] indexData = new byte[MAP_SIZE * MAP_SIZE];

			// Center 64x64 (at offset +1,+1)
			for (int x = 0; x < 64; x++)
				for (int y = 0; y < 64; y++)
					indexData[(y + 1) * MAP_SIZE + (x + 1)] = (byte)tileTexIdx[x, y];

			// Load neighbor sectors for border blending
			int sid = fs.sectorID;
			FacetSector secLeft = tryGetSector(sid - 64);
			FacetSector secRight = tryGetSector(sid + 64);
			FacetSector secUp = tryGetSector(sid - 1);
			FacetSector secDown = tryGetSector(sid + 1);

			// Left border (expanded x=0): neighbor's column 63
			for (int y = 0; y < 64; y++) {
				if (secLeft != null) {
					TextureImageInfo info = UOResourceManager.getLandtileTextureID(secLeft.tiles[63][y].landtileGraphic);
					indexData[(y + 1) * MAP_SIZE + 0] = (byte)addTexInfo(info, texIdxMap, uniqueTexInfos);
				} else {
					indexData[(y + 1) * MAP_SIZE + 0] = indexData[(y + 1) * MAP_SIZE + 1];
				}
			}
			// Right border (expanded x=65): neighbor's column 0
			for (int y = 0; y < 64; y++) {
				if (secRight != null) {
					TextureImageInfo info = UOResourceManager.getLandtileTextureID(secRight.tiles[0][y].landtileGraphic);
					indexData[(y + 1) * MAP_SIZE + 65] = (byte)addTexInfo(info, texIdxMap, uniqueTexInfos);
				} else {
					indexData[(y + 1) * MAP_SIZE + 65] = indexData[(y + 1) * MAP_SIZE + 64];
				}
			}
			// Top border (expanded y=0): neighbor's row 63
			for (int x = 0; x < 64; x++) {
				if (secUp != null) {
					TextureImageInfo info = UOResourceManager.getLandtileTextureID(secUp.tiles[x][63].landtileGraphic);
					indexData[0 * MAP_SIZE + (x + 1)] = (byte)addTexInfo(info, texIdxMap, uniqueTexInfos);
				} else {
					indexData[0 * MAP_SIZE + (x + 1)] = indexData[1 * MAP_SIZE + (x + 1)];
				}
			}
			// Bottom border (expanded y=65): neighbor's row 0
			for (int x = 0; x < 64; x++) {
				if (secDown != null) {
					TextureImageInfo info = UOResourceManager.getLandtileTextureID(secDown.tiles[x][0].landtileGraphic);
					indexData[65 * MAP_SIZE + (x + 1)] = (byte)addTexInfo(info, texIdxMap, uniqueTexInfos);
				} else {
					indexData[65 * MAP_SIZE + (x + 1)] = indexData[64 * MAP_SIZE + (x + 1)];
				}
			}
			// Corners: repeat nearest edge
			indexData[0] = indexData[1];
			indexData[65] = indexData[64];
			indexData[65 * MAP_SIZE] = indexData[65 * MAP_SIZE + 1];
			indexData[65 * MAP_SIZE + 65] = indexData[65 * MAP_SIZE + 64];

			// Now build Texture2DArray with ALL collected textures (including neighbor ones)
			if (uniqueTexInfos.Count > 0) {
				const int TARGET_SIZE = 256;

				Texture2DArray texArray = new Texture2DArray(TARGET_SIZE, TARGET_SIZE, uniqueTexInfos.Count, TextureFormat.RGBA32, false);
				texArray.wrapMode = TextureWrapMode.Repeat;
				texArray.filterMode = FilterMode.Bilinear;

				for (int i = 0; i < uniqueTexInfos.Count; i++) {
					UOResource res = UOResourceManager.getResource(uniqueTexInfos[i], ShaderTypes.Terrain);
					Texture2D srcTex = res.getTexture();

					RenderTexture rt = RenderTexture.GetTemporary(TARGET_SIZE, TARGET_SIZE, 0, RenderTextureFormat.ARGB32);
					Graphics.Blit(srcTex, rt);
					RenderTexture prev = RenderTexture.active;
					RenderTexture.active = rt;
					Texture2D resized = new Texture2D(TARGET_SIZE, TARGET_SIZE, TextureFormat.RGBA32, false);
					resized.ReadPixels(new Rect(0, 0, TARGET_SIZE, TARGET_SIZE), 0, 0);
					resized.Apply();
					RenderTexture.active = prev;
					RenderTexture.ReleaseTemporary(rt);

					texArray.SetPixelData(resized.GetRawTextureData<byte>(), 0, i);
					Object.Destroy(resized);
				}
				texArray.Apply(false);

				// Create index map texture (66x66)
				Texture2D indexMap = new Texture2D(MAP_SIZE, MAP_SIZE, TextureFormat.R8, false);
				indexMap.filterMode = FilterMode.Point;
				indexMap.wrapMode = TextureWrapMode.Clamp;
				indexMap.LoadRawTextureData(indexData);
				indexMap.Apply(false);

				// Per-texture repetition array (padded to 64)
				float[] repsArray = new float[64];
				for (int i = 0; i < uniqueTexInfos.Count && i < 64; i++) {
					float rep = uniqueTexInfos[i].repetition;
					repsArray[i] = (rep > 0) ? (1.0f / rep) : 0.25f;
				}

				// Create material
				Shader shader = Shader.Find("UO/TerrainBlend");
				if (shader == null) {
					UOConsole.Fatal("UO/TerrainBlend shader not found");
					shader = Shader.Find("Diffuse");
				}
				Material mat = new Material(shader);
				mat.SetTexture("_TerrainTextures", texArray);
				mat.SetTexture("_TileIndexMap", indexMap);
				mat.SetFloat("_Repetition", 0.25f);
				mat.SetFloat("_BlendWidth", 0.5f);
				mat.SetFloatArray("_Repetitions", repsArray);
				mesh.terrainMaterial = mat;

				UOConsole.Debug("terrain: {0} unique textures packed into array", uniqueTexInfos.Count);
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
							if (facetSprites.TryAdd(st.graphic, new UOStatic(st.graphic)))
								totalStaticsSingle++;
						}

						totalStatics++;
					}
				}
			}

			// Preload terrain texture IDs on background thread so buildTerrainMesh() hits cache
			for (int x2 = 0; x2 < fs.tiles.Length; ++x2)
				for (int y2 = 0; y2 < fs.tiles[x2].Length; ++y2)
					UOResourceManager.getLandtileTextureID(fs.tiles[x2][y2].landtileGraphic);

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
										facetSprites.TryRemove(st.graphic, out _);
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