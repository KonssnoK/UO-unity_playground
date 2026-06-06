// Ghidra post-analysis Java script: full-binary dump.
//
// Decompiles EVERY function in the loaded program (UOSA.exe) and writes one
// JSON object per line (JSONL) to $GHIDRA_OUT_JSONL (default ./ghidra_full.jsonl).
// JSONL avoids a multi-GB single-JSON file that no tool can stream.
//
// Each line:
//   {"entry":"0051a840","name":"FUN_0051a840","signature":"...","callees":["..."],
//    "callers":["..."],"strings":["..."],"decompiled":"..."}
//
// Also writes a sidecar index $GHIDRA_OUT_INDEX (default ./ghidra_index.json):
//   { "by_entry": { "0051a840": <line_number_in_jsonl> }, "by_name": {...} }
// so lookup-by-address is O(1) without scanning the whole JSONL.
//
//@category Analysis

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.util.*;

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.decompiler.DecompileOptions;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.StringDataInstance;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.Listing;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceManager;
import ghidra.util.task.ConsoleTaskMonitor;

public class FullDump extends GhidraScript {

    @Override
    public void run() throws Exception {
        String jsonlPath = System.getenv("GHIDRA_OUT_JSONL");
        if (jsonlPath == null) jsonlPath = "ghidra_full.jsonl";
        String indexPath = System.getenv("GHIDRA_OUT_INDEX");
        if (indexPath == null) indexPath = "ghidra_index.json";

        ConsoleTaskMonitor monitor = new ConsoleTaskMonitor();
        DecompInterface decomp = new DecompInterface();
        DecompileOptions opts = new DecompileOptions();
        decomp.setOptions(opts);
        decomp.toggleCCode(true);
        decomp.toggleSyntaxTree(false);
        decomp.openProgram(currentProgram);

        Listing listing = currentProgram.getListing();
        ReferenceManager refMgr = currentProgram.getReferenceManager();

        // Build address -> ascii string map for resolving constant-string xrefs in
        // each function. Cheap pre-pass.
        Map<String, String> stringByAddr = new HashMap<>();
        DataIterator di = listing.getDefinedData(true);
        while (di.hasNext() && !monitor.isCancelled()) {
            Data d = di.next();
            if (d == null) continue;
            String type = d.getDataType().getName();
            if (!(type.contains("string") || type.contains("String"))) continue;
            try {
                StringDataInstance s = StringDataInstance.getStringDataInstance(d);
                String txt = s.getStringValue();
                if (txt == null) continue;
                txt = trimAscii(txt);
                if (txt.length() < 2) continue;
                stringByAddr.put(d.getAddress().toString(), txt);
            } catch (Exception ignore) {}
        }
        println("indexed " + stringByAddr.size() + " strings");

        FunctionIterator funcs = currentProgram.getFunctionManager().getFunctions(true);
        long t0 = System.currentTimeMillis();
        int written = 0;
        int skipped = 0;

        // Stream out to JSONL — one function per line.
        try (BufferedWriter w = new BufferedWriter(new FileWriter(jsonlPath));
             BufferedWriter idx = new BufferedWriter(new FileWriter(indexPath))) {

            // index is just a JSON map { entry: line_number }
            idx.write("{\n  \"by_entry\": {\n");
            boolean firstIdx = true;

            int total = currentProgram.getFunctionManager().getFunctionCount();
            println("functions to decompile: " + total);

            while (funcs.hasNext() && !monitor.isCancelled()) {
                Function fn = funcs.next();
                if (fn == null) continue;
                if (fn.isThunk() || fn.isExternal()) { skipped++; continue; }

                String entry = fn.getEntryPoint().toString();
                String name = fn.getName();
                String sig = fn.getSignature().toString();

                // Collect callees (functions called from this body) and callers.
                LinkedHashSet<String> callees = new LinkedHashSet<>();
                for (Function c : fn.getCalledFunctions(monitor)) {
                    callees.add(c.getEntryPoint().toString());
                }
                LinkedHashSet<String> callers = new LinkedHashSet<>();
                for (Function c : fn.getCallingFunctions(monitor)) {
                    callers.add(c.getEntryPoint().toString());
                }

                // Strings referenced by this function body.
                LinkedHashSet<String> stringsHit = new LinkedHashSet<>();
                Address body = fn.getEntryPoint();
                Address end = fn.getBody().getMaxAddress();
                Address cur = body;
                while (cur != null && cur.compareTo(end) <= 0) {
                    Reference[] refs = refMgr.getReferencesFrom(cur);
                    if (refs != null) {
                        for (Reference r : refs) {
                            String tgt = r.getToAddress() == null ? null : r.getToAddress().toString();
                            if (tgt == null) continue;
                            String s = stringByAddr.get(tgt);
                            if (s != null) stringsHit.add(s);
                        }
                    }
                    cur = cur.next();
                    if (cur == null) break;
                }

                // Decompile (60s timeout). On failure write empty body — still
                // useful for callee/caller graph.
                String code = "";
                DecompileResults res = decomp.decompileFunction(fn, 60, monitor);
                if (res != null && res.getDecompiledFunction() != null) {
                    code = res.getDecompiledFunction().getC();
                }

                // Write the line.
                StringBuilder line = new StringBuilder(256 + code.length());
                line.append('{');
                appendField(line, "entry", entry, true);
                appendField(line, "name", name, false);
                appendField(line, "signature", sig, false);
                appendArray(line, "callees", callees);
                appendArray(line, "callers", callers);
                appendArray(line, "strings", stringsHit);
                appendField(line, "decompiled", code, false);
                line.append("}\n");
                w.write(line.toString());

                if (!firstIdx) idx.write(",\n");
                firstIdx = false;
                idx.write("    " + jstr(entry) + ": " + written);

                written++;
                if ((written & 0xFF) == 0) {
                    long elapsed = (System.currentTimeMillis() - t0) / 1000;
                    println("decompiled " + written + "/" + total + " (skip=" + skipped
                            + ") " + elapsed + "s");
                }
            }

            idx.write("\n  }\n}\n");
        }

        long elapsed = (System.currentTimeMillis() - t0) / 1000;
        println("DONE: " + written + " functions in " + elapsed + "s -> " + jsonlPath);
        println("index -> " + indexPath);
    }

    private static String trimAscii(String s) {
        StringBuilder b = new StringBuilder(s.length());
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == 0) break;
            if (c >= 0x20 && c < 0x7f) b.append(c);
        }
        return b.toString();
    }

    private static void appendField(StringBuilder sb, String key, String val, boolean first) {
        if (!first) sb.append(',');
        sb.append(jstr(key)).append(':').append(jstr(val));
    }

    private static void appendArray(StringBuilder sb, String key, Collection<String> items) {
        sb.append(',').append(jstr(key)).append(":[");
        boolean f = true;
        for (String s : items) { if (!f) sb.append(','); sb.append(jstr(s)); f = false; }
        sb.append(']');
    }

    private static String jstr(Object o) {
        if (o == null) return "null";
        String s = o.toString();
        StringBuilder b = new StringBuilder(s.length() + 2).append('"');
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
}
