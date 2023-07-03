class IDEX:

    def __init__(self):
        # Control signals
        self.wr_reg_en = 0x0
        self.alu_op = 0x0
        self.jump_en = 0x0
        self.alu_in2_mux_sel = 0x0
        self.dest_reg_mux_sel = 0x0

        # Register bank output
        self.rd1_data = 0x0
        self.rd2_data = 0x0

        # Decoding output
        self.sigext_imm = 0x0
        self.wr_reg1 = 0x0
        self.wr_reg2 = 0x0
        
        # Pass-through signals
        self.next_instr_addr = 0x0
        self.mem_rd_en = 0x0
        self.mem_wr_en = 0x0
        self.wb_mux_sel = 0x0

    def __str__(self):
        return ("IDEX Register:\n" +
                f"wr_reg_en = {hex(self.wr_reg_en)}\n" +
                f"alu_op = {hex(self.alu_op)}\n" +
                f"jump_en = {hex(self.jump_en)}\n" +
                f"alu_in2_mux_sel = {hex(self.alu_in2_mux_sel)}\n" +
                f"dest_reg_mux_sel = {hex(self.dest_reg_mux_sel)}\n" +
                f"rd1_data = {hex(self.rd1_data)}\n" +
                f"rd2_data = {hex(self.rd2_data)}\n" +
                f"sigext_imm = {hex(self.sigext_imm)}\n" +
                f"wr_reg1 = {hex(self.wr_reg1)}\n" +
                f"wr_reg2 = {hex(self.wr_reg2)}\n" +
                f"next_instr_addr = {hex(self.next_instr_addr)}\n" +
                f"mem_rd_en = {hex(self.mem_rd_en)}\n" +
                f"mem_wr_en = {hex(self.mem_wr_en)}\n" +
                f"wb_mux_sel = {hex(self.wb_mux_sel)}")
