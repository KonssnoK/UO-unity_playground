# EffectDefinitionCollection.uop

**Internal registry slot:** `UOEffectDefinitionCollectionBinaryFactory`
(registered at registry slot `0xd`, see `FUN_004af1a0`).

Visual-effect definitions — each describes one or more texture **layers** that
compose an animated effect (sparkle, glow, splash, …). These are what the
`tileart.uop` **Effects (SUB_9_8)** section and in-world effects reference.

## Naming — RESOLVED ✅

```
build/effectdefinitioncollection/{N:08}.bin     (8-digit zero-padded)
```

269 entries; 267 named directly in the UOReader `Dictionary.dic`.

## Record format

```
u32  layerCount
layerCount × {                      # 32 bytes each
    u32  type            # 0 in the common case (layer/blend type)
    u32  texStringOffset # offset into string_dictionary.uop -> effect texture name, e.g. "1255.tga"
    u32  _a              # 0
    u32  _b              # 0
    u32  _c              # 0
    f32  param           # 1.0 / 0.5 / 0.75 / 0.3 … (intensity / scale / rate)
    u32  flags           # 1, or packed values like 0x40000001 / 0x80000001
    u32  _d              # 0
}
```

- Record sizes line up exactly: `layerCount=1 → 36 B` (4 + 32), `2 → 68 B`,
  `3 → 100 B`. Most records are single-layer (261 of 269).
- **`texStringOffset`** resolves through `string_dictionary.uop` to a `.tga`
  filename (verified: offset 119154 → `"1255.tga"`); the actual pixels live in
  **`EffectTexture.uop`**.
- **`param`** is a float effect parameter clustering on `0.25–1.0`.
- **`flags`** low bit is usually set; the high bits (`0x40000000`, `0x80000000`)
  look like blend/loop mode bits.

## Connection to other archives

| Source | Provides |
|--------|----------|
| `EffectDefinitionCollection.uop` (this) | effect id → texture layers + params |
| `string_dictionary.uop` | resolves each layer's `texStringOffset` → `.tga` name |
| `EffectTexture.uop` | the actual effect-texture pixels |
| `tileart.uop` (Effects / SUB_9_8) | per-tile effect references |

## Status

Layout is decoded for the common single-layer case; the `flags` high bits and
multi-layer composition rules are not yet fully characterised (low priority —
purely visual).
