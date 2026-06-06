// Ghidra post-analysis Java script. v2 — xref-based.
//
// UOSA.exe is stripped of debug symbols, so asset identifiers only appear as
// string literals in .rdata. For each matched string this script:
//   1. Finds every code reference TO that string's address.
//   2. Looks up the function containing the xref's source address.
//   3. Decompiles that function (deduped) and records which strings triggered it.
//
// Output: JSON at $GHIDRA_OUT (default ./ghidra_dump.json).

//@category Analysis

import java.io.FileWriter;
import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolTable;
import ghidra.util.task.ConsoleTaskMonitor;

public class PostAnalysis extends GhidraScript {

    static final String[] KEYWORDS = {
        "Terrain", "TileArt", "GumpArtMask", "WorldArt",
        "MobAnim", "Mythic", "Sector",
        "%08d_TileArt", "%08d_LegacyTileArt",
        "tileartlegacy", "tileartenhanced", "worldart", "gumpartmask",
        "AnimationFrame", "LegacyTerrain", "TerrainDefinition", "TerrainTexture",
        "AtlasTerrain", "StaticTerrain", "GameTerrain",
        // Class-name strings for the record-parsing factories
        "TileArtData", "LegacyTextureData", "EnhancedTextureData", "GumpArtMaskData",
        "BinaryFactory", "BinaryBaseFactory",
        "UOTileArt", "AVUOTileArt", "AVUOTileArtBinary",
        "LegacyTileArtData", "EnhancedTileArtData",
        // The UOP filenames themselves
        "tileart.uop", "Texture.uop", "LegacyTexture.uop", "GumpArtMask.uop",
        "TerrainDefinition.uop", "LegacyTerrain.uop", "TerrainTexture.uop",
        // For tracing the SUB_9_7 sprite_id resolver
        "EnhancedTexture.uop", "EnhancedTexture",
        "TextureFileLocation", "SimpleTextureFileLocation", "SpriteTextureFileLocation",
        "WorldArtTexture", "AVWorldArt",
        "FetchTexture", "LoadTexture", "ResolveTexture",
        "TextureManager", "AVTextureManager", "ContainsTexture",
        // Asset cache / file lookup helpers
        "FindFileByName", "FindAsset", "ResourceManager", "AssetLoader",
        "MythicAssetLoader",
        // Texture group decode (SUB_9_7 lives inside TileArt records)
        "ParseTileArt", "DecodeTileArt", "ReadTileArt",
        "ParseTexture", "ReadTexture", "CreateTextureRef",
        // String dictionary lookup (sd_off resolver) — covers the off-by-prefix
        // issue we just hit. Names from typical EC/Mythic conventions.
        "StringDictionary", "string_dictionary", "stringdictionary",
        "GetString", "LookupString", "ResolveString",
        "Dictionary", "AVStringDictionary",
        // The tileart record parser (reads build/tileart/{id}.bin from
        // tileart.uop) — try class-name guesses and effect handler hints.
        "AVTileArt", "TileArtFactory", "TileArtReader", "ParseRecord",
        "DeserializeTileArt", "RegisterTileArt", "LoadTileArtData",
        // Effect-opcode handler (SUB_9_8) — opcodes 00/01/02/07/0A/0B/0C/0F/10/11
        "TileArtEffect", "EffectOpcode", "EffectFactory",
        "VisualEffect", "AVEffect", "EffectInfo", "TileEffect",
        // Generic property names that might appear as keys in effect blobs
        "Sparkle", "Splash", "Smoke", "GlowEffect", "ShimmerEffect",
    };

    @Override
    public void run() throws Exception {
        String outPath = System.getenv("GHIDRA_OUT");
        if (outPath == null) outPath = "ghidra_dump.json";

        SymbolTable symTable = currentProgram.getSymbolTable();
        ReferenceManager refMgr = currentProgram.getReferenceManager();
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);
        ConsoleTaskMonitor monitor = new ConsoleTaskMonitor();

        // 1. matching symbols
        List<Map<String, Object>> hits = new ArrayList<>();
        for (Symbol sym : symTable.getAllSymbols(true)) {
            String name = sym.getName();
            boolean match = false;
            for (String k : KEYWORDS) if (name.contains(k)) { match = true; break; }
            if (!match) continue;
            Map<String, Object> h = new LinkedHashMap<>();
            h.put("name", name);
            h.put("address", sym.getAddress() == null ? null : sym.getAddress().toString());
            h.put("symbol_type", sym.getSymbolType().toString());
            hits.add(h);
        }
        println("matched " + hits.size() + " candidate symbols");

        // 1b. Also queue up explicit function addresses we want decompiled
        // (suspected tileart loader chain + UOP loader helpers).
        String[] explicitFnAddrs = {
            "00457b20",   // texture/asset resolver called by FUN_0051a840
            "00a70df8",   // generic UOP loader helper
            "00403700",   // file-open helper used right before FUN_00a70df8
            "0098e793",   // post-load slot save (used after every UOP load)
            "00a70e45",   // exception/finally helper around UOP loads
            "00440620",   // shows up in terrain renderer
            "00678b10",   // CustomShaderData lookup (gump path)
            "0067c960",
            "0058e0b0",   // SpriteTextureFileLocation init
            "0058ecd0",   // path-copy helper
            "0058eab0",   // prefix-compare helper used to classify file locations
            "0040c640",   // tileart object setup (called immediately after FUN_00457b20)
            "0051fb60",
            "00458d80",   // FUN_00457b20 sub-call - the actual lookup body
            "00459390",   // FUN_00457b20 sub-call
            "0047d370",   // memory alloc helper
            "0051af20",   // legacy tile art loader (uses %08d_LegacyTileArt)
            "0051a840",   // HD tile art loader (uses %08d_TileArt)
            "005bfd30",   // called by both tile-art loaders
            // String-dictionary loader/lookup chain
            "00a72ba2",   // FUN that loads "Build/StringDictionary/string_dictionary.bin"
            "004bb0c0",   // Lua-bound "GetStringFromTid"  (the real resolver?)
            "004bb400",   // Lua-bound "GetStringUpppercaseFromTid"
            "004bb750",   // Lua-bound "ReplaceTokens"
            "008ddc25",   // Lua-bound "LoadStringTable"
            "008ddd98",   // Lua-bound "GetStringFromTable"
            "00a751ba",   // read-helper used by FUN_00a72ba2
            "0040c6c0",   // failure/log path inside FUN_00a72ba2
            // Request/Release TileArt — the Lua-bound asset registration site
            "0051e1d0",
            // The actual Lua-bound implementations (parser entry points)
            "0051c240",   // RequestTileArt
            "0051c920",   // ReleaseTileArt   (label, may not decompile)
            "0051cac0",   // RequestLegacyTileArt (label)
            "0051d1a0",   // ReleaseLegacyTileArt (label)
            "0051d340",   // RequestTexture
            "0051dbc0",   // RequestGumpArt
            "0051bff0",   // UpdatePortrait
            // Helpers around the loader chain we already know about
            "00a72ba2",
            // The asset factory called from FUN_005bfd30 — given (registry,
            // out, asset_id, 0x6000000, 0) returns the cached tileart object,
            // parsing the .bin on first access.
            "00a72320",
            "0040c640",   // referenced near tileart object setup
        };
        for (String addrStr : explicitFnAddrs) {
            Map<String, Object> h = new LinkedHashMap<>();
            h.put("name", "EXPLICIT_" + addrStr);
            h.put("address", addrStr);
            h.put("symbol_type", "ExplicitFunction");
            hits.add(h);
        }
        println("queued " + explicitFnAddrs.length + " explicit fn addresses");

        // 2. walk xrefs -> functions
        Set<String> seenFn = new HashSet<>();
        List<Map<String, Object>> decomps = new ArrayList<>();
        Map<String, List<String>> stringToFns = new LinkedHashMap<>();

        for (Map<String, Object> h : hits) {
            Object addrObj = h.get("address");
            if (addrObj == null) continue;
            Address addr = currentProgram.getAddressFactory().getAddress((String) addrObj);
            if (addr == null) continue;

            // For "ExplicitFunction" entries, decompile the function at that
            // address directly (don't bother with xrefs).
            if ("ExplicitFunction".equals(h.get("symbol_type"))) {
                Function fn = getFunctionAt(addr);
                if (fn == null) fn = getFunctionContaining(addr);
                if (fn != null) {
                    String key = fn.getEntryPoint().toString();
                    if (!seenFn.contains(key)) {
                        seenFn.add(key);
                        DecompileResults res = decomp.decompileFunction(fn, 60, monitor);
                        String code = "";
                        if (res != null && res.getDecompiledFunction() != null) {
                            code = res.getDecompiledFunction().getC();
                        }
                        Map<String, Object> d = new LinkedHashMap<>();
                        d.put("entry", key);
                        d.put("name", fn.getName());
                        d.put("signature", fn.getSignature().toString());
                        d.put("trigger_strings", new ArrayList<String>(
                                Arrays.asList((String) h.get("name"))));
                        d.put("decompiled", code);
                        decomps.add(d);
                    }
                }
                stringToFns.put((String) h.get("name"), Collections.singletonList(addr.toString()));
                continue;
            }

            List<String> referrers = new ArrayList<>();
            for (Reference ref : refMgr.getReferencesTo(addr)) {
                Address from = ref.getFromAddress();
                Function fn = getFunctionContaining(from);
                if (fn == null) continue;
                String key = fn.getEntryPoint().toString();
                referrers.add(key);
                if (seenFn.contains(key)) continue;
                seenFn.add(key);

                DecompileResults res = decomp.decompileFunction(fn, 60, monitor);
                String code = "";
                if (res != null && res.getDecompiledFunction() != null) {
                    code = res.getDecompiledFunction().getC();
                }
                Map<String, Object> d = new LinkedHashMap<>();
                d.put("entry", key);
                d.put("name", fn.getName());
                d.put("signature", fn.getSignature().toString());
                d.put("trigger_strings", new ArrayList<String>());
                d.put("decompiled", code);
                decomps.add(d);
                if (decomps.size() % 25 == 0) println("decompiled " + decomps.size() + " unique fns...");
            }
            stringToFns.put((String) h.get("name"), referrers);
        }

        // attach triggers
        Map<String, Map<String, Object>> byEntry = new HashMap<>();
        for (Map<String, Object> d : decomps) byEntry.put((String) d.get("entry"), d);
        for (Map.Entry<String, List<String>> e : stringToFns.entrySet()) {
            String trigger = e.getKey();
            for (String fnEntry : e.getValue()) {
                Map<String, Object> d = byEntry.get(fnEntry);
                if (d == null) continue;
                @SuppressWarnings("unchecked")
                List<String> ts = (List<String>) d.get("trigger_strings");
                if (!ts.contains(trigger)) ts.add(trigger);
            }
        }

        // 3. write JSON
        StringBuilder sb = new StringBuilder();
        sb.append("{\n");
        sb.append("  \"binary\": ").append(jstr(currentProgram.getName())).append(",\n");
        sb.append("  \"matched_symbols_count\": ").append(hits.size()).append(",\n");
        sb.append("  \"decompiled_function_count\": ").append(decomps.size()).append(",\n");
        sb.append("  \"string_to_referring_functions\": {\n");
        int si = 0;
        for (Map.Entry<String, List<String>> e : stringToFns.entrySet()) {
            sb.append("    ").append(jstr(e.getKey())).append(": [");
            for (int i = 0; i < e.getValue().size(); i++) {
                if (i > 0) sb.append(", ");
                sb.append(jstr(e.getValue().get(i)));
            }
            sb.append("]");
            if (si + 1 < stringToFns.size()) sb.append(",");
            sb.append("\n");
            si++;
        }
        sb.append("  },\n");
        sb.append("  \"decompiled_functions\": [\n");
        for (int i = 0; i < decomps.size(); i++) {
            sb.append("    ").append(toJsonRich(decomps.get(i)));
            if (i + 1 < decomps.size()) sb.append(",");
            sb.append("\n");
        }
        sb.append("  ]\n");
        sb.append("}\n");

        try (FileWriter fw = new FileWriter(outPath)) {
            fw.write(sb.toString());
        }
        println("Wrote " + hits.size() + " symbols, " + decomps.size()
                + " decompiled functions -> " + outPath);
    }

    private static String jstr(Object o) {
        if (o == null) return "null";
        String s = o.toString();
        StringBuilder b = new StringBuilder("\"");
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\': b.append("\\\\"); break;
                case '"':  b.append("\\\""); break;
                case '\n': b.append("\\n"); break;
                case '\r': b.append("\\r"); break;
                case '\t': b.append("\\t"); break;
                case '\b': b.append("\\b"); break;
                case '\f': b.append("\\f"); break;
                default:
                    if (c < 0x20) b.append(String.format("\\u%04x", (int) c));
                    else b.append(c);
            }
        }
        b.append('"');
        return b.toString();
    }

    @SuppressWarnings("unchecked")
    private static String toJsonRich(Map<String, Object> m) {
        StringBuilder b = new StringBuilder("{");
        int i = 0;
        for (Map.Entry<String, Object> e : m.entrySet()) {
            if (i++ > 0) b.append(", ");
            b.append(jstr(e.getKey())).append(": ");
            Object v = e.getValue();
            if (v instanceof List) {
                b.append("[");
                List<Object> list = (List<Object>) v;
                for (int k = 0; k < list.size(); k++) {
                    if (k > 0) b.append(", ");
                    b.append(jstr(list.get(k)));
                }
                b.append("]");
            } else {
                b.append(jstr(v));
            }
        }
        b.append("}");
        return b.toString();
    }
}
