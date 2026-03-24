using Mythic.Package;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Text;
using UOReader;

namespace UOResources {
	public class UOResourceManager {

		private const string fileDirectory = "Assets\\UOPs\\";

		#region Structures
		private struct stringDictionary_t {
			public ulong unk64;
			public uint count;
			public short unk16;
			public string[] values;
		};
		public struct uopMapping_t {
			public int block;
			public int file;
			public uopMapping_t(int b, int f) {
				block = b;
				file = f;
			}
		};
		private struct legacyTerrainMap_t {
			public uint legacyID;
			public uint newID;
			public uint newSubtype;
			public legacyTerrainMap_t(uint lid, uint nid, uint nst) {
				legacyID = lid;
				newID = nid;
				newSubtype = nst;
			}
		};
		#endregion

		public struct uopHashes_t {
			//Contain all known hashes and relative positioning in uop
			public Dictionary<ulong, uopMapping_t> tileartHashes;//tileart.uop
			public Dictionary<ulong, uopMapping_t> textureHashes;//texture.uop
			public Dictionary<ulong, uopMapping_t> terrainHashes;//TerrainDefinition.uop
			public Dictionary<ulong, uopMapping_t> facet0Hashes;//facet0.uop
			public Dictionary<ulong, uopMapping_t> legacyTexturesHashes;//LegacyTexture.uop
		};

		public static uopHashes_t uopHashes;
		//Contains all known string ID and relative string
		private static stringDictionary_t stringDictionary;
		//Used for FAST already loaded textures reading
		private static ConcurrentDictionary<uint, UOResource> textures = new ConcurrentDictionary<uint,UOResource>();
		private static ConcurrentDictionary<uint, UOResource> legacyTextures = new ConcurrentDictionary<uint, UOResource>();
		//Given a landtile legacy ID returns a texture ID
		private static ConcurrentDictionary<uint, TextureImageInfo> landtiles = new ConcurrentDictionary<uint, TextureImageInfo>();
		//Given a landtile legacy ID returns the shader name index from its TerrainDefinition
		private static ConcurrentDictionary<uint, int> landtileShaderIdx = new ConcurrentDictionary<uint, int>();
		//legacyterrainmap -> given a legacy landtile id, returns a struct
		private static Dictionary<uint, legacyTerrainMap_t> legacyTerrainMap = new Dictionary<uint, legacyTerrainMap_t>();
		//tileart
		private static ConcurrentDictionary<uint, Tileart> tileartCollection = new ConcurrentDictionary<uint, Tileart>();

		//Preload all hashes
		public static bool loadUOPs(){

			//Load the string dictionary data
			MythicPackage sd = MythicPackageCache.Get(fileDirectory + "string_dictionary.uop");
			byte[] data = sd.Blocks[0].Files[0].Unpack(sd.FileInfo.FullName);
			using (MemoryStream fs = new MemoryStream(data)) {
				using (BinaryReader r = new BinaryReader(fs)) {
					stringDictionary.unk64 = r.ReadUInt64();
					stringDictionary.count = r.ReadUInt32();
					stringDictionary.unk16 = r.ReadInt16();

					stringDictionary.values = new string[stringDictionary.count];
					for (int i = 0; i < stringDictionary.count; ++i) {
						ushort len = r.ReadUInt16();
						byte[] datas = r.ReadBytes(len);
						stringDictionary.values[i]= UTF8Encoding.ASCII.GetString(datas);
					}
				}
			}

			//Load the map conversion between new ids and legacy ones
			using (FileStream fs = new FileStream(fileDirectory + "legacyterrainmap.csv", FileMode.Open)) {
				using (StreamReader r = new StreamReader(fs)) {
					string line = r.ReadLine();//legacy newid newsub
					while(true) {
						line = r.ReadLine();
						if(line == null)
							break;

						string[] values = line.Split(',');
						if(values.Length != 3){
							UOConsole.Fatal("cannot read legacyterrainmap.csv");
							return false;
						}
						legacyTerrainMap[uint.Parse(values[0])] = new legacyTerrainMap_t(uint.Parse(values[0]), uint.Parse(values[1]), uint.Parse(values[2]));
					}
				}
			}

			//Now build files dictionaries for fast searching
			uopHashes.tileartHashes = new Dictionary<ulong, uopMapping_t>();
			uopHashes.textureHashes = new Dictionary<ulong, uopMapping_t>();
			uopHashes.terrainHashes = new Dictionary<ulong, uopMapping_t>();
			uopHashes.facet0Hashes = new Dictionary<ulong, uopMapping_t>();
			uopHashes.legacyTexturesHashes = new Dictionary<ulong, uopMapping_t>();

			MythicPackage _uop = MythicPackageCache.Get(fileDirectory + "tileart.uop");
			for (int i = 0; i < _uop.Blocks.Count; ++i) {
				for (int j = 0; j < _uop.Blocks[i].Files.Count; ++j) {
					uopHashes.tileartHashes.Add(_uop.Blocks[i].Files[j].FileHash, new uopMapping_t(i, j));
				}
			}

			_uop = MythicPackageCache.Get(fileDirectory + "Texture.uop");
			for (int i = 0; i < _uop.Blocks.Count; ++i) {
				for (int j = 0; j < _uop.Blocks[i].Files.Count; ++j) {
					uopHashes.textureHashes.Add(_uop.Blocks[i].Files[j].FileHash, new uopMapping_t(i, j));
				}
			}

			_uop = MythicPackageCache.Get(fileDirectory + "TerrainDefinition.uop");
			for (int i = 0; i < _uop.Blocks.Count; ++i) {
				for (int j = 0; j < _uop.Blocks[i].Files.Count; ++j) {
					uopHashes.terrainHashes.Add(_uop.Blocks[i].Files[j].FileHash, new uopMapping_t(i, j));
				}
			}

			_uop = MythicPackageCache.Get(fileDirectory + "facet0.uop");
			for (int i = 0; i < _uop.Blocks.Count; ++i) {
				for (int j = 0; j < _uop.Blocks[i].Files.Count; ++j) {
					uopHashes.facet0Hashes.Add(_uop.Blocks[i].Files[j].FileHash, new uopMapping_t(i, j));
				}
			}

			_uop = MythicPackageCache.Get(fileDirectory + "LegacyTexture.uop");
			for (int i = 0; i < _uop.Blocks.Count; ++i) {
				for (int j = 0; j < _uop.Blocks[i].Files.Count; ++j) {
					uopHashes.legacyTexturesHashes.Add(_uop.Blocks[i].Files[j].FileHash, new uopMapping_t(i, j));
				}
			}

			return true;
		}

		//Get a resource given an id
		// the id is coming from	TILEART -> TEXTURES 
		//					or		TERRAINDEF -> TEXTURES
		public static UOResource getResource( Tileart tileart ){
			if (tileart == null || tileart.textures == null) {
				UOConsole.Fatal("getResource: tileart or textures is null");
				return null;
			}

			UOResource resource = null;

			//WorldArt Texture
			if (tileart.textures[0] != null && tileart.textures[0].texturePresent == 1) {
				// For water statics (Wet flag), pick the diffuse texture (textureSlot=1)
				// instead of texturesArray[0] which is the alpha/normal map
				TextureImageInfo texInfo = tileart.textures[0].texturesArray[0];
				if ((tileart.flags & TileFlag.Wet) != 0 && tileart.textures[0].texturesCount > 1) {
					for (int ti = 0; ti < tileart.textures[0].texturesCount; ti++) {
						if (tileart.textures[0].texturesArray[ti].textureSlot == 1) {
							texInfo = tileart.textures[0].texturesArray[ti];
							break;
						}
					}
				}
				resource = getResource(texInfo, ShaderTypes.Sprite);
			}
			//LegacyTexture
			if (resource == null && tileart.textures[1] != null && tileart.textures[1].texturePresent == 1) {
				resource = getLegacyResource(tileart.textures[1].texturesArray[0]);
			}
			//EnhancedTexture — needed for water statics and other items without WorldArt/Legacy
			if (resource == null && tileart.textures[2] != null && tileart.textures[2].texturePresent == 1) {
				resource = getResource(tileart.textures[2].texturesArray[0], ShaderTypes.Sprite);
			}
			//Light Texture
			if (resource != null && tileart.textures[3] != null && tileart.textures[3].texturePresent == 1) {
				//TODO: light texture load
			}
			//
			if (resource == null){
				// Items with no textures at all (incomplete tileart parse) — use water placeholder
				bool allSlotsNull = (tileart.textures[0] == null || tileart.textures[0].texturePresent == 0)
					&& (tileart.textures[1] == null || tileart.textures[1].texturePresent == 0)
					&& (tileart.textures[2] == null || tileart.textures[2].texturePresent == 0);
				if (allSlotsNull) {
					UOConsole.Debug("static {0} no textures (flags=0x{1:X}) using water placeholder", tileart.id, (ulong)tileart.flags);
					return UOResource.WaterResource;
				}
				// Has texture slots but loading failed — log details
				UOConsole.Fatal("static {0} texture LOAD FAILED (flags=0x{1:X}) WA_present={2} Leg_present={3} Enh_present={4}",
					tileart.id, (ulong)tileart.flags,
					tileart.textures[0] != null ? tileart.textures[0].texturePresent : -1,
					tileart.textures[1] != null ? tileart.textures[1].texturePresent : -1,
					tileart.textures[2] != null ? tileart.textures[2].texturePresent : -1);
				// Log what textureIDX they reference
				if (tileart.textures[0] != null && tileart.textures[0].texturePresent == 1 && tileart.textures[0].texturesArray != null)
					UOConsole.Fatal("  WA[0] textureIDX={0}", tileart.textures[0].texturesArray[0].textureIDX);
				if (tileart.textures[1] != null && tileart.textures[1].texturePresent == 1 && tileart.textures[1].texturesArray != null)
					UOConsole.Fatal("  Leg[0] textureIDX={0}", tileart.textures[1].texturesArray[0].textureIDX);
				if (tileart.textures[2] != null && tileart.textures[2].texturePresent == 1 && tileart.textures[2].texturesArray != null)
					UOConsole.Fatal("  Enh[0] textureIDX={0}", tileart.textures[2].texturesArray[0].textureIDX);
			}

			return resource;
		}

		public static UOResource getResource(TextureImageInfo tileartTextureInfo, ShaderTypes stype) {
			//FAST search
			if (textures.TryGetValue(tileartTextureInfo.textureIDX, out UOResource cachedTex)) {
				return cachedTex;
			}

			//Get the string from stringDictionary
			if (tileartTextureInfo.textureIDX >= stringDictionary.count) {
				UOConsole.Fatal("String {0} not found in dictionary.", tileartTextureInfo.textureIDX);
				return null;
			}
			string tga = stringDictionary.values[tileartTextureInfo.textureIDX];

			//Replace extension
			int start = (tga.LastIndexOf("\\") == -1) ? 0 : (tga.LastIndexOf("\\") + 1);
			int end = tga.IndexOf("_");
			if (end == -1) {
				UOConsole.Debug("no descr in: {0} .. trying with extension", tga);
				tga = tga.Replace(".tga","");
				end = tga.Length;
			}
			//UOConsole.Fatal("{0} {1} {2}", tga, start, end);
			string toHash = tga.Substring(start, end - start) + ".dds";
			toHash = toHash.ToLower();
			toHash = "build/worldart/" + toHash;

			//Get the file from Texture.uop
			ulong tehHash = HashDictionary.HashFileName(toHash);
			if (!uopHashes.textureHashes.ContainsKey(tehHash)) {
				UOConsole.Fatal("string {0} not found in textureHashes - tga: {1}", toHash, tga);
				return null;
			}

			uopMapping_t map = uopHashes.textureHashes[tehHash];
			MythicPackage tex = MythicPackageCache.Get(fileDirectory + "texture.uop");
			byte[] raw = tex.Blocks[map.block].Files[map.file].Unpack(tex.FileInfo.FullName);
			UOResource res = new UOResource(raw, stype);

			textures.TryAdd(tileartTextureInfo.textureIDX, res);
			return res;
		}

		
		public static UOResource getLegacyResource(TextureImageInfo tileartTextureInfo) {
			//FAST search
			if (legacyTextures.TryGetValue(tileartTextureInfo.textureIDX, out UOResource cachedLeg)) {
				return cachedLeg;
			}

			//Get the string from stringDictionary
			if (tileartTextureInfo.textureIDX >= stringDictionary.count) {
				UOConsole.Fatal("String {0} not found in dictionary.", tileartTextureInfo.textureIDX);
				return null;
			}
			string tga = stringDictionary.values[tileartTextureInfo.textureIDX];

			//Replace extension
			int start = (tga.LastIndexOf("\\") == -1) ? 0 : (tga.LastIndexOf("\\") + 1);
			int end = tga.IndexOf("_");
			if (end == -1) {
				UOConsole.Debug("no descr in: {0} .. trying with extension", tga);
				tga = tga.Replace(".tga", "");
				end = tga.Length;
			}
			//UOConsole.Fatal("{0} {1} {2}", tga, start, end);
			string toHash = tga.Substring(start, end - start);
			while(toHash.Length < 8)//Filling the missing zeros
				toHash = "0" + toHash;
			toHash += ".dds";
			toHash = toHash.ToLower();
			toHash = "build/tileartlegacy/" + toHash;

			//Get the file from Texture.uop
			ulong tehHash = HashDictionary.HashFileName(toHash);
			if (!uopHashes.legacyTexturesHashes.ContainsKey(tehHash)) {
				UOConsole.Fatal("string {0} not found in legacyTextureHashes - tga: {1}", toHash, tga);
				return null;
			}

			uopMapping_t map = uopHashes.legacyTexturesHashes[tehHash];
			MythicPackage tex = MythicPackageCache.Get(fileDirectory + "LegacyTexture.uop");
			byte[] raw = tex.Blocks[map.block].Files[map.file].Unpack(tex.FileInfo.FullName);
			UOResource res = new UOResource(raw, ShaderTypes.Sprite, true);

			legacyTextures.TryAdd(tileartTextureInfo.textureIDX, res);
			return res;
		}

		//Land tiles does not have tileart TEXTURES section.. we need to extract them from terrain definition
		public static TextureImageInfo getLandtileTextureID(uint legacyLandtileID){
			//Fast search
			if(landtiles.TryGetValue(legacyLandtileID, out TextureImageInfo cachedLand)){
				return cachedLand;
			}

			//Translate the legacy ID to the new pair newID-subtype using legacyterrainMap
			if (!legacyTerrainMap.ContainsKey(legacyLandtileID)) {
				UOConsole.Fatal("Cannot find {0} in legacyTerrainMap", legacyLandtileID);
				return null;
			}
			legacyTerrainMap_t landtileID = legacyTerrainMap[legacyLandtileID];

			//Get the file from terrain definition using the newID
			ulong hash = HashDictionary.HashFileName(string.Format("build/terraindefinition/{0}.bin", landtileID.newID));

			if (!uopHashes.terrainHashes.ContainsKey(hash)) {
				UOConsole.Fatal("Cannot find {0} in terrainHashes", landtileID.newID);
				return null;
			}
			uopMapping_t pos = uopHashes.terrainHashes[hash];

			MythicPackage _uop = MythicPackageCache.Get(fileDirectory + "TerrainDefinition.uop");
			byte[] raw = _uop.Blocks[pos.block].Files[pos.file].Unpack(_uop.FileInfo.FullName);

			//Read the loaded terrainDefinition file.
			TerrainDefinition td;
			using (MemoryStream ms = new MemoryStream(raw)) {
				using (BinaryReader r = new BinaryReader(ms)) {
					td = TerrainDefinition.readTerrainDefinition(r);
				}
			}
			if (td == null){
				UOConsole.Fatal("Cannot read terrainDefinition file");
				return null;
			}

			landtiles.TryAdd(legacyLandtileID, td.textures.texturesArray[landtileID.newSubtype]);
			landtileShaderIdx.TryAdd(legacyLandtileID, td.textures.shaderNameIDX);

			//Returns the texture according to subtype
			return td.textures.texturesArray[landtileID.newSubtype];
		}

		/// <summary>
		/// Returns the full TerrainDefinition for a landtile (for debugging/inspection)
		/// </summary>
		public static TerrainDefinition getTerrainDefinition(uint legacyLandtileID) {
			if (!legacyTerrainMap.ContainsKey(legacyLandtileID))
				return null;
			legacyTerrainMap_t landtileID = legacyTerrainMap[legacyLandtileID];
			ulong hash = HashDictionary.HashFileName(string.Format("build/terraindefinition/{0}.bin", landtileID.newID));
			if (!uopHashes.terrainHashes.ContainsKey(hash))
				return null;
			uopMapping_t pos = uopHashes.terrainHashes[hash];
			MythicPackage _uop = MythicPackageCache.Get(fileDirectory + "TerrainDefinition.uop");
			byte[] raw = _uop.Blocks[pos.block].Files[pos.file].Unpack(_uop.FileInfo.FullName);
			using (MemoryStream ms = new MemoryStream(raw)) {
				using (BinaryReader r = new BinaryReader(ms)) {
					return TerrainDefinition.readTerrainDefinition(r);
				}
			}
		}

		/// <summary>
		/// Returns the subtype index from legacyTerrainMap for a landtile
		/// </summary>
		public static int getLandtileSubtype(uint legacyLandtileID) {
			if (!legacyTerrainMap.ContainsKey(legacyLandtileID))
				return -1;
			return (int)legacyTerrainMap[legacyLandtileID].newSubtype;
		}

		/// <summary>
		/// Resolves a string dictionary index to its string value
		/// </summary>
		public static string getStringDictValue(uint idx) {
			if (idx >= stringDictionary.count) return null;
			return stringDictionary.values[idx];
		}

		/// <summary>
		/// Returns the shader name string for a landtile, looked up from string dictionary
		/// </summary>
		public static string getLandtileShaderName(uint legacyLandtileID) {
			if (!landtileShaderIdx.TryGetValue(legacyLandtileID, out int idx))
				return null;
			if (idx < 0 || idx >= stringDictionary.count)
				return null;
			return stringDictionary.values[idx];
		}

		//Get a tileart given a graphic id
		public static Tileart getTileart(uint graphic) {
			//Fast search
			if (tileartCollection.TryGetValue(graphic, out Tileart cachedTa)) {
				return cachedTa;
			}

			//Get the file from tileart using the id
			ulong hash = HashDictionary.HashFileName(string.Format("build/tileart/{0:D8}.bin", graphic));

			if (!uopHashes.tileartHashes.ContainsKey(hash)) {
				UOConsole.Fatal("Cannot find {0} in tileartHashes", graphic);
				return null;
			}
			uopMapping_t pos = uopHashes.tileartHashes[hash];

			MythicPackage _uop = MythicPackageCache.Get(fileDirectory + "tileart.uop");
			byte[] raw = _uop.Blocks[pos.block].Files[pos.file].Unpack(_uop.FileInfo.FullName);

			//Read the loaded tileart file.
			Tileart t;
			using (MemoryStream ms = new MemoryStream(raw)) {
				using (BinaryReader r = new BinaryReader(ms)) {
					t = Tileart.readTileart(r);
				}
			}
			if (t == null) {
				UOConsole.Fatal("Cannot read tileart file");
				return t;
			}

			tileartCollection.TryAdd(graphic, t);

			//Returns the texture according to subtype
			return t;
		}
	}
}