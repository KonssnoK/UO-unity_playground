# Introduction #

This file use is currently unknown (inform me if you find what is for)

# Inner Extension #
```
facetdefinition.bin
```

# Format #

```
-BYTE
-DWORD
-DWORD
-DWORD
-BYTE
-BYTE
-BYTE
-DWORD Count						SUB_28
if( Count > 0 ){
	do{
		-DWORD	Number_in_Cycle
		-DWORD
		-BYTE
		-BYTE
		-BYTE
		-BYTE
		-DWORD	SubCount			SUB_SUB_28
		if( SubCount > 0 ){
			do{
				-DWORD
				-DWORD
				-DWORD
				-DWORD
			}while(SubCount-- != 1)
		}
	}while(Count-- != 1)
}
```