# Description #

This page contains the format of all the effects.

# Format #

```

---------------------------------------------------
EFFECT1 -> Unk_2.UOP -> BIN
			->standalone
			->FUNCTION indirectly called by tiledata_Effect_4_6_30
---------------------------------------------------
{
	-DWORD
	-DWORD
}

```
```

---------------------------------------------------
WATERFALLS
EFFECT0 -> Unk_3.UOP -> BIN
			->standalone
			->FUNCTION indirectly called by tiledata_Effect_4_6_30
---------------------------------------------------
{
	-DWORD	-> StringDictionary NIF Offset
	-DWORD
	-DWORD
	-DWORD
	-DWORD
	-BYTE
	-DWORD
	-BYTE
	-BYTE
	-BYTE
}

```
```

---------------------------------------------------
EFFECT2 -> Unk_4.UOP -> BIN
			->standalone
			->NO REFERENCE ON LOAD
---------------------------------------------------
{
	-DWORD Count
	for ( i = 1; i< Count; ++i ){
	
		Effect_4_6_30();
		TOCHECK
	}
}

```
```

---------------------------------------------------
EFFECT7 -> Unk_5.UOP -> BIN
			->standalone
			->NO REFERENCE ON LOAD
---------------------------------------------------
{
	for ( i = 0; i< 9; ++i ){
		-BYTE
		-BYTE
	
	TOCHECK
}

```
```

---------------------------------------------------
EFFECT10 -> Unk_6.UOP -> BIN
			->standalone
			->NO REFERENCE ON LOAD
---------------------------------------------------
{
	EFFECT1X_sub();
	
	-DWORD
	-DWORD
	-BYTE
}

```
```

---------------------------------------------------
EFFECT12 -> Unk_Tiledata_30 -> BIN	
			->standalone
			->FUNCTION indirectly called by tiledata_Effect_4_6_30 
---------------------------------------------------
{
	-BYTE
	-QWORD
	-DWORD

	Effect1X_sub();
	Effect_11_12_sub();
}

```
```

---------------------------------------------------
EFFECT17 Unk_31.UOP -> BIN
			->standalone
			->FUNCTION indirectly called by tiledata_Effect_4_6_30 
---------------------------------------------------
{
	-DWORD
	EFFECT1X_sub();
}

```
```

---------------------------------------------------
EFFECT16 -> Unk_32.UOP -> BIN
			->standalone
			->NO REFERENCE ON LOAD
---------------------------------------------------
{
	-DWORD Count	
	if( Count > 0 ){
		do{
			-DWORD
			
			EFFECT1X_sub();
			
		}while(Count-- != 1)
	}
}

```
```

---------------------------------------------------
EFFECT15 -> Unk_29.UOP -> BIN
			->standalone
			->NO REFERENCE ON LOAD
---------------------------------------------------
{
	-QWORD
	-QWORD
	-QWORD
	 TOCHECK
}

```