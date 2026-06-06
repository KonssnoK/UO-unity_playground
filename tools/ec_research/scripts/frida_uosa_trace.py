"""Runtime function tracer for the Enhanced Client (UOSA.exe) via Frida.

UOSA.exe has ImageBase 0x400000 and **no ASLR** (verified), so the absolute
addresses from the Ghidra dump map 1:1 to runtime addresses — no rebasing.

Usage (run from an ELEVATED shell — UOSA runs elevated, so Frida must match):
    # spawn a fresh client and trace from the very start (catches asset load):
    python frida_uosa_trace.py --spawn "C:/Games/Electronic Arts/Ultima Online Enhanced/UOSA.exe"
    # or attach to a running one (same privilege level required):
    python frida_uosa_trace.py --attach UOSA.exe

Add/disable hooks in HOOKS below. Each hook logs entry (args from the cdecl/
thiscall stack), and optionally hexdumps a byte buffer pointed to by an arg
(handy for parsers: see how many bytes each opcode consumes).

This is a generic capability — point it at any function to map it at runtime.
"""
import sys, argparse, frida

# (label, static_addr, arg_count, dump_arg_index_or_None, dump_len)
# Seeded with tileart/effect-parse candidates from the static analysis.
HOOKS = [
    # effect-object factory dispatch (switch on type id -> alloc+construct)
    ("effectFactory_005782b0", 0x005782b0, 1, None, 0),
    # the per-record stream cursor read helpers (0040c6c0 = bounds-check read)
    ("streamRead_0040c6c0",     0x0040c6c0, 4, None, 0),
    # add the tileart record parser here once located, e.g.:
    # ("tileartParse_00XXXXXX", 0x00XXXXXX, 4, 0, 256),
]

JS_TEMPLATE = r'''
var BASE = ptr(0x400000);
var hooks = HOOKS_JSON;
hooks.forEach(function (h) {
    var addr = ptr(h.addr);
    try {
        Interceptor.attach(addr, {
            onEnter: function (args) {
                var rec = { fn: h.label, addr: h.addr.toString(16), args: [] };
                for (var i = 0; i < h.argc; i++) {
                    try { rec.args.push(this.context ? null : null); } catch (e) {}
                }
                // read first few stack dwords (cdecl args at [esp+4..])
                try {
                    var sp = this.context.esp;
                    var a = [];
                    for (var i = 1; i <= h.argc; i++) a.push(sp.add(i*4).readU32());
                    rec.stack = a;
                } catch (e) { rec.stack_err = String(e); }
                if (h.dump >= 0) {
                    try {
                        var p = ptr(rec.stack[h.dump]);
                        rec.dump = p.readByteArray(h.dumplen);
                    } catch (e) { rec.dump_err = String(e); }
                }
                send(rec, rec.dump);
            }
        });
        send({ status: "hooked", label: h.label, addr: h.addr.toString(16) });
    } catch (e) {
        send({ status: "hook_failed", label: h.label, err: String(e) });
    }
});
send({ status: "ready" });
'''

def build_js():
    import json
    hk = [{"label": l, "addr": a, "argc": c, "dump": (d if d is not None else -1), "dumplen": dl}
          for (l, a, c, d, dl) in HOOKS]
    return JS_TEMPLATE.replace("HOOKS_JSON", json.dumps(hk))

def on_message(msg, data):
    if msg["type"] == "send":
        p = msg["payload"]
        if data:
            print(p, "bytes=", data.hex())
        else:
            print(p)
    else:
        print("ERR", msg)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spawn"); ap.add_argument("--attach")
    args = ap.parse_args()
    if args.spawn:
        pid = frida.spawn([args.spawn])
        session = frida.attach(pid)
        resume = pid
    elif args.attach:
        session = frida.attach(args.attach)
        resume = None
    else:
        ap.error("need --spawn <exe> or --attach <name|pid>")
    script = session.create_script(build_js())
    script.on("message", on_message)
    script.load()
    if resume is not None:
        frida.resume(resume)
    print("[tracer running — Ctrl+C to stop]")
    sys.stdin.read()

if __name__ == "__main__":
    main()
