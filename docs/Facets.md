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

- Each `facet{N}.uop` holds **~7,169 sector records** (one per map sector),
  ~26 MB per archive. `facet{N}x.uop` is a parallel set (the `x` variant — the
  two cover terrain vs. static layers / base vs. overlay).
- A sector record is the binary terrain+static placement for that sector
  (heights, land tile ids, static items). Each is **~22 KB** (the common size is
  22,043 B; 160 of the first 300 share it), starting with a small header then a
  long run of per-cell records (land tile ids such as `0x0244` are visible in
  the raw bytes). The exact cell layout (terrain block vs. statics block split,
  per-cell stride) is **not yet decoded**.

> **Priority note:** this is the largest undecoded EC archive *by size*, but
> **low value for a CC-compatible port** — ClassicUO renders maps from CC
> `map*.mul` + `statics*.mul`, so these facet sectors are bypassed entirely.
> Decoding them is only worthwhile for a *pure-EC* map renderer.

## Status

Naming fully resolved (via the UOReader dictionary). The per-sector chunk binary
layout is the main outstanding EC map-rendering task; for now the CC
`map*.mul`/`statics*.mul` path is used and these archives are bypassed.
