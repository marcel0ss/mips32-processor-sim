class MEMWB:

    def __init__(self):
        self.wr_reg_en = 0x0
        self.mem_rd_output = 0x0
        self.alu_output = 0x0
        self.wr_reg_addr = 0x0
        self.wb_mux_sel = 0x0
        
    def __str__(self):
        return ("MEMWB Register:\n" +
                f"wr_reg_en = {hex(self.wr_reg_en)}\n" +
                f"mem_rd_output = {hex(self.mem_rd_output)}\n" +
                f"alu_output = {hex(self.alu_output)}\n" +
                f"wr_reg_addr = {hex(self.wr_reg_addr)}\n" +
                f"wb_mux_sel = {hex(self.wb_mux_sel)}")