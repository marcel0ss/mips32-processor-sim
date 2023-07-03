class IFID:

    def __init__(self, next_instr, next_addr):
        self.instr = next_instr
        self.addr = next_addr

    def __str__(self):
        return ("IFID Register: \n" +
                f"Instruction: {hex(self.instr)} \n" +
                f"Address: {hex(self.addr)}")