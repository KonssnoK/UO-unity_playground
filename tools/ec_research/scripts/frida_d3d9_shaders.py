"""Dump every D3D9 shader UOSA.exe creates, via Frida (runtime capture).

The UO 2D-layer shaders are in Shaders.uop (text HLSL). The **terrain** shaders
(GameTerrain_HybridLighting/VertexLighting/Offscreen, AtlasTerrain) are NOT in
any file or recoverable bytecode — they're **generated at runtime by the
Gamebryo NiD3DShader system**. The only way to get them is to capture the
bytecode at IDirect3DDevice9::CreatePixelShader / CreateVertexShader time.

This hooks the COM vtable (no ASLR on UOSA, but d3d9.dll is resolved at runtime):
  Direct3DCreate9[Ex] -> CreateDevice[Ex] -> device vtbl[106]=CreatePixelShader,
  vtbl[91]=CreateVertexShader. Each shader's bytecode is dumped (disassemble
  later with D3DDisassemble / fxc /dumpbin).

IMPORTANT: shaders are created when the client actually RENDERS. The 2D shaders
appear at the login screen; **terrain shaders only appear in-world**, so to
capture them you must (a) close any already-running (elevated) client so this
spawn isn't single-instanced out, and (b) log in and stand on terrain.

    python frida_d3d9_shaders.py --seconds 120 --out captured_shaders
"""
import frida, time, argparse, os

EXE = r"C:\Games\Electronic Arts\Ultima Online Enhanced\UOSA.exe"
JS = r'''
function gx(m,n){ try{return Process.getModuleByName(m).getExportByName(n);}catch(e){return null;} }
var seen={}, devHooked=false;
function dump(pf,kind){ try{
  var ver=pf.readU32(), nn=0, p=pf;
  while(nn<16384){ if(p.readU32()===0x0000FFFF){nn++;break;} p=p.add(4); nn++; }
  var bytes=pf.readByteArray(nn*4);
  var key=kind+':'+ver.toString(16)+':'+nn;
  if(seen[key]) return; seen[key]=1;
  send({shader:kind, version:'0x'+ver.toString(16), dwords:nn}, bytes);
}catch(e){ send({dump_err:String(e)}); } }
function hookDev(dev){ if(devHooked)return; devHooked=true; try{
  var vt=dev.readPointer();
  Interceptor.attach(vt.add(106*4).readPointer(),{onEnter:function(a){dump(a[1],'ps');}});
  Interceptor.attach(vt.add(91*4).readPointer(),{onEnter:function(a){dump(a[1],'vs');}});
  send({status:'DEVICE HOOKED — capturing shaders'});
}catch(e){send({hd_err:String(e)});} }
function hookCD(p,idx,ppIdx){ try{
  var cd=p.readPointer().add(idx*4).readPointer();
  Interceptor.attach(cd,{onEnter:function(a){this.pp=a[ppIdx];},onLeave:function(){try{var d=this.pp.readPointer(); if(!d.isNull())hookDev(d);}catch(e){}}});
}catch(e){} }
function arm(){
  var f=gx('d3d9.dll','Direct3DCreate9'), fx=gx('d3d9.dll','Direct3DCreate9Ex');
  if(f) Interceptor.attach(f,{onLeave:function(r){if(!r.isNull())hookCD(r,16,7);}});       // CreateDevice
  if(fx) Interceptor.attach(fx,{onEnter:function(a){this.pp=a[1];},onLeave:function(){try{var p=this.pp.readPointer(); if(!p.isNull())hookCD(p,20,8);}catch(e){}}}); // CreateDeviceEx
  return !!(f||fx);
}
if(!arm()){ var ll=gx('kernel32.dll','LoadLibraryExW'); if(ll) Interceptor.attach(ll,{onLeave:function(){arm();}}); }
setInterval(function(){ send({hb:{shaders:Object.keys(seen).length, dev:devHooked}}); }, 5000);
send({status:'armed'});
'''

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--seconds',type=int,default=60)
    ap.add_argument('--out',default='captured_shaders')
    ap.add_argument('--exe',default=EXE)
    args=ap.parse_args()
    os.makedirs(args.out,exist_ok=True)
    n=[0]
    def on(m,d):
        p=m.get('payload') if m['type']=='send' else m
        if isinstance(p,dict) and p.get('shader') and d:
            fn=os.path.join(args.out,f"{n[0]:03d}_{p['shader']}_{p['version']}_{p['dwords']}dw.bin"); n[0]+=1
            open(fn,'wb').write(d); print('saved',fn,flush=True)
        else: print(p,flush=True)
    pid=frida.spawn([args.exe]); print('pid',pid,flush=True)
    s=frida.attach(pid); sc=s.create_script(JS); sc.on('message',on); sc.load(); frida.resume(pid)
    try: time.sleep(args.seconds)
    finally:
        print('--- stopping ---',flush=True)
        try: frida.kill(pid)
        except Exception: pass

if __name__=='__main__': main()
