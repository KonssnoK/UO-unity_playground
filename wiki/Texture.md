# Introduction #

This function tells informations about a texture, and it's widely used by the other formats.
I really need help with this. :)


# Format #

```

-BYTE	Val					SUB_9_7
if( Val != 0 ){
	-BYTE
	-DWORD				-> Shader
	-BYTE Count
	if( Count > 0 ){
		do{
			-DWORD		-> StringDictionary Offset  TGA/DDS FILE
			-BYTE
			-DWORD		-> float TextureRepetition -> if i have a texture with 4x4 square and this is 4  a tile should display a single square
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