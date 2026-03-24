# Description #

Those files are used to map old Legacy terrain informations to the new texture terrain.

The Enhanced Client uses a layered terrain system with these terrain layer types (from RTTI in UOSA.exe):
- `IUOTerrainLayer` — interface
- `UOBaseTerrainLayer` — base implementation
- `UODefaultTerrainLayer` — standard land terrain
- `UOWaterTerrainLayer` — water terrain (rendered separately with water shader)
- `UOBumpMapTerrainLayer` — bump-mapped terrain

Water terrain definitions have 3 texture slots:
- textureSlot 0: DuDv bump/distortion map (e.g. `water_alpha.tga`, rep=16)
- textureSlot 1: Diffuse base color (e.g. `water.tga`, rep=4)
- textureSlot 2: CubeMap for reflections (e.g. `cube3.tga`, rep=1)

Terrain definitions are associated with shaders via the Shader field in TEXTURES():
- `UOTerrainShader` — standard terrain
- `UOStaticTerrainShader` — static terrain elements
- `UOWaterShader` / `NewWaterShader` / `MythicNewWaterShader` — water terrain

# Inner Extension #

```
.bin
```

# Format #

```
-DWORD		nameIDX in stringDictionary
-DWORD		ID
-DWORD
-DWORD
-DWORD

-DWORD		Count						SUB_11
if( Count > 0 ){
	do{
		-DWORD		CountIndex
		-DWORD		OLD ALIAS ? (Example: Cobblestone 1001)
		-QWORD		Flags
	}while(Count-- != 1)
}
call TEXTURES()
```
