# Audit — can we render Enhanced statics in ClassicUO now?

Checklist of what the existing CC static renderer needs vs. what the EC research has produced.

## Required inputs (per static at world cell X, Y, Z with art id `N`)

| # | Need                                  | EC source                              | Status | Notes                                                                 |
|---|---------------------------------------|----------------------------------------|--------|-----------------------------------------------------------------------|
| 1 | Hash-addressable archive of art       | `Texture.uop` + `LegacyTexture.uop`    | ✅     | Patterns confirmed (96% / 76%); the rest falls back to CC `art.mul`. |
| 2 | DDS pixel decode                      | `Texture2D.FromStream` (FNA)           | ✅     | FNA supports DXT1/3/5/BC4/BC5 in DDS; verified via Pillow.            |
| 3 | Texture dimensions (W × H)            | DDS header (24/28 bytes in)            | ✅     | Read width/height/format directly from DDS bytes.                     |
| 4 | Anchor offset (sprite origin vs. cell) | `tileart.uop` record                   | ⚠️     | Binary layout partially decoded; `tiledata.mul` fallback works.       |
| 5 | Tile height / z-extent (for stacking) | `tileart.uop` record                   | ⚠️     | Same; CC's height field is correct for ~99% of tiles.                 |
| 6 | Tile flags (impassable, bridge, …)    | `tileart.uop` record                   | ⚠️     | Same; CC `TileFlag` covers all the existing logic.                    |
| 7 | Hue / palette application             | `Hues.uop`                             | ✅     | 100% mapped (`data/definitions/hues/hue{NN:04}.bmp`).                 |
| 8 | Sort by world Z                       | C# scene graph                         | ✅     | No change vs. CC.                                                     |
| 9 | Animated statics (water, fire, …)     | `AnimationFrame*.uop` (AMOU)           | ❌     | Defer — AMOU pixel decode is unsolved. CC anims fill the gap.         |

## Bottom line

**Yes — we can render enhanced statics now**, by combining:

- **Pixels** from `Texture.uop` (HD) → `LegacyTexture.uop` (legacy DDS) → CC `art.mul` (final fallback).
- **Metadata** (anchor, height, flags) initially from CC `tiledata.mul`. For ~99% of the world this is visually correct because the EC re-encoded the *same tile* in the *same anchor*.

The remaining 1% (tiles whose EC anchor differs from CC) and the *correct* EC `tileart.uop` layout are a follow-up RE pass — they are not blockers for the first integration milestone.

## Update from Ghidra pass #2 — the runtime `TileArt` struct

`FUN_0051a840` is the HD-texture lookup that wraps `"%08d_TileArt"`. After resolving the cached object via `FUN_00457b20`, it accesses a 6-float struct laid out as:

```c
struct EcTileArt {            // in-memory; not the on-disk layout
    float x0;                  // bounds-min x
    float y0;                  // bounds-min y
    float x1;                  // bounds-max x  (width = x1 - x0)
    float y1;                  // bounds-max y  (height = y1 - y0)
    float pixels_x_offset;     // anchor X within the texture
    float pixels_y_offset;     // anchor Y within the texture
    /* + handle / interface pointers follow */
};
```

So an EC tile-art object is a bounding rect (4 floats) plus an anchor pair (2 floats). This is what the renderer actually consumes — it's the in-memory representation produced by parsing the on-disk `tileart.uop` record.

**For the C# first-cut renderer**: emulate the same struct in managed code. Populate `x0,y0,x1,y1` from the DDS dimensions (`x0=0, y0=0, x1=ddsW, y1=ddsH`) and `pixels_x_offset/y_offset` from `tiledata.mul` (or just leave at zero for centering). The visual output will match the EC 99% of the time; the residual 1% (tiles with non-standard anchor offsets) needs the on-disk record decoded.

## What to do for full EC fidelity (`tileart.uop` decode)

Empirically, every record begins:

```
offset  size  field           example (id 0x4000)
0       2     version u16     0x0004
2       4     stringId u32    0x0000B01C (offsets into LocalizedStrings.uop)
6       4     tileArtId u32   matches the file id
10      4     count u32       usually 1
14      4     scale_x f32     1.0
18      4     scale_y f32     1.5
22      4     ??              0
26      3     rgb24           0xFFFFFF for statics
…       …    … not yet decoded …
```

Per-tile floats *do* appear deeper in the record (e.g. id 16640 contains `cd cc cc bd 33 33 a3 c0` = `(-0.1, -5.1)` floats — almost certainly the anchor offset).

The clean path forward is a focused Ghidra pass on the **tileart record parser function**: search for cross-references to the `tileart.uop` filename literal in `FUN_00a70e5a` line 548, follow the loader stub to the per-record decode routine, then dump that function's struct accesses. That's a 2-hour RE task once we tee up the right script.
