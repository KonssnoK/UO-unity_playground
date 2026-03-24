# Introduction #

Each sector defines a 64x64 block of the map.

# Inner Extension #
```
build/sectors/facetX/XXXXXXXX.bin
```

# Format #

```
-BYTE	FACETID
-WORD	FILEID
while( 2 ){
	do{
		-BYTE Z									Facet_SUB
		-WORD LANDTILEGraphic	
		-bBYTE	DELIMITERCount
		if(HIBYTE(bBYTE)>0){
			for ( i = 0 ; i < bBYTE; ++i){		
				-dBYTE	DIRECTION					Facet_SUB_SUB
				if(dBYTE <= 7){
					-BYTE	Z
					-DWORD	Graphic
				}
			}
		}
		-cBYTE	STATICSCount
		if(cBYTE>0){
			for ( i = 0 ; i < cBYTE; ++i){
				-DWORD	Graphic						Facet_SUB_SUB_2
				-BYTE	Z
				-DWORD	Color
			}
		}
		++y
	}while( y < 64 )
	++x
	if( x < 64 )
		continue
	break
}
```