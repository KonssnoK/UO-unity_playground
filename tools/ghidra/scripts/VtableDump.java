// Find CObj vtable: scan the constructor for any constant/ref into .rdata whose
// slots look like .text function pointers, then dump it.
//@category Analysis
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.scalar.Scalar;

public class VtableDump extends GhidraScript {
    boolean looksText(long a){ return a>=0x00401000L && a<=0x006e0000L; }
    boolean validVtable(Address base){
        try{
            int ok=0;
            for(int i=0;i<8;i++){ long fp=getInt(base.add(i*4))&0xFFFFFFFFL; if(looksText(fp)&&getFunctionAt(toAddr(fp))!=null) ok++; }
            return ok>=6;
        }catch(Exception e){return false;}
    }
    @Override public void run() throws Exception {
        Address ctor=toAddr(0x005baf30L);
        Function f=getFunctionAt(ctor);
        Instruction ins=getInstructionAt(ctor);
        int guard=0; Address vt=null;
        java.util.LinkedHashSet<Long> cands=new java.util.LinkedHashSet<>();
        while(ins!=null && getFunctionContaining(ins.getAddress())==f && guard++<120){
            int nops=ins.getNumOperands();
            for(int op=0;op<nops;op++){
                for(Object o:ins.getOpObjects(op)){
                    if(o instanceof Scalar){ long v=((Scalar)o).getUnsignedValue(); if(v>=0x006c0000L&&v<=0x00770000L) cands.add(v); }
                    if(o instanceof Address){ long v=((Address)o).getOffset(); if(v>=0x006c0000L&&v<=0x00770000L) cands.add(v); }
                }
            }
            ins=ins.getNext();
        }
        println("candidate .rdata constants: "+cands);
        for(long c:cands){ Address a=toAddr(c); if(validVtable(a)){ vt=a; println("VTABLE FOUND @ "+a); break; } }
        if(vt==null){ println("no vtable among candidates"); return; }
        for(int i=0;i<40;i++){
            long fp=getInt(vt.add(i*4))&0xFFFFFFFFL;
            Function tf=getFunctionAt(toAddr(fp));
            println(String.format("  idx %2d +0x%02x -> %08x %s",i,i*4,fp,tf!=null?tf.getName():"(none)"));
        }
        println("DONE");
    }
}
