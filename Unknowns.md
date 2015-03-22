# Description #

This page contains the format of all the unknown formats i found in the client.


# Format #

```

---------------------------------------------------
AnimationFrameSet_7.UOP -> BIN
			->standalone
			->REFERENCED by sub
---------------------------------------------------
-DWORD
-DWORD
-DWORD

```
```

---------------------------------------------------
Effect_4_6_30
Called by	->EFFECT1X_sub
			->Tiledata_sub_9_8
			->Unk_4
			->AnimationSequence_sub
			->standalone
---------------------------------------------------
{
	-DWORD									4_6_30_Sub
	
	FUNCTION();
}

```
```
	
---------------------------------------------------
EFFECT1X_sub -> Unk_sub
Called by 	->Unk_30_sub
			->Unk_Tiledata_30
			->Unk_6
			->Unk_31
			->Unk_32
---------------------------------------------------
{
	-DWORD Count								COUNT_LOOP
	for(i =0 ; i < Count; ++i){
		
		Effect_4_6_30();
		
	}
}

```
```

---------------------------------------------------
EFFECT_11_12_sub -> Unk_30_sub
Called by 	->Unk_30
			->Standalone
---------------------------------------------------
{
	-DWORD SubCount								30_Sub
	if( SubCount > 0 ){
		do{
			-DWORD
			
			EFFECT1X_sub();
			
		}while(SubCount-- != 1)
	}
}

```
```

---------------------------------------------------
Unk_20_sub.UOP -> BIN
			->unk_20
---------------------------------------------------
{
	-DWORD XCount					SUB_20				
	if( XCount > 0 ){
		do{
			-DWORD
			-DWORD
		}while( XCount-- != 1) 
	}
}

```
```

---------------------------------------------------
Unk_20.UOP -> BIN
			->standalone
			->REFERENCED by sub
---------------------------------------------------
{
	-DWORD Count
	if( Count > 0 ){
		do{
			-DWORD
			-DWORD SubCount
			if( SubCount > 0 ){
				do{
					-DWORD
					-DWORD
					-DWORD
					-DWORD
					
					Unk_20_sub();
					Unk_20_sub();
					Unk_20_sub();
					
				}while(SubCount-- != 1)
			}
		}while(Count-- != 1)
	}
}

```