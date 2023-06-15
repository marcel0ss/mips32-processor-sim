

class Memory:

    def __init__(self, mem_cfg):
        self.capacity = mem_cfg.capacity_in_bytes
        self.cells = ["0"*8 for _ in self.capacity] 
