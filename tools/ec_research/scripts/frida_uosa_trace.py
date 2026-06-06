"""Runtime tracer for the Enhanced Client (UOSA.exe) via Frida.

UOSA.exe has ImageBase 0x400000 and **no ASLR** (verified at runtime: the
spawned module base is 0x400000), so absolute addresses from the Ghidra dump
map 1:1 — no rebasing.

Spawn a fresh client (catches asset load from the very start) and trace:

    python frida_uosa_trace.py                       # archive-load trace (default)
    python frida_uosa_trace.py --hook 0x5782b0,0x578b70   # also hook these static addrs
    python frida_uosa_trace.py --seconds 30

Notes
-----
* Spawning works at the current user's privilege (no need to match the
  elevated, already-running client). It opens a second UOSA window.
* The binary-factory record parsers read fields with **inline** memory
  accesses (not a callable helper), so you can't hook "the field reader".
  What you CAN hook: real functions (constructors, vtable methods, Win32
  APIs). Some tiny/jump-table functions can't be trampoline-hooked — those
  are reported as "unhookable" and skipped.
* Confirmed by this tracer: all archives load at startup in registry order
  (facet0..6, tileart, string_dictionary, AnimationDefinition, ...), so the
  tileart/effects parse happens during the spawn window — no login needed.
"""
import frida, time, argparse, json

EXE = r"C:\Games\Electronic Arts\Ultima Online Enhanced\UOSA.exe"

JS = r'''
function expt(mod, name){
  try { return Process.getModuleByName(mod).getExportByName(name); }
  catch(e){ try { return Module.getGlobalExportByName(name); } catch(e2){ return null; } }
}
var m = Process.getModuleByName("UOSA.exe");
send({base: m.base.toString(), size: m.size});

// --- archive-load trace (CreateFileW) ---
var cf = expt("kernel32.dll", "CreateFileW");
if (cf) Interceptor.attach(cf, { onEnter: function(a){
  try { var p = a[0].readUtf16String(); if (p && /\.uop$/i.test(p)) send({uop: p.replace(/^.*[\\/]/,'')}); } catch(e){}
}});

// --- user hooks by static address ---
var HOOKS = HOOKS_JSON;
HOOKS.forEach(function(addr){
  try {
    Interceptor.attach(ptr(addr), { onEnter: function(args){
      var c = this.context;
      send({ hook: addr, eax: (c.eax>>>0), ecx: (c.ecx>>>0),
             arg0: this.context.esp.add(4).readU32(), ret: this.returnAddress.toString() });
    }});
    send({hooked: addr});
  } catch(e){ send({unhookable: addr, err: String(e)}); }
});
send({status: "ready"});
'''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hook", default="", help="comma-separated static addrs, e.g. 0x5782b0,0x578b70")
    ap.add_argument("--seconds", type=int, default=20)
    ap.add_argument("--exe", default=EXE)
    args = ap.parse_args()

    hooks = [int(x, 16) for x in args.hook.split(",") if x.strip()]
    js = JS.replace("HOOKS_JSON", json.dumps(hooks))

    def on(msg, data):
        print(msg.get("payload") if msg["type"] == "send" else msg, flush=True)

    pid = frida.spawn([args.exe])
    print("spawned pid", pid, flush=True)
    s = frida.attach(pid)
    sc = s.create_script(js); sc.on("message", on); sc.load()
    frida.resume(pid)
    try:
        time.sleep(args.seconds)
    finally:
        print("--- stopping ---", flush=True)
        try: frida.kill(pid)
        except Exception: pass

if __name__ == "__main__":
    main()
