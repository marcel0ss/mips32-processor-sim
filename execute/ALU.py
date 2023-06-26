import logging

log = logging.getLogger(__name__)

class ALU:

    def __init__(self):
        # Inputs
        self.alu_op = 0xF
        self.in1 = 0x0
        self.in2 = 0x0

        # Outputs
        self.zero = False
        self.alu_output = 0x0

    def execute_operation(self):

        log.info(f"ALU received operation code {hex(self.alu_op)}")

        match self.alu_op:
            # Add / Addu / Addi / Addiu / Lw / Sw
            case 0x1:
                self.alu_output = self.in1 + self.in2
            # And / Andi
            case 0x2:
                self.alu_output = self.in1 & self.in2
            # Nor
            case 0x3:
                self.alu_output =  (self.in1 | self.in2) ^ \
                0b11111111111111111111111111111111
            # Or / Ori
            case 0x4:
                self.alu_output = self.in1 | self.in2
            # Sllv
            case 0x5:
                self.alu_output = self.in2 << self.in1
            # Srav
            case 0x6:
                self.alu_output = self.in2 >> self.in1
            # Sub / Subu
            case 0x7:
                self.alu_output = self.in1 - self.in2
            # Xor / Xori
            case 0x8:
                self.alu_output = self.in1 ^ self.in2
            # Slt / Sltu / Slti
            case 0x9:
                self.alu_output = int(self.in1 < self.in2)
            # Beq
            case 0xA:
                self.alu_output = 0x0
                self.zero = (self.in1 == self.in2)
            # Bgtz
            case 0xB:
                self.alu_output = 0x0
                self.zero = (self.in1 > 0)
            # Blez
            case 0xC:
                self.alu_output = 0x0
                self.zero = (self.in1 <= 0)
            # Bne
            case 0xD:
                self.alu_output = 0x0
                self.zero = (self.in1 != self.in2)
            # Default
            case _:
                self.alu_output = 0x0
                log.error(f"ALU operation code {hex(self.alu_op)} " +
                          "not supported yet. Nothing to do")

        