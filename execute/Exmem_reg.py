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
        