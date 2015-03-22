# Introduction #

Questo programma che sto sviluppando serve a comprimere i files creati con "UO:KR Unpacker", qui posterò i vari ChangeLog.

[b](b.md)[color=red]---19/09/08--- Parte 7[/color][/b]
[b](b.md)v1.0 Stable[/b]
- now repacker will check also subfolders; to do right unpacking must select ./unpacked/ folder or the one which build/ is child
- fix to name hashing ( now hashing is Right )
- fixed Datablock ( also last block )
- Cleaned form1 by 2 writings method and calculate offset v1.0

[img](img.md)http://img362.imageshack.us/img362/2329/packerreleasezz6.jpg[/img]

[b](b.md)[color=red]---19/09/08--- Parte 6[/color][/b]
[b](b.md)v0.9[/b]
- fixed offset to Datablock
( last block not working )
[b](b.md)v0.81[/b]
- fixed offset to nextblock
( now indexes are readed correctly by unpacker. )

[b](b.md)[color=red]---18/09/08--- Parte 5[/color][/b]
[b](b.md)v0.8[/b]
- Added 2 types of writing
( now size is Ok, offsets are to check)
- Added new offset calculation
- Added regions
[b](b.md)v0.71[/b]
- added zeroes to blocks

[b](b.md)[color=red]---17/09/08--- Parte 4[/color][/b]
[b](b.md)v0.7[/b]
- added Blocksize
- cleaned some trash
[b](b.md)v0.62[/b]
- added nextblock offset
[b](b.md)v0.61[/b]
- fixed dimension of .uop ( now is smaller 1056 bytes )
[b](b.md)v0.6[/b]
- added Datablockoffset
- added Dataoffset
- rewrited writing funct ( still not working, 250+ mega .uop)

[b](b.md)[color=red]---16/09/08--- Parte 3[/color][/b]
[b](b.md)v0.52[/b]
- repacker will now compress only files bigger than 10bytes
[b](b.md)v0.51[/b]
- added version
- added Fill prop to header
- Fix to Flag dimension
- Fix to Dataoffset dimension
- deleted zeros when over counting
- Fix to HEader start
[b](b.md)v0.5[/b]
- added .uop writing ( not working properly )


[b](b.md)[color=red]---16/09/08--- Parte 2[/color][/b]
[b](b.md)v0.41[/b]
- added Header creation ( to check )
[b](b.md)v0.4[/b]
- added Block creation( to check zeroes )
[b](b.md)v0.3[/b]
- added FileTime ( to check )
- added AboutBox
- added CRC Adler32 ( to check )

[img](img.md)http://img519.imageshack.us/img519/4894/packer1rs1.jpg[/img]


[b](b.md)[color=red]---16/09/08--- Parte 1[/color][/b]
[b](b.md)v0.2[/b]
- added Hashing of names
- index now registers data's lists
- added Progress-bar
- added bg\_Worker
[b](b.md)v0.1b[/b]
- added fileInFolder reading
[b](b.md)v0.1a[/b]
- added folder reading
- added funny textbox ( as statusbar )
[b](b.md)v0.1[/b]
- main classes

![http://img523.imageshack.us/img523/2826/packerqb8.jpg](http://img523.imageshack.us/img523/2826/packerqb8.jpg)