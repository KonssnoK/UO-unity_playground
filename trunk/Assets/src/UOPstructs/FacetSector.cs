using UnityEngine;
using System.Collections;
using System.IO;

namespace UOReader {
	public struct facetDelimiter_t {
		public byte direction;
		public sbyte z;
		public uint graphic;
	};

	public struct facetStatic_t {
		public uint graphic;
		public sbyte z;
		public uint color;
	};

	public struct facetTile_t {
		public sbyte z;
		public ushort landtileGraphic;
		public byte delimitersCount;
		public facetDelimiter_t[] delimiters;
		public byte staticsCount;
		public facetStatic_t[] statics;
	}

	public class FacetSector {
		public byte facetID;
		public ushort sectorID;
		public facetTile_t[][] tiles = new facetTile_t[64][];

		private FacetSector() {
		}

		public static FacetSector readSector(BinaryReader r) {
			FacetSector fs = new FacetSector();
			fs.facetID = r.ReadByte();
			fs.sectorID = r.ReadUInt16();

			for (int x = 0; x < 64; ++x) {
				fs.tiles[x] = new facetTile_t[64];
				for (int y = 0; y < 64; ++y) {
					fs.tiles[x][y].z = r.ReadSByte();
					fs.tiles[x][y].landtileGraphic = r.ReadUInt16();
					fs.tiles[x][y].delimitersCount = r.ReadByte();
					if (fs.tiles[x][y].delimitersCount > 0) {
						fs.tiles[x][y].delimiters = new facetDelimiter_t[fs.tiles[x][y].delimitersCount];
						for (int i = 0; i < fs.tiles[x][y].delimitersCount; ++i) {
							fs.tiles[x][y].delimiters[i].direction = r.ReadByte();
							if (fs.tiles[x][y].delimiters[i].direction < 8) {
								fs.tiles[x][y].delimiters[i].z = r.ReadSByte();
								fs.tiles[x][y].delimiters[i].graphic = r.ReadUInt32();
							}
						}
					}
					fs.tiles[x][y].staticsCount = r.ReadByte();
					if (fs.tiles[x][y].staticsCount > 0) {
						fs.tiles[x][y].statics = new facetStatic_t[fs.tiles[x][y].staticsCount];
						for (int i = 0; i < fs.tiles[x][y].staticsCount; ++i) {
							fs.tiles[x][y].statics[i].graphic = r.ReadUInt32();
							fs.tiles[x][y].statics[i].z = r.ReadSByte();
							fs.tiles[x][y].statics[i].color = r.ReadUInt32();
						}
					}
				}
			}

			return fs;
		}
	}
}