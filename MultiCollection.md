# Description #

Multi Collection contains all the multis, which are a collection of tiles.

# Inner Extension #
```
.bin
```

# Format #

```
-DWORD 
-DWORD Count
do{
	-WORD 	Graphic
	-WORD 	X
	-WORD 	Y
	-WORD 	Z
	-BYTE		unknown Bool
	-BYTE		unknown Bool
	-DWORD 	SubCount
	if( SubCount > 0 )
		do{
			-DWORD		->StringDictionary Offset
		}while(SubCount-- != 1)
}while(	Count-- )
```