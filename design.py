from myhdl import *
from myhdl import concat

def Fetch(pc,instMem,inst,clk,instType, opCode, rs, rt, rd, sa, function, immediate,res, mux_out, mux_out3, RegWrite,regFile, rd1, rd2,RegDst,stall):
    
    @always(clk.posedge)
    def fetch_behave():
        
        if (stall == 1):
            inst.next = intbv(0)
        if(pc<len(instMem)and stall == 0):
            inst.next = (instMem[pc])
            
        if (inst.next[32:26] == 0b000000):
            instType.next = "R-Type"
            opCode.next =inst.next[32:26]
            rs.next=inst.next[26:21]
            rt.next=inst.next[21:16]
            rd.next=inst.next[16:11]
            sa.next=inst.next[11:6]
            function.next =inst.next[6:0] 
            
        else:
            instType.next = "I-Type"
            opCode.next = inst.next[32:26]
            rs.next=inst.next[26:21]
            rt.next=inst.next[21:16]
            immediate.next=inst.next[16:0]
            if immediate.next[15]:
                res.next = concat(intbv(-1)[16:], immediate.next)
            else:
                res.next = concat(intbv(0)[16:], immediate.next)
        

        rd1.next = regFile[int(rs.next)]
        rd2.next = regFile[int(rt.next)]
        
    return fetch_behave



def ControlUnit(clk,opCode, function, RegDst, ALUSrc, MemToReg, RegWrite, MemWrite,MemRead, Branch, ALUOp):
    
    @always(opCode,function)
    def ControlUnit_behave():
        if(opCode == 0b000000):
            if(function == 0b100000): #ADD
                RegDst.next = 1
                RegWrite.next = 1
                ALUSrc.next = 0
                ALUOp.next = 0b010
                MemWrite.next = 0
                MemRead.next = 0
                MemToReg.next = 0
                Branch.next = 0
            if(function == 0b100010): #SUB
                RegDst.next = 1
                RegWrite.next = 1
                ALUSrc.next = 0
                ALUOp.next = 0b110
                MemWrite.next = 0
                MemRead.next = 0
                MemToReg.next = 0
                Branch.next = 0 
            if(function == 0b110110):  #AND
                RegDst.next = 1
                RegWrite.next = 1
                ALUSrc.next = 0
                ALUOp.next = 0b000
                MemWrite.next = 0
                MemRead.next = 0
                MemToReg.next = 0
                Branch.next = 0
            if(function == 0b110111): #OR
                RegDst.next = 1
                RegWrite.next = 1
                ALUSrc.next = 0
                ALUOp.next = 0b001
                MemWrite.next = 0
                MemRead.next = 0
                MemToReg.next = 0
                Branch.next = 0
            if(function == 0b111000):  #XOR
                RegDst.next = 1
                RegWrite.next = 1
                ALUSrc.next = 0
                ALUOp.next = 0b011
                MemWrite.next = 0
                MemRead.next = 0
                MemToReg.next = 0
                Branch.next = 0
        if(opCode == 0b001000):  #ADDI
            RegDst.next = 0
            RegWrite.next = 1
            ALUSrc.next = 1
            ALUOp.next = 0b010
            MemWrite.next = 0
            MemRead.next = 0
            MemToReg.next = 0
            Branch.next = 0
        if(opCode == 0b100100):  #SUBI
            RegDst.next = 0
            RegWrite.next = 1
            ALUSrc.next = 1
            ALUOp.next = 0b110
            MemWrite.next = 0
            MemRead.next = 0
            MemToReg.next = 0
            Branch.next = 0   
        if(opCode == 0b100011):  #LW
            RegDst.next = 0
            RegWrite.next = 1
            ALUSrc.next = 1
            ALUOp.next = 0b010
            MemWrite.next = 0
            MemRead.next = 1
            MemToReg.next = 1
            Branch.next = 0
        if(opCode == 0b101011):  #SW
            #RegDst = 0
            RegWrite.next = 0
            ALUSrc.next = 1
            ALUOp.next = 0b010
            MemWrite.next = 1
            MemRead.next = 0
            #MemToReg = 0
            Branch.next = 0 
        if(opCode == 0b000100):  #BEQ
            #RegDst = 0
            RegWrite.next = 0
            ALUSrc.next = 0
            ALUOp.next = 0b110
            MemWrite.next = 0
            MemRead.next = 0
            #MemToReg = 0
            Branch.next = 1
    return ControlUnit_behave


def RegisterMux(rt, rd, RegDst, mux_out):
    @always_comb
    def RegisterMux_behave():
        if RegDst.next:
            mux_out.next = rd.next
        else:
            mux_out.next = rt.next

    return RegisterMux_behave

def writeIn_regFile(regFile,rd,rt,RegWrite,RegDst,mux_out3,clk):
    @always(clk.negedge)
    def writeIn_regFile_behave():
        if RegWrite.next:
            if RegDst.next:
                regFile[int(rd.next)] = mux_out3.next
            else:
                regFile[int(rt.next)] = mux_out3.next
    return writeIn_regFile_behave           

def afterReg_Mux(rd2,res,ALUSrc,mux_out2):
    @always(rd2,res,ALUSrc)
    def afterReg_Mux_behave():
        if ALUSrc:
            mux_out2.next = res.next
        else:
            mux_out2.next = rd2.next
            
    return afterReg_Mux_behave        

def ALU(rd1,mux_out2,ALUOp,ALU_res,alu_zeroflag):
    @always(rd1,mux_out2,ALUOp)
    def ALU_behave():
        if(ALUOp == 0b010):
            ALU_res.next = (rd1.next + mux_out2.next) & 0xFFFFFFFF
            if (rd1.next + mux_out2.next) == 0:
                alu_zeroflag.next = 1
            else:
                alu_zeroflag.next = 0
        if(ALUOp == 0b110):
            ALU_res.next = (rd1.next - mux_out2.next) & 0xFFFFFFFF
            if (rd1.next - mux_out2.next) == 0:
                alu_zeroflag.next = 1
            else:
                alu_zeroflag.next = 0
        if(ALUOp == 0b000):
            ALU_res.next = (rd1.next & mux_out2.next) & 0xFFFFFFFF
            if (rd1.next & mux_out2.next) == 0:
                alu_zeroflag.next = 1
            else:
                alu_zeroflag.next = 0
        if(ALUOp == 0b001):
            ALU_res.next = (rd1.next | mux_out2.next) & 0xFFFFFFFF
            if (rd1.next | mux_out2.next) == 0:
                alu_zeroflag.next = 1
            else:
                alu_zeroflag.next = 0
        if(ALUOp == 0b011):
            ALU_res.next = (rd1.next ^ mux_out2.next) & 0xFFFFFFFF
            if (rd1.next ^ mux_out2.next) == 0:
                alu_zeroflag.next = 1
            else:
                alu_zeroflag.next = 0
                
                
    return ALU_behave 

def DM(ALU_res,rd2,MemRead,MemWrite,data,readData):
    @always(ALU_res,rd2,MemRead,MemWrite)
    def DM_behave():
        if MemRead:
            readData.next = data[int(ALU_res)].next
        if MemWrite:
            data[int(ALU_res)].next = rd2.next
    return DM_behave 

def afterDM_mux(readData,ALU_res,MemToReg,mux_out3):
    @always(readData,ALU_res,MemToReg)
    def afterDM_mux_behave():
        if MemToReg:
            mux_out3.next = readData.next
        else:
            mux_out3.next = ALU_res.next
    return afterDM_mux_behave                  


def and_branch(alu_zeroflag,Branch,and_branch_output):
    @always(alu_zeroflag,Branch)
    def and_branch_funct():
        and_branch_output.next = alu_zeroflag.next & Branch.next
    return and_branch_funct 

def shift_left2(res,shift_left2_output):
    @always(res)
    def shift_left2_funct():
        shift_left2_output.next[32:2] = res[30:]
    return shift_left2_funct

def adder(shift_left2_output,pc,Add_res):
    @always(shift_left2_output,pc)
    def adder_behave():
        Add_res.next = (shift_left2_output.next + pc.next) & 0xFFFFFFFF
    return adder_behave

def stall_func(MemRead,MemWrite,clk,stall):
    @always(clk.posedge)
    def stall_func_behave():
        if (MemRead == 1 and MemWrite.next == 1) :
            stall = 1
        elif (MemRead.next == 1 and MemWrite == 1):
            stall = 1
        else:
            stall = 0
    return stall_func_behave       
        
    


       
