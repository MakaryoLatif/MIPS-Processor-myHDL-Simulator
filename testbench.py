from myhdl import *
from design import *
import random

def Fetch_test():
    with open('instructions2', 'r') as file:
        instMem = [Signal(intbv(line.strip(), 2)) for line in file]
           

    inst = Signal(intbv(0)[32:])
    pc = Signal(intbv(0)[32:])
    clk = Signal(bool(0))
    instType = Signal(str(""))
    opCode = Signal(intbv(0)[6:])
    rs = Signal(intbv(0)[5:])
    rt = Signal(intbv(0)[5:])
    rd = Signal(intbv(0)[5:])
    sa = Signal(intbv(0)[5:])
    function = Signal(intbv(0)[6:])
    immediate = Signal(intbv(0)[16:])
    rd1 = Signal(intbv(0)[32:])
    rd2 = Signal(intbv(0)[32:])
    RegDst = Signal(bool(0))
    RegWrite = Signal(bool(0))
    ALUSrc = Signal(bool(0))
    ALUOp = Signal(intbv(0)[3:])
    MemWrite = Signal(bool(0))
    MemRead = Signal(bool(0))
    MemToReg = Signal(bool(0))
    Branch = Signal(bool(0))
    mux_out = Signal(intbv(0)[5:])
    mux_out3 = Signal(intbv(0, min=-4294967295, max=4294967296))
    regFile = [
Signal(4),
Signal(5),
Signal(3),
Signal(6),
Signal(7),
Signal(5),
Signal(8),
Signal(7),
Signal(1),
Signal(23),
Signal(55),
Signal(4),
Signal(5),
Signal(65),#60 pc1
Signal(73),
Signal(45),#0 pc2
Signal(16),
Signal(7),
Signal(3),
Signal(22),
Signal(11),
Signal(55),
Signal(15),
Signal(76),
Signal(5),
Signal(3),
Signal(45),
Signal(12),
Signal(23),
Signal(12),
Signal(6),
Signal(0)]
    
    res = Signal(intbv(0)[32:])
    mux_out2 = Signal(intbv(0)[32:])
    ALU_res = Signal(intbv(0, min=-(2**32), max=(2**32)+1))
    readData =Signal(intbv(0)[32:])
    alu_zeroflag = Signal(bool(0))
    and_branch_output = Signal(bool(0))
    shift_left2_output = Signal(intbv(0)[32:])
    Add_res = Signal(intbv(0)[32:])
    stall = Signal(bool(0))
    def generate_DM():
        return Signal(intbv(0)[32:])
    data = [generate_DM() for _ in range(33800)]
    print("data memory array at element 4918 for PC5: {}".format(data[4918]))
    print("data memory array at element 4889 for PC6: {}".format(data[4889]))
    print("data memory array at element 16505 for PC7: {}".format(data[16505]))
    print("data memory array at element 7984 for PC15: {}".format(data[7984]))
    print("data memory array at element 8075 for PC19: {}".format(data[8075]))
    print("data memory array at element 10402 for PC21: {}".format(data[10402]))
    print("data memory array at element 19708 for PC22: {}".format(data[19708]))
    print("data memory array at element 2683 for PC30: {}".format(data[2683]))
    

    @always(delay(10))
    def invertCLK():
        clk.next = not clk
        

    @instance
    def printValues():
        yield delay(50)
        for i in range(len(instMem)+1):
            yield clk.posedge
            if and_branch_output:
                pc.next = Add_res
            else:
                if(pc<len(instMem)):
                    pc.next = pc+1
            instruction_str = "{:032b}".format(int(inst))
            opcode_str = "{:06b}".format(int(opCode))
            rs_str = "{:05b}".format(int(rs))
            rt_str = "{:05b}".format(int(rt))
            rd1_str = "{:04b}".format(int(rd1))
            rd2_str = "{:04b}".format(int(rd2))
            ALU_res_str = "{:032b}".format(int(ALU_res))
            
            print("PC: {}, Instruction: {}, Instruction type: {}, opcode: {}, rs: {}, rt: {},readData1: {},readData2: {}".format(int(pc), instruction_str, instType, opcode_str, rs_str, rt_str,rd1_str,rd2_str))
            if (instType == "I-Type" and (opCode != 0b101011 and opCode != 0b000100)):  
                immediate_str = "{:016b}".format(int(immediate))
                ALUOp_str = "{:03b}".format(int(ALUOp))
                res_str = "{:032b}".format(int(res))
                mux_out2_str = "{:032b}".format(int(mux_out2))
                shift_left2_output_str = "{:032b}".format(int(shift_left2_output))
                print("Immediate: {},RegDst: {}, RegWrite: {}, ALUSrc: {}, ALUOp: {}, MemWrite: {}, MemRead: {}, MemToReg: {}, Branch: {},sign Extension: {},shift_left2_output: {}".format(immediate_str,RegDst,RegWrite,ALUSrc,ALUOp_str,MemWrite,MemRead,MemToReg,int(Branch),res_str,shift_left2_output_str))
                print("mux_out2: {}".format(mux_out2_str))
                
            elif (instType == "I-Type" and (opCode == 0b101011 or opCode == 0b000100)):
                immediate_str = "{:016b}".format(int(immediate))
                ALUOp_str = "{:03b}".format(int(ALUOp))
                res_str = "{:032b}".format(int(res))
                mux_out2_str = "{:032b}".format(int(mux_out2))
                shift_left2_output_str = "{:032b}".format(int(shift_left2_output))
                print("Immediate: {}, RegWrite: {}, ALUSrc: {}, ALUOp: {}, MemWrite: {}, MemRead: {}, Branch: {},sign Extension: {},shift_left2_output: {}".format(immediate_str,RegWrite,ALUSrc,ALUOp_str,MemWrite,MemRead,int(Branch),res_str,shift_left2_output_str))
                print("mux_out2: {}".format(mux_out2_str))
                
            else:
                rd_str = "{:05b}".format(int(rd))
                sa_str = "{:05b}".format(int(sa))
                function_str = "{:06b}".format(int(function))
                ALUOp_str = "{:03b}".format(int(ALUOp))
                mux_out_str = "{:05b}".format(int(mux_out))
                print("rd: {}, sa: {}, function: {}, RegDst: {}, RegWrite: {}, ALUSrc: {}, ALUOp: {}, MemWrite: {}, MemRead: {}, MemToReg: {}, Branch: {},Write register: {}".format(rd_str,sa_str,function_str,RegDst,RegWrite,ALUSrc,ALUOp_str,MemWrite,MemRead,MemToReg,int(Branch),mux_out_str))
                mux_out2_str = "{:032b}".format(int(mux_out2))
                print("mux_out2: {}".format(mux_out2_str))
                
            if MemRead:
                print("read data: {},data memory at ALU_res: {}".format(readData,data[ALU_res]))
            if MemWrite:
                print("data memory at ALU_res: {}".format(data[ALU_res]))
            if RegWrite:
                print("register file at mux_out: {}".format(regFile[mux_out]))
            
            print("ALU_res: {},mux_out3: {},alu_zeroflag: {},and_branch_output: {}".format(ALU_res_str,mux_out3,alu_zeroflag,and_branch_output))
            if and_branch_output:
                print("pc after branching: {},Add_res: {}".format(pc,Add_res))
            print("stall:{}".format(stall))    
            print("")

    fetch_inst = Fetch(pc, instMem, inst, clk,instType, opCode, rs, rt, rd, sa, function, immediate,res, mux_out, mux_out3, RegWrite,regFile, rd1, rd2,RegDst,stall)
    CU_inst = ControlUnit(clk, opCode, function, RegDst, ALUSrc, MemToReg, RegWrite, MemWrite,MemRead, Branch, ALUOp)
    RegisterMux_inst = RegisterMux(rt, rd, RegDst, mux_out)
    afterReg_Mux_inst = afterReg_Mux(rd2,res,ALUSrc,mux_out2)
    ALU_inst = ALU(rd1,mux_out2,ALUOp,ALU_res,alu_zeroflag)
    DM_inst = DM(ALU_res,rd2,MemRead,MemWrite,data,readData)
    afterDM_mux_inst = afterDM_mux(readData,ALU_res,MemToReg,mux_out3)
    and_branch_inst = and_branch(alu_zeroflag,Branch,and_branch_output)
    shift_left2_inst = shift_left2(res,shift_left2_output)
    adder_inst = adder(shift_left2_output,pc,Add_res)
    writeIn_regFile_inst = writeIn_regFile(regFile,rd,rt,RegWrite,RegDst,mux_out3,clk)
    stall_func_inst = stall_func(MemRead,MemWrite,clk,stall)
    
    

    return fetch_inst, invertCLK, printValues, CU_inst, RegisterMux_inst, afterReg_Mux_inst,ALU_inst,DM_inst,afterDM_mux_inst,and_branch_inst,shift_left2_inst,adder_inst,writeIn_regFile_inst,stall_func_inst

def simulate(timesteps):
    tb = traceSignals(Fetch_test)
    sim = Simulation(tb)
    sim.run(timesteps)

simulate(10000)
