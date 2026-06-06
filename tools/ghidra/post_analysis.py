# Ghidra post-analysis script (PyGhidra / Python 3).
# Run via:  analyzeHeadless ... -postScript post_analysis.py
#
# Dumps every symbol whose name contains an EC asset-related keyword, plus the
# decompiled C for the function each one belongs to. Writes JSON to the path in
# the GHIDRA_OUT env var (default ./ghidra_dump.json).

# @category Analysis
# @runtime PyGhidra

import os
import json
import re

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

KEYWORDS = [
    "Terrain", "TerrainDefinition", "TerrainTexture", "TerrainLayer",
    "TileArt", "TileArtLegacy", "TileArtEnhanced",
    "GumpArtMask", "LegacyTerrain",
    "AVUOTerrain", "AVUOTileArt", "AVUOBaseTerrainLayer",
    "AVUOStaticTerrainShader", "AVUOTerrainShader",
    "AVUOTerrainDefinitionBinary",
    "WorldArt", "MobAnim",
    "Sector",                 # facet/sector loader
    "Mythic",                 # Mythic.Package-style
    "HashFile", "UopFile",
]

out_path = os.environ.get("GHIDRA_OUT", "ghidra_dump.json")

prog = getCurrentProgram()
sym_table = prog.getSymbolTable()
fn_mgr = prog.getFunctionManager()
listing = prog.getListing()
monitor = ConsoleTaskMonitor()

decomp = DecompInterface()
decomp.openProgram(prog)

hits = []
for sym in sym_table.getAllSymbols(True):
    name = sym.getName()
    if not any(k in name for k in KEYWORDS):
        continue
    addr = sym.getAddress()
    hits.append({
        "name": name,
        "address": addr.toString() if addr else None,
        "symbol_type": str(sym.getSymbolType()),
        "namespace": sym.getParentNamespace().getName(True) if sym.getParentNamespace() else None,
    })

# Decompile every function that any matched symbol belongs to.
fn_decomps = []
seen_fn_addrs = set()
for h in hits:
    if h["address"] is None:
        continue
    addr = prog.getAddressFactory().getAddress(h["address"])
    fn = fn_mgr.getFunctionAt(addr) or fn_mgr.getFunctionContaining(addr)
    if fn is None:
        continue
    key = fn.getEntryPoint().toString()
    if key in seen_fn_addrs:
        continue
    seen_fn_addrs.add(key)

    res = decomp.decompileFunction(fn, 60, monitor)
    code = ""
    if res and res.getDecompiledFunction():
        code = res.getDecompiledFunction().getC()
    fn_decomps.append({
        "trigger_symbol": h["name"],
        "entry": key,
        "name": fn.getName(),
        "signature": str(fn.getSignature()),
        "decompiled": code,
    })

data = {
    "binary": prog.getName(),
    "matched_symbols_count": len(hits),
    "decompiled_function_count": len(fn_decomps),
    "matched_symbols": hits[:5000],
    "decompiled_functions": fn_decomps,
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Wrote {len(hits)} symbols, {len(fn_decomps)} decompiled functions -> {out_path}")
