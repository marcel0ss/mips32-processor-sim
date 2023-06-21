import logging
import random
from config.Configurator import ARCHITECTURE
from config.MemoryCfg import MEM_EMPTY, MEM_RANDOM
from general.Util import Util

log = logging.getLogger(__name__)

# Memory return codes
MEM_SUCCESS = 0
MEM_RD_NOT_ENABLE = 1
MEM_ADDRESS_NOT_FOUND = 2
MEM_WR_NOT_ENABLE = 3
MEM_DATA_MISSALIGNED = 4
MEM_DATA_INVALID = 5

class Memory:

    def __init__(self, mem_cfg):
        self.capacity = mem_cfg.capacity_in_bytes
        self.__init_mem(mem_cfg)
        self.read_en = False
        self.write_en = False
        self.output = 0x0

    def read(self, address):

        # If the memory is not enabled for reading, do nothing
        if not self.read_en:
            log.error("Read is not enabled in memory")
            return MEM_RD_NOT_ENABLE

        # Verify the adress is valid and exists
        if address not in self.cells:
            log.error("Memory address not found while trying READ operation")
            return MEM_ADDRESS_NOT_FOUND

        # Read the data from memory
        read_data = 0x0
        cells_to_read = ARCHITECTURE // 8
        for cur_addr in range(address, address + cells_to_read):
            read_data |= self.cells[cur_addr]
            read_data <<= 8

        self.output = (read_data >> 8)
        return MEM_SUCCESS

    def write(self, address, data):

        # If the memory is not enabled for writing, do nothing
        if not self.write_en:
            log.error("Write is not enabled in memory")
            return MEM_WR_NOT_ENABLE

        # Verify the adress is valid and exists
        if address not in self.cells:
            log.error(
                f"Memory address {hex(address)} not found while trying WRITE operation")
            return MEM_ADDRESS_NOT_FOUND

        # Verify correct alignment
        if not self.__is_aligment_correct(address):
            log.error("Write operation could not be performed. " +
                      "Address is missaligned")
            return MEM_DATA_MISSALIGNED

        # Verify validity of the data to be written
        if Util.count_min_bits(data) > ARCHITECTURE:
            log.error(
                f"Data to be written must be {ARCHITECTURE} bits, " +
                f"but data received needs {Util.count_min_bits(data)} bits. " +
                "Unable to write data")
            return MEM_DATA_INVALID

        # Write data into memory
        cells_to_write = ARCHITECTURE // 8
        shift_amt = ARCHITECTURE - 8
        for i in range(cells_to_write):
            self.cells[address + i] = (data >> shift_amt) & 0xFF
            shift_amt -= 8

        return MEM_SUCCESS

    def reset_mem(self):
        self.read_en = False
        self.write_en = False
        self.output = 0x0
        self.cells = {i: random.randint(0, 255) for i in range(self.capacity)}

    def __is_aligment_correct(self, address):
        # Convert the address to integer
        div = ARCHITECTURE // 8
        # If alignment is correct, the operation output 0, so invert the result
        return not address % div

    def __init_mem(self, mem_cfg):
        if mem_cfg.start == MEM_EMPTY:
            self.cells = {i: 0 for i in range(self.capacity)}
        elif mem_cfg.start == MEM_RANDOM:
            self.cells = {
                i: random.randint(0, 255)
                for i in range(self.capacity)}
        # TODO: Implement starting memory from file

    def __str__(self):
        print_data = ""
        for addr, data in self.cells.items():
            print_data += (hex(addr) + " " + hex(data)) + "\n"
        return print_data
