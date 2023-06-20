# Global Constants
MEM_EMPTY = 0
MEM_RANDOM = 1
MEM_FROM_FILE = 2


class MemoryCfg:

    def __init__(self):
        self.capacity_in_bytes = 0
        self.start = MEM_EMPTY
