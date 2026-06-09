# Runtime tracing of the Enhanced Client (UOSA.exe)

Dynamic analysis complements the static Ghidra dump: spawn the real client under
[Frida](https://frida.re) and observe what actually runs. Tooling:
`tools/ec_research/scripts/frida_uosa_trace.py`.

## Why it's clean here

- **UOSA.exe has ImageBase `0x400000` and NO ASLR** (PE `DllCharacteristics=0`;
  confirmed at runtime — the spawned module base is `0x400000`). So **every
  static address from the Ghidra dump maps 1:1 to a runtime address** — no
  rebasing, hook by absolute address directly.

## Access

- The user's normal client runs **elevated**, so Frida can't attach to it from a
  non-elevated shell ("unable to access process from current user account").
- **Solution: spawn a fresh client under Frida** (`frida.spawn`). It launches at
  the current user's privilege (attachable) and — importantly — **all archives
  load at startup, before login**, so the asset parse happens in the spawn
  window with no server/login needed.

## Confirmed by the tracer

- **Archive load order at startup** (hooking `kernel32!CreateFileW`, filtering
  `*.uop`) — matches the registry slot order exactly:
  `facet0..6, tileart, string_dictionary, AnimationDefinition, TerrainDefinition,
  EffectDefinitionCollection, AnimationSequence, Texture, Audio, EffectTexture,
  LocalizedStrings, TerrainChunk, RadarMapTexture, Interface, GameData, MainMisc,
  LegacyTerrain, TerrainTexture, SystemTextures, Paperdoll, Hues, MultiCollection,
  Shaders, Waypoint, LegacyTexture, facets, EnhancedTexture, GumpArtMask`.
  (`TerrainChunk`, `RadarMapTexture`, `EnhancedTexture`, `Waypoint` are *opened*
  even though not all ship on disk.)

## What can and can't be hooked

- **Hookable:** Win32 APIs, normal C++ functions, vtable methods, constructors.
- **Not hookable as "the field reader":** the binary-factory record parsers read
  each field with **inline** memory accesses (`*(int*)(buf + cursor)`), not via a
  callable helper — so there's no single function to hook to watch field reads.
- **Some tiny/jump-table functions can't be trampoline-hooked** (Frida: "unable
  to intercept function") — e.g. the effect-type factory `FUN_005782b0`. That one
  is also a *one-time* template-registry build (`FUN_00575b30` loops a fixed
  `0x1f`), not a per-effect parser, so it wouldn't help anyway.

## Open: the tileart Effects (SUB_9_8) per-opcode bodies

Still the one undecoded piece (see [tileart_VERIFIED.md](tileart_VERIFIED.md)).
The parse uses each effect template's **deserialize vtable method**; locating and
hooking those (or Stalker-tracing the tileart-parse window to enumerate the
functions involved) is the next dynamic step. It's a <1 %, visual-only feature
with no reference decoder, so it's low priority.

## Usage

```
# default: trace archive loads for 20s from a fresh spawn
python tools/ec_research/scripts/frida_uosa_trace.py
# also hook specific static addresses (logs eax/ecx/arg0/caller on entry)
python tools/ec_research/scripts/frida_uosa_trace.py --hook 0x578b70 --seconds 30
```
