# MultiCollection.uop

**Internal registry slot:** `UOMultiCollectionBinaryFactory` (registered at
registry slot `0x13`, see `FUN_004af1a0`).

House / boat / multi definitions — the EC equivalent of CC's `multi.mul` +
`multi.idx`. One record per multi id.

## Naming — RESOLVED ✅

```
build/multicollection/{N:06}.bin     (6-digit zero-padded)
```

- 872 entries; 325 named directly in the UOReader 0.8.7 `Dictionary.dic`, the
  rest follow the same zero-padded pattern. `N` is the multi id (0-based).

## Record format — VERIFIED ✅

Decoded from UOReader (`MultiItem.Load`) and verified against the data:
**871/872 records parse and consume their buffer *exactly***. (The one outlier
is a ~41 KB giant multi.)

```
u32  id              # multi id (== filename N)
u32  tileCount
tileCount × {
    u16  graphic     # static tile id placed in the multi
    i16  x           # cell offset from the multi anchor
    i16  y
    i16  z           # height offset (clamped to sbyte at runtime; >255 = invalid)
    u8   flag1       # 0 (96%) or 1 (4%)  — per-tile flag
    u8   flag2       # 0 (96%) or 1 (4%)  — per-tile flag
    u32  strCount
    strCount × i32   # indices into the EC StringDictionary (per-tile metadata)
}
```

Field notes (measured over all records, 186k tiles):
- **`flag1` / `flag2`** are each almost always `0`, `1` on ~4 % of tiles —
  small booleans (CC's multi format carries a "visible"/"is-static" flag in the
  same slot; these are the EC equivalents).
- **`strCount`** is `0` on ~96 % of tiles; `1` on ~1.3 %, `2` on ~0.4 %. The
  `i32` values index `string_dictionary.uop` (`StringDictionary.GetStringAtPosition`),
  i.e. optional per-tile string metadata (UOReader stores them as `MultiTile.UnkList`).

## Connection to other archives

| Source | Provides |
|--------|----------|
| `MultiCollection.uop` (this) | multi id → list of `(graphic, x, y, z, flags, strRefs)` |
| `string_dictionary.uop` | resolves the per-tile `i32` string indices |
| `tileart.uop` | each tile `graphic` resolves to its sprite/flags |

## Notes for the C# port

- Parse into `Dictionary<int multiId, MultiTile[]>` at load; mirrors CC's
  `MultiLoader`. The `(graphic, x, y, z)` quad is the CC-compatible core; the
  EC `flag1/flag2` + string refs are extra metadata most tiles don't use.
- Z is stored as `i16` but is logically an `sbyte` (runtime casts it).
