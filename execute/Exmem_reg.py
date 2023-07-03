class EXMEM:

    def __init__(self):
        # Execution output
        self.shifted_addr = 0x0
        self.alu_zero = 0x0
        self.alu_output = 0x0
        self.rd2_data = 0x0
        self.wr_reg_addr = 0x0

        # Control signals
        self.wr_reg_en = 0x0
        self.jump_en = 0x0
        self.mem_wr_en = 0x0
        self.mem_rd_en = 0x0
        self.wb_mux_sel = 0x0
        
    def __str__(self):
        return ("EXMEM Register:\n" +
                f"shifted_addr = {hex(self.shifted_addr)}\n" +
                f"alu_zero = {hex(self.alu_zero)}\n" +
                f"alu_output = {hex(self.alu_output)}\n" +
                f"rd2_data = {hex(self.rd2_data)}\n" +
                f"wr_reg_addr = {hex(self.wr_reg_addr)}\n" +
                f"wr_reg_en = {hex(self.wr_reg_en)}\n" +
                f"jump_en = {hex(self.jump_en)}\n" +
                f"mem_wr_en = {hex(self.mem_wr_en)}\n" +
                f"mem_rd_en = {hex(self.mem_rd_en)}\n" +
                f"wb_mux_sel = {hex(self.wb_mux_sel)}\n")