REGISTER_MAP = {
    0: "zero",  # Constant zero
    1: "at",    # Reserved for assembler
    2: "v0",    # Expression evaluation
    3: "v1",    # Results of a function
}

class Register:
    
    def __init__(self, num):
        self.num = num
        self.name = REGISTER_MAP[num]
        self.data = 0x0
        self.output = 0x0
