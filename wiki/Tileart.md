# Description #

Tile art contains informations about each single object existing in Ultima Online. This is valid for items but also for mobiles.

# Inner Extension #

```
.bin
```

# Format #

```

-WORD		Version 03
-DWORD		StringDictionary Offset -> dword[28*Group]
-DWORD		TileID
-BYTE		Unkown Bool
-BYTE
-DWORD		->float unknown
-DWORD		->float unknown
-DWORD		fixed zero?
-DWORD		->oldid?
-DWORD
-DWORD
-BYTE
-DWORD		->float 1.0? NOT float 3F800000
-DWORD		
-DWORD		->float LightRelated
-DWORD		->float LightRelated
-DWORD
-QWORD		FLAGS
-QWORD		FLAGS -> Got more data !
-DWORD
-B[24]		EC IMAGE Offset
-B[24]		2D IMAGE Offset

// Props
//	- 0 Weight
//	- 1 Quality
//	- 2 Quantity
//	- 3 Height
//	- 4 Value
//	- 5 AcVc
//	- 6 Slot
//	- 7 off_C8
//	- 8 Appearance
//	- 9 Race
//	- 10 Gender
//	- 11 Paperdoll
//

-BYTE Count					SUB_9
if( Count > 0 ){
	do{
		-BYTE		Prop
		-DWORD		Value
	}while(Count-- != 1)
}

-BYTE Count					SUB_9_2
if( Count > 0 ){
	do{
		-BYTE		Prop
		-DWORD		Value
	}while(Count-- != 1)
}

//At each amount corresponds a specific id. (Gold/Silver)
-DWORD Count					SUB_9_3 //MONEY items appearance
if( Count > 0 ){
	for ( i = Count; i; --i ){
		-DWORD		Amount
		-DWORD		ID
	}
}

-DWORD Count					SUB_9_4
if( Count > 0 ){
	do{
		-BYTE Val		//animation appearance filter
		if(Val){
			if(Val == 1){
				-BYTE			SUB_SUB_9
				-DWORD
			}
		}else{
			-DWORD SubCount			SUB_SUB_9_2
			if( SubCount > 0 ){
				do{
					-DWORD
					-DWORD
				}while(SubCount-- != 1)
			}	
		}
	}while(Count-- != 1)
}

-BYTE Count					SUB_9_5
if( Count != 0 ){			//The sitting data count is not 1 or 0
	-DWORD
	-DWORD
	-DWORD
	-DWORD
}

//RADARCOL
-BYTE	R					SUB_9_6 RADARCOLOR
-BYTE	G
-BYTE	B
-BYTE	Alpha

//Each item can have up to 4 textures
//TEXTURES
call TEXTURES()					SUB_9_7 DATA\WORLDART
call TEXTURES()					SUB_9_7 DATA\TILEARTLEGACY
call TEXTURES()					SUB_9_7 DATA\TILEARTENHANCED
//USED FOR LIGHTS
call TEXTURES()					SUB_9_7 DATA\TEXTURES


-BYTE Count				SUB_9_8
if( Count > 0 ){
	do{
		-DWORD		EffectID						
		call 4_6_30_Sub
		
		FUNCTION		//EFFECT
		//Could be
		//- 00 -> Unk_3
		//- 01 -> Unk_2_
		//- 02 -> Unk_4
		//- 07 -> Unk_5
		//- 10 -> Unk_6
		//- 11 -> Unk_30_sub_caller
		//- 12 -> Unk_30
		//- 15 -> Unk_29
		//- 16 -> Unk_32
		//- 17 -> Unk_31
		//////////
	}while(Count-- != 1)
}

```