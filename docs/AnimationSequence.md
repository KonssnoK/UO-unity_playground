# AnimationSequence.uop

**Internal registry slot pair:** 24 / 25.

388 binary records, ~2.4 KB each (range 2,377 – 7,045 B; the dominant size is
2,431 B, 227 records). One record per body id. It is a **per-body group table**:
how many frames each animation group has, and optional group→group remaps.

This archive is **not EC-specific** — the modern Classic Client ships the same
`AnimationSequence.uop` and ClassicUO already parses it in
`AnimationsLoader.ProcessAnimationSequenceData`
([AnimationsLoader.cs:839](../../src/ClassicUO.Assets/AnimationsLoader.cs#L839)).
The fixed header + entry layout below is taken from that parser and verified
against the EC bytes; field names match the CC reader.

## Naming

```
build/animationsequence/{id:08}.bin
```

100% coverage. `id` = body id. The same id is **also stored at offset 0** of the
payload (`animID`), so a record is self-identifying.

## Record layout

### Header (56 bytes)

| Offset | Size | Type | Field | Notes |
|-------:|-----:|------|-------|-------|
| `0x00` | 4 | u32 | `animID` | Body id. Equals the filename id. |
| `0x04` | 48 | — | *reserved* | **Always zero** across all 388 records. CC `reader.Skip(48)`. |
| `0x34` | 4 | i32 | `replaceCount` | Number of group entries that follow. **Sentinel:** the values `48` and `68` mean "no entries / use defaults" — CC skips the entry loop entirely for them. Real counts seen: `29` (340 recs), `32` (41), `31` (4). |

### Group entries — `replaceCount` × 72 bytes, starting at `0x38`

`oldGroup` increments `0,1,2,…` across the entries, so the array is simply
"group 0, group 1, …" in order. Stride verified at exactly 72 bytes.

| Offset | Size | Type | Field | Notes |
|-------:|-----:|------|-------|-------|
| `+0x00` | 4 | i32 | `oldGroup` | The animation-group id this entry describes (0-based, sequential). |
| `+0x04` | 4 | u32 | `frameCount` | Frame count of that group. **`0` is the trigger for a remap** (see below); non-zero means the group exists natively with this many frames. |
| `+0x08` | 4 | i32 | `newGroup` | Replacement group. `-1` = no remap (the common case for monsters). |
| `+0x0C` | 4 | f32 | `frameCount` (float) | Same value as `frameCount` as a float (e.g. `9` ⇒ `9.0`). Likely a duration/rate scratch field. |
| `+0x10` | 16 | — | *fill* | `0x80808080` repeated — an uninitialised-memory fill pattern, not data. |
| `+0x20` | 40 | — | *reserved* | Zero. |

CC reads only the first 12 bytes (`oldGroup`, `frameCount`, `newGroup`) and
`Skip(60)` over the rest.

### How CC applies it

```csharp
uint animID   = ReadUInt32();   // 0x00
Skip(48);                       // 0x04..0x33
int replaces  = ReadInt32();    // 0x34
if (replaces != 48 && replaces != 68)
    for (k in replaces) {
        int  oldGroup   = ReadInt32();   // +0x00
        uint frameCount = ReadUInt32();  // +0x04
        int  newGroup   = ReadInt32();   // +0x08
        if (frameCount == 0)             // 0 frames natively => redirect
            uopInfo.ReplacedAnimations[oldGroup] = newGroup;
        Skip(60);                        // +0x0C..+0x47
    }
```

So the practical contract is: **for each group, if `frameCount == 0` the group
has no frames of its own and playback should fall back to `newGroup`.** This is
the mechanism that fixes "missing group" cases (a body that lacks e.g. an attack
group borrows another group's frames).

### Trailing section (variable, not fully decoded)

After the `replaceCount` × 72-byte array there is a further variable-length
block (e.g. 287 B on the 2,431-byte records, larger on the 4–7 KB outliers).
CC ignores it entirely. It is a nested count-prefixed structure — the 2,431-byte
records begin it with `02 00 00 00` then sub-records mixing small ints and the
same `0x80808080` fill. It has **not** been reverse-engineered; it is not needed
for frame playback (CC plays animations correctly without reading it). Decoding
it is only worthwhile if a future feature needs whatever per-direction / timing
extras EC stored here.

## Notes for the C# port

- Load into `Dictionary<int animID, UopInfo>` exactly as CC's
  `ProcessAnimationSequenceData` does; reuse that code path unchanged.
- Relevant for EC only as the source of **group-remap** and **frame-count**
  data; the AMOU pixels themselves come from `AnimationFrame{1..6}.uop`
  (see [AnimationFrame_AMOU.md](AnimationFrame_AMOU.md)).
- The group ids here are in CC's per-body-type group numbering, **not** AMOU's
  High numbering — see the action-numbering section in
  [AnimationDefinition.md](AnimationDefinition.md).
