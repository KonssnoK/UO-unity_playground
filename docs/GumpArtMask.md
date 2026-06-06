# GumpArtMask.uop

**Internal registry slot pair:** 66 / 67 (registered last in `FUN_00a70e5a`).

## What it contains

DDS **mask textures** that pair with the entries in `gumpartLegacyMUL.uop` to provide an alpha channel (the classic gump format is paletted with a 1-bit colour-key transparency; the mask gives smooth alpha for the EC renderer).

## Naming — cracked via disassembly

The pattern was **invisible to brute-force** because the id is offset by +1,000,000. The decompiled `FUN_005960f0` shows:

```c
FUN_009a3ada(auStack_408, 0x400,
             "Build\\GumpArtMask\\0%d.dds",
             (int)local_44c + 1000000);
```

That `sprintf` produces `Build\GumpArtMask\01000000.dds`, `01000001.dds`, … . The leading `0` is **literal** (not zero-padding), then the integer expands without padding.

Lower-cased + forward-slashed for hashing:

```
build/gumpartmask/0{id+1000000:d}.dds
```

## Empirical coverage

- **Entries in archive:** 4,597.
- **Mapped by the formula above:** **4,597 (100%)**.
- Sample names:
  - `build/gumpartmask/01000000.dds`  ← gump id 0
  - `build/gumpartmask/01000001.dds`  ← gump id 1
  - `build/gumpartmask/01004596.dds`  ← gump id 4,596

## Notes for the C# port

- The `+1,000,000` offset is an EC convention shared with at least one other namespace: we observe `Data\WorldArt\01000020_daymap.tga` in the binary's string table, which is `worldart` id 1,000,020. So the offset is the engine's way of segregating *shader/effect* textures from *gameplay* textures within a single logical namespace.
- For the C# port: map `(gumpId) → entry` by hashing `f"build/gumpartmask/0{gumpId + 1_000_000}.dds"`. No special-cases needed.
- To composite a final gump: load the corresponding `gumpartLegacyMUL` entry (TGA, classic palette) and overlay the alpha from this DDS mask.
- File-location code (from `FUN_0058e1a0`): **0x1b (27)** for `GumpArtMask\` requests.
