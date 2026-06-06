# AnimationFrame{1..6}.uop

**Internal registry slots:** Not directly registered through the `FUN_00a70e5a` table — these archives are loaded on demand by the animation manager (the disassembly references `AVUOAnimationFrameSet` and `AVUOAnimationFrameSetFactory` types).

## What it contains

The per-frame **AMOU**-format animation atlases. One UOP per loader bucket (the EC partitions animations into six buckets the same way the CC partitions `anim.mul` / `anim2.mul` / etc.).

| File                       | Entries  |
|----------------------------|---------:|
| `AnimationFrame1.uop`      |  6,124   |
| `AnimationFrame2.uop`      | 14,382   |
| `AnimationFrame3.uop`      |  8,900   |
| `AnimationFrame4.uop`      |  2,575   |
| `AnimationFrame5.uop`      |    455   |
| `AnimationFrame6.uop`      |  1,693   |
| **Total**                  | **34,129** |

## Naming

```
build/animationframe/{body:06}/{action:02}.bin
```

- **100% coverage** across all six archives — every entry resolves.
- `body` is the UO body id (e.g. 109 = horse, 400 = human male, 943 = mongbat, etc.).
- `action` is the action id (0..40-ish per body, varies).
- All six buckets share the SAME folder root (`animationframe`); the partition by *file* is just a load-balancing artefact. Look-up logic for the C# port: hash the name once, query each AnimationFrame{1..6} in turn until you find a hit.

## Payload format — the AMOU header

The first 32 bytes of every entry follow this layout (confirmed by sampling `AnimationFrame1.uop[0]`):

```
offset  size  field          example values
0       4     magic          'AMOU'
4       4     version u32    1
8       4     dsize u32      = entry.decompressed_size (sanity field)
12      4     count u32      varies (frame count or something proportional)
16      2     bbox_min_x i16 e.g. -31
18      2     bbox_min_y i16 e.g. -99
20      2     bbox_max_x i16 e.g. +31
22      2     bbox_max_y i16 e.g. -21
24      2     atlas_w u16    always 256 in our sample
26      2     padding/flags  always 0
28      4     atlas_h u32    always 40 in our sample (per-strip height)
32...         frame pixel data follows
```

- Atlas dimensions 256×40 imply a horizontal strip of frames per row; larger animations stack rows.
- Pixel encoding past the 32-byte header is **not yet decoded** — likely DXT-compressed atlas plus a directions/timings table. Needs another RE pass.

## Disassembly notes

- The Ghidra dump shows `AVUOAnimationFrameSet`, `AVUOAnimationFrameSetFactory`, `AnimationLegacyFrameSet` types referenced — these are the in-memory classes built from the AMOU payloads.
- The "Legacy" variant (`AnimationLegacyFrameSet`) suggests EC keeps both legacy `.mul`-derived animations AND new `AMOU` ones in the same engine; for ClassicUO we only need the AMOU path.

## Notes for the C# port

- 2-level hash lookup is cheap: pre-compute hashes for `(body, action)` pairs as needed.
- AMOU pixel-decode is the next big blocker. Two options:
  1. **Decode AMOU** properly. Requires identifying the codec (could be DXT block-runs interspersed with metadata for direction / hue layers).
  2. **Defer animations** in the C# port: render statics + terrain first, fall back to CC anims, treat AMOU as a future task.
- Recommended for first cut: option 2.
