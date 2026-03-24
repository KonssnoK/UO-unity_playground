# Description #

The string dictionary is the first uop loaded by the EC client.

It contains strings used to get textures from UOP and many other things.

# Inner Extension #

```
.bin
```

# Format #

```
-QWORD
-DWORD Count
-WORD
do{
	-WORD SLen = StringLength
	-B[SLen] String
}while(Count-- != 1)
```