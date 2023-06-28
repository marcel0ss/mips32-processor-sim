import logging
from execute.ALU import *

log = logging.getLogger(__name__)

JMP_OPCODES = [0b000010, 0b000011, 
               0b001001, 0b001000]

IMM_OPCODES = [0b001000, 0b001001,
               0b001100, 0b001101,
               0b001010, 0b001001]

BRANCH_OPCODES = [0b000100, 0b000111,
                  0b000110, 0b000101]

class ControlUnit:

    def __init__(self):
        self.wr_reg_en = 0x0
        self.jmp_en = 0x0
        self.dest_reg_mux_sel = 0x0
        self.alu_op = 0x0
        self.alu_in2_mux_sel = 0x0
        self.mem_rd_en = 0x0
        self.mem_wr_en = 0x0
        self.wb_mux_sel = 0x0

    def set_signals(self, opcode, func):

        # R instructions
        if opcode == 0b0:
            self.wr_reg_en = 0x1
            self.jmp_en = 0x0
            self.dest_reg_mux_sel = 0x0
            self.alu_op = self.__set_r_instr_alu_op(func)
            self.alu_in2_mux_sel = 0x0
            self.mem_rd_en = 0x0
            self.mem_wr_en = 0x0
            self.wb_mux_sel = 0x0
            
        elif opcode in IMM_OPCODES:
            self.wr_reg_en = 0x1
            self.jmp_en = 0x0
            self.dest_reg_mux_sel = 0x1
            self.alu_op = self.__set_alu_op(opcode)
            self.alu_in2_mux_sel = 0x1
            self.mem_rd_en = 0x0
            self.mem_wr_en = 0x0
            self.wb_mux_sel = 0x0
        # Store
        elif opcode == 0b101011:
            self.wr_reg_en = 0x0
            self.jmp_en = 0x0
            self.dest_reg_mux_sel = 0x0
            self.alu_op = ALU_ADD_OP
            self.alu_in2_mux_sel = 0x1
            self.mem_rd_en = 0x0
            self.mem_wr_en = 0x1
            self.wb_mux_sel = 0x0
        # Load
        elif opcode == 0b100011:
            self.wr_reg_en = 0x1
            self.jmp_en = 0x0
            self.dest_reg_mux_sel = 0x1
            self.alu_op = ALU_ADD_OP
            self.alu_in2_mux_sel = 0x1
            self.mem_rd_en = 0x1
            self.mem_wr_en = 0x0
            self.wb_mux_sel = 0x1
        # Branches
        elif opcode in BRANCH_OPCODES:
            self.wr_reg_en = 0x0
            self.jmp_en = 0x1
            self.dest_reg_mux_sel = 0x0
            self.alu_op = self.__set_alu_op(opcode)
            self.alu_in2_mux_sel = 0x1
            self.mem_rd_en = 0x0
            self.mem_wr_en = 0x0
            self.wb_mux_sel = 0x0
        

    def __set_alu_op(self, opcode):
        match opcode:
            # Addi / Addiu / Lw / Sw
            case 0b001000 | 0b001001 | 0b100011 | 0b101011:
                return ALU_ADD_OP
            # Andi
            case 0b001100:
                return ALU_AND_OP
            # Ori
            case 0b001101:
                return ALU_OR_OP
            # Xori
            case 0b001110:
                return ALU_XOR_OP
            # Slti / Sltiu
            case 0b001010 | 0b001001:
                return ALU_SLT_OP
            # Beq
            case 0b000100:
                return ALU_BEQ_OP
            # Bgtz
            case 0b000111:
                return ALU_BGTZ_OP
            # Blez
            case 0b000110:
                return ALU_BLEZ_OP
            # Bne
            case 0b000101:
                return ALU_BNE_OP
            
    def __set_r_instr_alu_op(self, func):
        match func:
            # Add / Addu
            case 0b100000 | 0b100001:
                return ALU_ADD_OP
            # And
            case 0b100100:
                return ALU_AND_OP
            # Nor
            case 0b100111:
                return ALU_NOR_OP
            # Or
            case 0b100101:
                return ALU_OR_OP
            # Sllv
            case 0b000100:
                return ALU_SLLV_OP
            # Srav
            case 0b000011:
                return ALU_SRAV_OP
            # Sub / Subu
            case 0b100010 | 0b100011:
                return ALU_SUB_OP
            # Xor
            case 0b100110:
                return ALU_XOR_OP
            # Slt / Sltu
            case 0b101010 | 0b101001:
                return ALU_SLT_OP

