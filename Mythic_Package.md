# Description #

Mythics's packages are the containers for the new UO's client.
Those were changed since KR, here's the latest.

UOPs can be open with the [MythicPackage\_Editor](http://code.google.com/p/mondains-legacy/downloads/detail?name=Mythic%20Package%20Editor%20v1.03.zip) made from Malganis

# Format #

```

Mythic Package File Format (.UOP)
---------------------------------

[1] Format Header
BYTE  -> 'M'
BYTE  -> 'Y'
BYTE  -> 'P'
BYTE  ->  0
DWORD -> Version
DWORD -> Signature?
QWORD -> Address of the first [2] Block
DWORD -> Max number of files per block
DWORD -> Number of files in this package
DWORD -> UNK ( 0 1 2 3 A C 1B) // Only V5.1
DWORD -> UNK (Same as Above )  // Only V5.1
BYTE[]-> 0

[2] Block Header
DWORD -> Number of files in this block
QWORD -> Address of the next block // 0 in V5.1

	[3] File Header
8	QWORD -> Address of [4] Data Header
4	DWORD -> Length of file header
4	DWORD -> Size of compressed file
4	DWORD -> Size of decompressed file
8	QWORD -> File hash
4	DWORD -> Adler32 of [4a] Data Header in little endian, unknown in Version 5
2	WORD  -> Compression type (0 - no compression, 1 - zlib)
	
	[4] Data Header (Version 4)
	WORD  -> Data type
	WORD  -> Offset to data
	QWORD -> File time (number of 100-nanosecond intervals since January 1, 1601 UTC)
	BYTE (size of compressed file) -> File	

	[4] Data Header (Version 5)
	BYTE[]-> Metadata used by UO patcher

Pseudocode:
[1] Format Header

while ( Address of the next block > 0 )
	[2] File Header

	while ( Max number of files per block )
		[3] File Header
	end

	while ( Number of files in this block )
		[4] Data Header
	end	
end

```