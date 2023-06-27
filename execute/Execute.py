import logging
from .ALU import ALU
from general.Mux import Mux
from .Exmem_reg import EXMEM

log = logging.getLogger(__name__)

class Execute:

    def __init__(self):
        self.alu = ALU()
        self.alu_in_mux = Mux(2)
        self.wr_reg_mux = Mux(2)

    def run_execution(self, idex):
        # Set muxes
        self.alu_in_mux.set_input(0, idex.rd2_data)
        self.alu_in_mux.set_input(1, idex.sigext_imm)
        self.alu_in_mux.select(idex.alu_in2_mux_sel)

        self.wr_reg_mux.set_input(0, idex.wr_reg)
        self.wr_reg_mux.set_input(1, idex.shift_amt)
        self.wr_reg_mux.select(idex.dest_reg_mux_sel)

        # Set up ALU
        self.alu.alu_op = idex.alu_op
        self.alu.in1 = idex.rd1_data
        self.alu.in2 = self.alu_in_mux.output

        # Execute
        self.alu.execute_operation()

        # Set up signals for next stage
        exmem = EXMEM()
        exmem.shifted_addr = idex.next_instr_addr + \
                            (idex.sigext_imm << 2)
        exmem.alu_zero = self.alu.zero
        exmem.alu_output = self.alu.alu_output
        exmem.rd2_data = idex.rd2_data
        exmem.wr_reg_addr = self.wr_reg_mux.output
        exmem.wr_reg_en = idex.wr_reg_en
        exmem.jump_en = idex.jump_en

        return exmem



