import logging
from .Memory import Memory
from .Memwb_reg import MEMWB

log = logging.getLogger(__name__)

class Mem:

    def __init__(self, dmem_cfg):
        self.dmem = Memory(dmem_cfg)
        
        # Outputs signal
        self.jmp_mux_sel = 0x0
        self.jmp_addr = 0x0

    def run_memory(self, exmem):
        
        memwb = MEMWB()
        self.jmp_mux_sel = exmem.jump_en & exmem.alu_zero
        self.jmp_addr = exmem.shifted_addr

        self.dmem.read_en = exmem.mem_rd_en
        self.dmem.write_en = exmem.mem_wr_en
        self.dmem.address_in = exmem.alu_output
        self.dmem.wr_data = exmem.rd2_data

        self.dmem.run()

        memwb.wr_reg_en = exmem.wr_reg_en
        memwb.mem_rd_output = self.dmem.output
        memwb.alu_output = exmem.alu_output
        memwb.wr_reg_addr = exmem.wr_reg_addr
        memwb.wb_mux_sel = exmem.wb_mux_sel

        