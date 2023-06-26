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
        self.shift_amt = 0x0
        self.wr_reg = 0x0
        
        # Pass-through signals
        self.next_instr_addr = 0x0
