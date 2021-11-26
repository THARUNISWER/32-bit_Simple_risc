# 32-bit_Simple_RISC
A 32-bit processor in Logisim with a 5-stage pipeline structure.

The various components of the processor can be found in `Simple_risc`. The following stages of the 5-stage pipeline were implemented:
- Instruction Fetch (IF) stage
- Operand Fetch (OF) stage 
- Execute (EX) stage
- Memory Access (MA) stage 
- Read-Write (RW) stage

The ALU, Control Unit, Forwarding Unit, Data Lock Unit and Latches were also implemented and are present in `RiscProcessor.circ`

The SimpleRISC codes that were used to evaluate and benchmark the processor can be found in `Benchmarks`. Additionally, an assembler was created to convert the assembly language code to machine code and can be accessed from the `Assembler.py` file.

