# AnimationDefinition.uop

**Internal registry slot pair:** 18 / 19.

## What it contains

1,205 small binary records (46 – 356 bytes). One record per **body type**. Each
maps the body to an ordered list of **frame-provider body-ids** — the bodies
whose AMOU folders actually supply this body's animation slots.

The class name is `UOAnimationDefinition` /
`UOAnimationDefinitionBinaryFactory` (string seen in `UOSA.exe`, instantiated
via vftable). The binary layout below is **verified across all 1,205 records**:
every record satisfies `len == 0x24 + count*5` exactly.

## Naming

```
build/animationdefinition/{id:08}.bin
```

- `id` is the body id, **not** an array index. The same id is also stored at
  offset 0 of the payload.
- Most records are *not* addressable by the plain `{body:08}` pattern — their
  virtual names come from `Dictionary.dic`. For field analysis read the entries
  directly; the body id is payload `[0x00]`.

## Record layout

The structure below is **confirmed against the EC parser** in `UOSA.exe`:
`FUN_004b81a0` reads the four leading dwords, then `FUN_004b82e0` runs an outer
loop `groupCount` times, each pass reading `groupKey, aliasGroup, interval,
slotCount` followed by `slotCount` slot reads (factory vtable method `+0x10`).

### Header + group block

`groupCount` (`0x10`) is always `1` in every shipped record, so the single
group's fields sit at the fixed offsets below.

| Offset | Size | Type | Field | Observed | Notes |
|-------:|-----:|------|-------|----------|-------|
| `0x00` | 4 | u32 | `bodyID` | varies | Body this record describes. Equals the filename id. |
| `0x04` | 4 | u32 | *field1* | always `0` | Read by the parser (passed through), purpose unknown. |
| `0x08` | 4 | u32 | *field2* | always `0` | ″ |
| `0x0C` | 4 | u32 | *field3* | always `0` | ″ |
| `0x10` | 4 | u32 | `groupCount` | always `1` | **Outer-loop count** in the parser. The whole "group block" below repeats this many times. |
| `0x14` | 4 | u32 | `groupKey` | always `0` | The group id this block defines (single-group bodies ⇒ 0). |
| `0x18` | 4 | i32 | `aliasGroup` | always `-1` | If `≠ -1`, the parser builds a redirect from `groupKey`→`aliasGroup` (same idea as AnimationSequence's `newGroup`). `-1` = none. |
| `0x1C` | 4 | f32 | `interval` | `0.0 – 0.9375` | **Stored on the runtime anim object** (parser writes it via `FUN_00837d14` into the group object `+0x30`). Per-group playback float; clusters on `1/16…1/2` ⇒ seconds-per-frame (`0.125`≈8 fps). |
| `0x20` | 4 | u32 | `slotCount` | `2 – 64` | Number of slot descriptors that follow. |

### Slot descriptors — `slotCount` × 5 bytes, starting at `0x24`

| Offset | Size | Type | Field | Notes |
|-------:|-----:|------|-------|-------|
| `+0x00` | 4 | u32 | `srcBodyID` | An ordered body-id reference. Slot 0 = primary source; the rest are sibling/alternate bodies. |
| `+0x04` | 1 | u8 | `flag` | **Always `0`** across all 10,011 descriptors. Reserved. |

The slot's *position* (0-based) is its index; the parser passes the index to the
factory's slot reader, which stores `(index → srcBodyID)`.

## What this archive is — and is NOT (RESOLVED ✅)

The decisive finding: **AnimationDefinition and AnimationFrame (AMOU) live in
almost-disjoint body-id spaces.**

- **AMOU** covers body ids **0–1681** — the real in-game mobiles (human 400/401,
  horse 204/226, dragon 59, …). Every common mobile is here and is animated by
  indexing AMOU **directly by its own body id**; none of them have an
  AnimationDefinition record.
- **AnimationDefinition** is keyed almost entirely by **high ids 2000–46000+**
  (10 000 400 max). Only **10 of 1 202** records reference an AMOU-backed body at
  all, and only **3** fully resolve (942/943/944). The high bodies have **no
  frame data anywhere** in the shipped archives — not in AMOU, and there is no
  separate HD-animation archive.

So AnimationDefinition is **not** the lookup table that drives normal mobile
animation. It is a separate registry over EC's high/HD asset id space whose
referenced frames are not present in this install. The slot list is best read as
"ordered frame-source body ids (slot 0 primary, rest siblings)", and the rotated
sets seen on clusters like 109/110/111 or 942/943/944 are just each body listing
its group **self-first**.

### Why the earlier "per-direction sub-bodies" guess was wrong
Directions are **packed inside each AMOU file** (5 contiguous direction slices —
see [AnimationFrame_AMOU.md](AnimationFrame_AMOU.md)), so they are *not* spread
across adjacent body ids. Bodies 105/106/107 are different creatures (frame
counts 60/55/50, bboxes 316×236 / 342×324 / 136×128), not directions of one.

## Notes for the C# port

- For mobile rendering you do **not** need AnimationDefinition: index
  `AnimationFrame{1..6}` directly by the mobile's body id
  (`build/animationframe/{body:06}/{action:02}.bin`) and slice the 5 directions.
  This is what ClassicUO's EC path already does and why it works.
- If a future feature touches EC's HD/high-body assets, parse the record as
  `{ bodyID, interval, aliasGroup, srcBodyID[] }` per the table above — but note
  the frames those ids reference are absent from a stock install.

## Action numbering across CC and EC

This is the most important practical fact for porting EC animations
into a CC engine (and the cause of "cow plays death when idle" bugs).

**CC's `GetGroupForAnimation` returns action IDs in *per-body-type*
enums:**
- `AnimationGroupsType.Human` / `Equipment` → `PeopleAnimationGroup`
  (e.g. `Stand = 4`, `Die1 = 21`)
- `AnimationGroupsType.Animal` (default) → `LowAnimationGroup`
  (e.g. `Stand = 2`, `Die1 = 8`)
- `AnimationGroupsType.Monster` → `HighAnimationGroup`
  (e.g. `Stand = 1`, `Die1 = 2`)

**AMOU files always use `HighAnimationGroup` numbering, regardless
of body type.** So for any non-Monster body, the action number CC
emits has to be **translated to High** before the AMOU file lookup.

### Example: cow (body 216, `AnimationGroupsType.Animal`)

- CC emits action `Low.Stand = 2` for "idle"
- AMOU's `00000216/02.bin` is `High.Die1` — the **death** animation
- Without remapping, cow plays death when standing → use the
  Low → High table from `AnimationFrame_AMOU.md`

### The `CalculateOffsetLowGroupExtended` flag

Some `Animal` bodies in `mobtypes.txt` set the
`CalculateOffsetLowGroupExtended` flag (`0x20`). CC's dispatcher then
switches the body's effective group to **High** (default), **Low**
(if `ByLowGroup = 0x40` is also set), or **People** (if
`ByPeopleGroup = 0x400` is also set).

In a stock UO Classic install the flag is set on **21 bodies**: `5,
6, 23, 25, 27, 29, 34, 37, 52, 63, 64, 65, 81, 88, 97, 98, 99, 100,
127, 133, 134` — visually these are **flying creatures** (eagles, bats,
small birds) and **dragon-style monsters** (97, 127, 134) that
animate from a monster skeleton even though they're typed Animal.

Implication for the port: when remapping CC actions to AMOU's High
numbering for `Animal` bodies, **read the body's flags** and skip the
Low → High step when `Extended` is set (without `ByLowGroup`). These
bodies already emit High-group actions from CC.

### Per-body AMOU action presence

Each body's AnimationDefinition record enumerates the action IDs
that body supports (the `count`× small descriptors after the header).
Many bodies are sparse — e.g. body 5 (eagle) ships actions
`{2, 4, 10, 19, 22, 25, 26}`. Notably no `Walk(0)` or `Stand(1)`:
flying creatures don't walk, and "idle" maps to `Fly(19)` instead.

The renderer should:
1. Compute the action via CC's `GetGroupForAnimation`.
2. Translate to High if needed (using the body's effective group).
3. Look up the AMOU file; if missing, **fall back to CC** rather than
   guessing a near match. The EC engine has its own fallback logic
   (e.g. flying creature with no Stand → use Fly) that we haven't
   fully reverse-engineered yet.
