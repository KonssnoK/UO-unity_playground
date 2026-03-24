# Introduction #

This function tells informations about a texture, and it's widely used by the other formats.

Used by both Tileart (for static/item textures) and TerrainDefinition (for terrain textures).

# Known Shader Names #

From UOSA.exe RTTI and string analysis:

**Terrain shaders:**
- `UOTerrainShader` — standard terrain rendering
- `UOStaticTerrainShader` — static terrain elements
- `UOWaterShader` — original water shader
- `NewWaterShader` — updated water shader
- `MythicNewWaterShader` — latest Mythic engine water shader

Shader files: `WaterShader.psh` / `WaterShader.vsh`, loaded from `UOShaderLibrary.nl9` / `MythicShaderLibrary.nl9` inside `Shaders.uop`.

**Sprite shaders:**
- `UOSpriteShader` — standard sprite
- `UOSpriteShaderMob` — mobile/creature sprite
- `UOSpriteShaderShadow` — shadow sprite
- `UOSpriteShaderDepthOnly` — depth-only pass
- `UOSpriteUIShader` — UI sprite

**Other shaders:**
- `UOBaseShader`, `UOEffectsShader`, `UOFadeShader`, `UONightMapShader`
- `UOLightingShader`, `UOShadowShader`, `UODeathShader`
- `MythicBaseShader`, `MythicColorShader`, `MythicDepthOnlyShader`
- `MythicShadowMapShader`, `MythicUIDecalShader`

# Texture Slot Mapping #

For water TerrainDefinitions, the texture slots have specific roles:
- Slot 0 (textureSlot=0): DuDv bump/distortion map
- Slot 1 (textureSlot=1): Diffuse base color
- Slot 2 (textureSlot=2): CubeMap for reflections

For wet statics (TileFlag.Wet) in Tileart, the WORLDART texture array also follows this pattern.

# Format #

```

-BYTE	Val					SUB_9_7   (texturePresent — 0=no texture, 1=has texture data)
if( Val != 0 ){
	-BYTE				(texturesCount — number of texture entries)
	-DWORD				-> Shader name IDX in stringDictionary
	-BYTE Count			(actual texture array count)
	if( Count > 0 ){
		do{
			-DWORD		-> StringDictionary Offset  TGA/DDS FILE  (textureIDX)
			-BYTE		-> textureSlot (0, 1, 2...) — determines role in shader pipeline
			-DWORD		-> float TextureRepetition -> if i have a texture with 4x4 square and this is 4 a tile should display a single square
			-DWORD
			-DWORD
		}while(Count-- != 1)
	}
	-DWORD Count
	if( Count > 0 ){
		do{
			-DWORD
		}while(Count-- != 1)
	}
	-DWORD Count
	if( Count > 0 ){
		do{
			-DWORD		-> FLOAT
		}while(Count-- != 1)
	}
}

```
