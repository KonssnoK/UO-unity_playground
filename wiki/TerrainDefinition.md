# Description #

Those files are used to map old Legacy terrain informations to the new texture terrain.

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