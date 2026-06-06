# tools/

Reverse-engineering & research tooling for the Enhanced Client (`.uop`) formats.
The findings live in [`../docs/`](../docs/); this tree holds the code that
produced them.

## Layout

| Path | What |
|------|------|
| `ec_research/scripts/` | ~100 Python analysis scripts (UOP decoding, EC↔CC correlation, brute-forcing, validation). Numbered roughly in the order they were written. |
| `ec_research/ec/` | Reusable Python modules: `uop.py` (UOP/MYP reader + Jenkins hash), `dic.py` (Dictionary.dic parser), `patterns.py`. |
| `ec_research/scripts/frida_uosa_trace.py` | Runtime function tracer for `UOSA.exe` (no ASLR → static Ghidra addresses map 1:1). Run elevated. |
| `ec_research/uoreader/decompiled/` | Decompiled UOReader 0.8.7 source (`.cs`) — the authoritative format reference. |
| `ec_research/uoreader/Dictionary.dic`, `scripts/Dictionary.dic` | Hash→name tables used for naming resolution/validation. |
| `ghidra/scripts/` | Ghidra headless scripts (`FullDump.java`, etc.) that produce the decompile dumps. |

## Regenerating the large artifacts (git-ignored)

To keep the repo lean, these are **not** tracked — regenerate as needed:

- **`ghidra/ghidra_full.jsonl`** (~52 MB, UOSA.exe decompile dump) — produced by
  the Ghidra headless scripts in `ghidra/scripts/`. Most `ec_research/scripts`
  that read it expect it at that path.
- The Ghidra install (`ghidra/ghidra_*_PUBLIC/`), JDK, project DBs, Python
  `.venv`s, `dump_*/` image dumps, and `ec_research/out/` catalogs are likewise
  ignored — see the `tools/` section of the repo `.gitignore`.

## Data paths assumed by the scripts

- Enhanced Client: `C:\Games\Electronic Arts\Ultima Online Enhanced`
- Classic Client:  `C:\Games\Electronic Arts\Ultima Online Classic`
