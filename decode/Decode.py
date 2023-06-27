import logging
from .RegisterBank import RegisterBank
from .Idex_reg import IDEX
from execute.ALU import *

log = logging.getLogger(__name__)

# Global constants
OPCODE_LEN = 6
REGISTER_LEN = 5
SHIFT_AMT_LEN = 5
FUNCTION_LEN = 6
IMMEDIATE_LEN = 16
JUMP_ADDR_LEN = 26
MIPS_INSTR_LEN = 32

JMP_OPCODES = [0b000010, 0b000011, 
               0b001001, 0b001000]

IMM_OPCODES = [0b001000, 0b001001,
               0b001100, 0b001101,
               0b001110, 0b001010,
               0b001001]

class Decode:

    def __init__(self):
        # Components
        self.reg_bank = RegisterBank()

        # Input
        self.instruction = 0x0
        
    def run_decode(self, ifid):

        idex = IDEX()

        self.instruction = ifid.instr
        idex.next_instr_addr = ifid.addr
        
        log.info(f"Decoding instruction {bin(self.instruction)} " +
                   f"({hex(self.instruction)})")

        # Break down the instruction
        opcode = self.instruction >> (MIPS_INSTR_LEN - OPCODE_LEN)
        rd1 = \
            (self.instruction & 0x3E00000) >> \
            (REGISTER_LEN*2 + SHIFT_AMT_LEN + FUNCTION_LEN)
        rd2 = \
            (self.instruction & 0x1F0000) >> \
            (REGISTER_LEN + SHIFT_AMT_LEN + FUNCTION_LEN)
        imm = (self.instruction & 0xFFFF)
        wr_reg = \
            (self.instruction & 0xF800) >> (SHIFT_AMT_LEN + FUNCTION_LEN)
        shift_amt = \
            (self.instruction & 0x7C0) >> FUNCTION_LEN
        func_code = (self.instruction & 0x3F)

        log.info("Instruction broken down: \n" +
                 f"opcode = {bin(opcode)}\n" +
                 f"rd1 = {bin(rd1)}\n" +
                 f"rd2 = {bin(rd2)}\n" +
                 f"imm = {bin(imm)}\n" +
                 f"wr_reg = {bin(wr_reg)}\n" +
                 f"shift_amt = {bin(shift_amt)}\n" +
                 f"func_code = {bin(func_code)}")
        
        # Immediate sign extension
        sign_bit = (imm) >> 15
        idex.sigext_imm = imm if not sign_bit else imm | 0xFFFF0000

        # Read registers
        self.reg_bank.read_registers(rd1, rd2)
        idex.rd1_data = self.reg_bank.r1_output
        idex.rd2_data = self.reg_bank.r2_output

        # Set control signals

        # If is an R-type instruction
        if opcode == 0x0:
            idex.wr_reg_en = 0x1
            idex.alu_op = self.__get_alu_op_r(func_code)
        
        # TODO: Map all other available instructions

        if opcode in JMP_OPCODES:
            idex.jump_en = 0x1
        elif opcode in IMM_OPCODES:
            idex.alu_in2_mux_sel = 0x1

        # Write register
        idex.wr_reg = wr_reg
        
        return idex

    def write_register(self, wr_reg, wr_data, wr_en):
        self.reg_bank.write_register(wr_reg, wr_data, wr_en)

    def reset(self):
        self.reg_bank = RegisterBank()
        self.instruction = 0x0

    def __get_alu_op_r(self, func):

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


        
