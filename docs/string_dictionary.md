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
  - **by position** — the Nth string (`GetStringAtPosition`).
  - **by byte offset** — the string whose record starts at byte `X` in the
    decompressed buffer (`GetStringAtOffset`). This is what tileart/effects use:
    the stored `u32` is a **byte offset** into this buffer, not an index.
    (Verified: offset 119154 → `"1255.tga"`.)

## Notes for the C# port

- Decompress once at load, keep the raw buffer, and expose
  `GetStringAtOffset(int)` that reads the `u16 len` then `len` ASCII bytes.
  ClassicUO's `EcStringDictionary` already does this.
