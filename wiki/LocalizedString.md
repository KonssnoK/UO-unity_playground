# Description #

Localized strings are used by the client to show messages to the user based on an identificator.

# Format #

```

-WORD 		unknown
-DWORD		unknown

while(!eof){
	-DWORD 		id
	-BYTE		unk
	-WORD		length
	-BYTE[length]	ASCII String
}

```