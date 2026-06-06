# Facets — `facets.uop` + `facet{0..5}.uop` / `facet{0..5}x.uop`

The EC **map data** system: per-map definitions plus per-sector terrain/static
chunks. This is the EC equivalent of CC's `map*.mul` + `statics*.mul` +
`staidx*.mul`.

## `facets.uop` — facet (map) definitions

```
build/facetdefinition/{N:08}.bin
```

7 entries = the 7 UO maps (facet 0–6). Each is a small variable-length header
record. Observed leading fields per facet:

| facet | len | field@0x10 |
|------:|----:|-----------:|
| 0 (Felucca) | 2244 | 58 |
| 1 (Trammel) | 1412 | 35 |
| 2 (Ilshenar) | 900 | 20 |
| 3 (Malas) | 148 | 4 |
| 4 (Tokuno) | 148 | 4 |
| 5 (TerMur) | 836 | 24 |
| 6 | 52 | 1 |

The `field@0x10` count tracks map size (Felucca largest), so the record is a
per-facet header followed by a variable list of region/sector descriptors. Exact
field layout not yet decoded (low priority — the per-sector chunks below carry
the actual tiles).

## `facet{0..5}.uop` / `facet{0..5}x.uop` — per-sector map chunks

```
build/sectors/facet_{NN}/{sector:08}.bin       (NN = 2-digit facet index)
```

- Each `facet{N}.uop` holds **~7,169 sector records** (one per **64×64-cell**
  map sector), ~26 MB per archive. `facet{N}x.uop` is a parallel set (the `x`
  variant — a second copy, base vs. overlay).

### Sector record format — VERIFIED ✅

Decoded from UOReader's `FacetSectorItem`/`FacetSectorTile`/`FacetSectorDelimiter`/
`FacetSectorStatic` classes and verified against the data: **7168/7169 sectors
per facet consume their buffer exactly** (the lone failure is an empty/special
sector), confirmed across `facet0`, `facet0x`, `facet3`.

```
u8   facetID
u16  sectorID                    # == the {sector:08} in the filename
64 × 64 tiles (row-major, x outer, y inner) {
    i8   z                       # land height
    u16  landGraphic             # land tile id
    u8   delimiterCount
    delimiterCount × {           # terrain-transition / blend edges  (6 B)
        u8   direction           # which neighbour edge (0,1,2,…)
        i8   z
        u32  graphic             # neighbouring terrain graphic to blend
    }
    u8   staticCount
    staticCount × {              # static items in this cell  (9 B)
        u32  graphic             # static tile id
        i8   z
        u32  color               # hue / tint
    }
}
```

- **delimiters** are the EC terrain auto-tiling data — per-cell directional
  blend entries that fill the seams between adjacent land types (CC does this
  with transition tiles; EC stores explicit neighbour graphics + direction).
- **statics** are the per-cell static placements (the EC equivalent of
  `statics*.mul`). facet0 holds ~2.9M statics and ~1.8M delimiters.
- The `x` archive carries an almost identical static count — a base/overlay or
  Trammel/Felucca-style parallel layer.

> **Port note:** ClassicUO renders maps from CC `map*.mul` + `statics*.mul`, so
> for a CC-compatible client these sectors are redundant. They're only needed
> for a **pure-EC** map renderer — but the format is now fully known, so that
> path is unblocked.

## Status

**Fully decoded** ✅ — naming (UOReader dictionary) and the per-sector chunk
binary layout (verified 7168/7169 exact). The `facetdefinition` per-map header
list is the only remaining minor unknown. ClassicUO still uses the CC
`map*.mul`/`statics*.mul` path, so these archives are bypassed for the
CC-compatible client, but the format is no longer a blocker for pure-EC map work.
