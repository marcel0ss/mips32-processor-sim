import logging

log = logging.getLogger(__name__)

class ALU:

    def __init__(self):
        # Inputs
        self.alu_op = 0x0
        self.in1 = 0x0
        self.in2 = 0x0

        # Outputs
        self.zero = False
        self.alu_output = 0x0

    def execute_operation(self):

        match self.alu_op:
            # Add / Addu / Addi / Addiu
            case [0x20, 0x21, 0x8, 0x9]:
                self.alu_output = self.in1 + self.in2
            # And / Andi
            case [0x24, 0xC]:
                self.alu_output = self.in1 & self.in2
            # Nor
            case 0x27:
                self.alu_output = not (self.in1 | self.in2)
            # Or / Ori
            case [0x25, 0xD]:
                self.alu_output = self.in1 | self.in2
            # Sllv
            case 0x0:
                self.alu_output = self.in2 << self.in1
            # Srav
            case 0x7:
                self.alu_output = self.in2 >> self.in1
            # Sub / Subu
            case [0x22, 0x23]:
                self.alu_output = self.in1 = self.in2
            # Xor / Xori
            case [0x26, 0xE]:
                self.alu_output = self.in1 ^ self.in2

        if not self.alu_output:
            self.zero = True
        
