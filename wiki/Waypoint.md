# Description #

This format is currently unknown.

# Inner Extension #

```
.bin
```

# Format #

```

-WORD Val
if(Val == 2){
	-WORD	 Count						SUB_24
	if( Count > 0 ){
		do{
			-DWORD
			-DWORD
		}while(Count-- != 1)
	}
	-WORD	 Count						SUB_24_2
	if( Count > 0 ){
		do{
			-DWORD
			-DWORD
		}while(Count-- != 1)
	}
	-WORD	 Count						SUB_24_3
	if( Count > 0 ){
		do{
			-DWORD
			-BYTE
			for( i = 0 ; i < 3 ++i){
				-DWORD
				-BYTE
			}
		}while(Count-- != 1)
	}
	-WORD	 Count						SUB_24_4
	if( Count > 0 ){
		do{
			-DWORD
			-DWORD
			-BYTE
			-BYTE
			-WORD
			-WORD
			-DWORD
		}while(Count-- != 1)
	}
}

```