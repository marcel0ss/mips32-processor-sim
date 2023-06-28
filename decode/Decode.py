import logging
from .RegisterBank import RegisterBank
from .ControlUnit import ControlUnit
from .Idex_reg import IDEX

log = logging.getLogger(__name__)

# Global constants
OPCODE_LEN = 6
REGISTER_LEN = 5
SHIFT_AMT_LEN = 5
FUNCTION_LEN = 6
IMMEDIATE_LEN = 16
JUMP_ADDR_LEN = 26
MIPS_INSTR_LEN = 32

class Decode:

    def __init__(self):
        # Components
        self.reg_bank = RegisterBank()
        self.control_unit = ControlUnit()

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
        
        self.control_unit.set_signals(opcode, func_code)
        
        # Immediate sign extension
        sign_bit = (imm) >> 15
        idex.sigext_imm = imm if not sign_bit else imm | 0xFFFF0000

        # Read registers
        self.reg_bank.read_registers(rd1, rd2)
        idex.rd1_data = self.reg_bank.r1_output
        idex.rd2_data = self.reg_bank.r2_output

        idex.wr_reg_en = self.control_unit.wr_reg_en
        idex.alu_op = self.control_unit.alu_op
        idex.jump_en = self.control_unit.jmp_en
        idex.alu_in2_mux_sel = self.control_unit.alu_in2_mux_sel
        idex.wr_reg1 = wr_reg
        idex.wr_reg2 = rd2
        idex.dest_reg_mux_sel = self.control_unit.dest_reg_mux_sel
        idex.mem_rd_en = self.control_unit.mem_rd_en
        idex.mem_wr_en = self.control_unit.mem_wr_en
        idex.wb_mux_sel = self.control_unit.wb_mux_sel

        return idex

    def write_register(self, wr_reg, wr_data, wr_en):
        self.reg_bank.write_register(wr_reg, wr_data, wr_en)

    def reset(self):
        self.reg_bank = RegisterBank()
        self.instruction = 0x0
