# AnimationFrame{1..6}.uop

**Internal registry slot:** `UOAnimationFrameSetFactory` (registered at registry
slots `0x10` / `0x12`, see `FUN_004af1a0`). Loaded on demand by the animation
manager.

> ✅ **The payload format is fully decoded.** See
> **[AnimationFrame_AMOU.md](AnimationFrame_AMOU.md)** for the verified spec and a
> working reference decoder. This page is kept only for the archive-level facts;
> the format details that were here before were **wrong** (see the correction at
> the bottom).

## What it contains

The per-frame **AMOU**-format animation frames. Six UOP buckets sharing one
virtual-folder root; the partition by file is just load-balancing.

- **34,836 entries** total across the six archives, all resolving under the
  name pattern below.
- Body-id coverage **0–1681** (790 distinct bodies at action 0; action ids span
  0–78). These are the real in-game mobiles — human (400/401), horse (204/226),
  dragon (59), etc. The high-id bodies in `AnimationDefinition.uop` are a
  separate, frame-less id space (see [AnimationDefinition.md](AnimationDefinition.md)).

## Naming

```
build/animationframe/{body:06}/{action:02}.bin
```

- `body` = UO body id; `action` = action id. Hash the name once, query each
  `AnimationFrame{1..6}` in turn until a hit.

## Payload format (summary — full spec in AnimationFrame_AMOU.md)

- **40-byte header** (`0x00..0x27`): magic `AMOU`, version, total_size, body_id,
  global bbox (4×i16), `colour_count` (`0x18`), `colour_offset` (`0x1C`, always
  `0x28`), `frame_count` (`0x20`), `frame_offset` (`0x24`).
- **Palette** at `0x28`: `colour_count` × `(R,G,B,flag)`. The `flag` is the EC
  hue-mask (0 = skin/greyscale-tinted, ≠0 = baked cloth).
- **Frame table** at `frame_offset`: `frame_count` × 16 B.
- **Pixels**: anti-aliased **RLE** (not DXT), one slice per frame.
- **5 directions** are packed per action file (`frame_count = 5 × framesPerDir`),
  mirrored to 8 at draw time.

## ❌→✅ Correction (what this page used to claim)

The earlier version of this doc described a "32-byte header with a 256×40
**DXT-compressed atlas**, pixel encoding not yet decoded." **All wrong:**

- The header is **40 bytes**, not 32.
- The "`atlas_w = 256`" was the palette **`colour_count` (256)** at `0x18`; the
  "`atlas_h = 40`" was **`colour_offset` (0x28 = 40)** at `0x1C`. There is no
  256×40 atlas.
- The pixels are **anti-aliased RLE**, not DXT.

The decode was reverse-engineered from UOReader 0.8.7 and verified in-client.
