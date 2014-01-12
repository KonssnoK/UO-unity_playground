using UnityEngine;
using System.Collections;
using System.IO;

namespace UOReader {
	public struct terrainDefinitionAlias{
		public uint countIndex;
		public uint oldAlias;
		public ulong flags;
	};

	public class TerrainDefinition {
		public uint nameIDX;
		public uint index;
		public uint _unk3;
		public uint _unk4;
		public uint _unk5;

		public uint aliasCount;
		public terrainDefinitionAlias[] aliases;
		public TextureInfo textures;

		private TerrainDefinition() {
		}

		public static TerrainDefinition readTerrainDefinition(BinaryReader r) {
			TerrainDefinition td = new TerrainDefinition();

			td.nameIDX = r.ReadUInt32();
			td.index = r.ReadUInt32();
			td._unk3 = r.ReadUInt32();
			td._unk4 = r.ReadUInt32();
			td._unk5 = r.ReadUInt32();

			td.aliasCount = r.ReadUInt32();

			if (td.aliasCount > 0) {
				td.aliases = new terrainDefinitionAlias[td.aliasCount];
				for (uint i = 0; i < td.aliasCount; ++i) {
					td.aliases[i].countIndex = r.ReadUInt32();
					td.aliases[i].oldAlias = r.ReadUInt32();
					td.aliases[i].flags = r.ReadUInt64();
				}
			}

			td.textures = TextureInfo.readTextureInfo(r);

			return td;
		}

		//End
	}

}