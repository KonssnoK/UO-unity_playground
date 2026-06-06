# string_dictionary.uop

**Internal registry slot:** `UOStringDictionary` (the EC global string table).

A single flat table of ASCII strings that many other archives reference **by
byte offset** — e.g. `tileart.uop` texture refs, `EffectDefinitionCollection`
layer textures, `MultiCollection` per-tile metadata, terrain names.

## Naming

```
build/stringdictionary/string_dictionary.bin
```

One entry (~3.8 MB).

## Format (from UOReader `stringDictionaryData`)

```
i64  unk64               # header value (timestamp/version)
u32  stringCount         # e.g. 120404
i16  unk16
stringCount × {
    u16  len
    u8[len]  ascii       # the string (e.g. "1255.tga", "UOSprite", "build/...")
}
```

- Two access modes (UOReader `StringDictionary`):
  - **by position / index** — the Nth string (`GetStringAtPosition`). **This is
    what the consumers actually use:** the stored `u32` is a 0-based string
    index. Verified — tileart name field `0x02` (40,402/40,402 in-range; index
    6=`nodraw`, 9=`ankh`) and `EffectDefinitionCollection` texture refs
    (268/269; e.g. index → `lightning.ems`).
  - **by byte offset** — the string whose record starts at byte `X`
    (`GetStringAtOffset`). Exists in the API but is **not** how tileart/effects
    reference strings (interpreting their `u32` as a byte offset resolves only
    ~3 %, by coincidence).

## Notes for the C# port

- Decompress once at load, keep the raw buffer, and expose
  `GetStringAtOffset(int)` that reads the `u16 len` then `len` ASCII bytes.
  ClassicUO's `EcStringDictionary` already does this.
