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

        log.info(f"ALU received operation code {hex(self.alu_op)}")

        match self.alu_op:
            # Add / Addu / Addi / Addiu / Lw / Sw
            case 0x20 | 0x21 | 0x23 | 0x2B | 0x8 | 0x9:
                self.alu_output = self.in1 + self.in2
            # And / Andi
            case 0x24 | 0xC:
                self.alu_output = self.in1 & self.in2
            # Nor
            case 0x27:
                self.alu_output = not (self.in1 | self.in2)
            # Or / Ori
            case 0x25 | 0xD:
                self.alu_output = self.in1 | self.in2
            # Sllv
            case 0x0:
                self.alu_output = self.in2 << self.in1
            # Srav
            case 0x7:
                self.alu_output = self.in2 >> self.in1
            # Sub / Subu
            case 0x22:
                self.alu_output = self.in1 = self.in2
            # Xor / Xori
            case 0x26 | 0xE:
                self.alu_output = self.in1 ^ self.in2
            # Slt / Sltu / Slti
            case 0x2A | 0xA | 0x29:
                self.alu_output = self.in1 < self.in2
            # Beq
            case 0x4:
                self.alu_output = abs(self.in1 - self.in2)
            # Bgtz
            case 0x7:
                self.alu_output = not (self.in1 > 0)
            # Blez
            case 0x6:
                self.alu_output = not (self.in1 <= 0)
            # Bne
            case 0x5:
                self.alu_output = not (self.in1 != self.in2)
            # Default
            case _:
                self.alu_output = 0x0
                log.error(f"ALU operation code {hex(self.alu_op)} " +
                          "not supported yet. Nothing to do")

        if not self.alu_output:
            self.zero = True
        