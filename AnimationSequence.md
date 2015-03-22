# Description #

This format is currently unknown.


# Format #
```

-DWORD
do{
	-BYTE
	-BYTE
}while(v9^v10)
do{
	-WORD
	-WORD
}while(v15^v16)
-DWORD Count
if( Count > 0 ){
	do{
		-DWORD Iteration
		-DWORD
		-DWORD
		-DWORD
		do{
			-BYTE
			-BYTE
		}while(v28^v29)
		do{
			-WORD	
			-WORD
		}while(v34^v35)
		-DWORD SubCount
		if( SubCount > 0 ){
			do{
				-DWORD
				-DWORD XCount							SUB_8
				if( XCount > 0 ){
					do{
						-DWORD							4_6_30_Sub
						
						FUNCTION
						
					}while( XCount-- != 1) 
				}
			}while(SubCount-- != 1)
		}
		-DWORD SubCount
		if( SubCount > 0 ){
			do{
				-DWORD
			}while(SubCount-- != 1)
		}

	}while(Count-- != 1)
}
-DWORD Count
if( Count > 0 ){
	do{
		-BYTE
		-BYTE		-Can be -1
		-DWORD
		-DWORD SubCount
		if( SubCount > 0 ){
			do{
				-BYTE
				-DWORD
			}while(SubCount-- != 1)
		}
		-DWORD SubCount
		if( SubCount > 0 ){
			do{
				-BYTE
				-DWORD
				-DWORD
			}while(SubCount-- != 1)
		}
		-DWORD SubCount
		if( SubCount > 0 ){
			do{
				-BYTE
				-BYTE
				-DWORD XCount							
				if( XCount > 0 ){
					do{
						-DWORD
					}while( XCount-- != 1) 
				}
			}while(SubCount-- != 1)
		}
	}while(Count-- != 1)
}

```