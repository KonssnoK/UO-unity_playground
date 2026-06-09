// Disassemble a function (env FUNC_ADDR) so we can see exact compare/branch ops.
//@category Analysis
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Instruction;

public class AsmDump extends GhidraScript {
    @Override public void run() throws Exception {
        String s = System.getenv("FUNC_ADDR");
        long a = Long.parseLong(s, 16);
        Address start = toAddr(a);
        Function f = getFunctionContaining(start);
        println("=== " + (f!=null?f.getName():"?") + " @ " + start + " ===");
        Instruction ins = getInstructionAt(start);
        int n=0;
        while (ins != null && f != null && getFunctionContaining(ins.getAddress())==f && n++<400) {
            StringBuilder sb=new StringBuilder();
            sb.append(ins.getAddress()).append("  ").append(ins.toString());
            println(sb.toString());
            ins = ins.getNext();
        }
        println("DONE");
    }
}
