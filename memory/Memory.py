import logging
import random
from config.Configurator import ARCHITECTURE
from config.MemoryCfg import MEM_EMPTY, MEM_RANDOM, MEM_FROM_FILE
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
        # Components
        self.capacity = mem_cfg.capacity_in_bytes
        self.cells = {}
        self.mem_file = mem_cfg.mem_file
        self.__init_mem(mem_cfg)
        
        # Output
        self.output = 0x0

        # Inputs
        self.read_en = 0x0
        self.write_en = 0x0
        self.address_in = 0x0
        self.wr_data = 0x0

    def run(self):
        if self.read_en:
            return self.read()
        elif self.write_en:
            return self.write()

    def read(self):

        # If the memory is not enabled for reading, do nothing
        if not self.read_en:
            self.output = 0x0
            log.warning("Read is not enabled in memory")
            return MEM_RD_NOT_ENABLE

        # Verify the adress is valid and exists
        if self.address_in not in self.cells:
            log.error("Memory address not found while trying READ operation")
            return MEM_ADDRESS_NOT_FOUND

        # Read the data from memory
        read_data = 0x0
        cells_to_read = ARCHITECTURE // 8
        for cur_addr in range(self.address_in, self.address_in + cells_to_read):
            read_data |= self.cells[cur_addr]
            read_data <<= 8

        self.output = (read_data >> 8)
        return MEM_SUCCESS

    def write(self):

        # If the memory is not enabled for writing, do nothing
        if not self.write_en:
            log.warning("Write is not enabled in memory")
            return MEM_WR_NOT_ENABLE

        # Verify the adress is valid and exists
        if self.address_in not in self.cells:
            log.error(
                f"Memory address {hex(self.address_in)} not found while trying WRITE operation")
            return MEM_ADDRESS_NOT_FOUND

        # Verify correct alignment
        if not self.__is_aligment_correct(self.address_in):
            log.error("Write operation could not be performed. " +
                      "Address is missaligned")
            return MEM_DATA_MISSALIGNED

        # Verify validity of the data to be written
        if Util.count_min_bits(self.wr_data) > ARCHITECTURE:
            log.error(
                f"Data to be written must be {ARCHITECTURE} bits, " +
                f"but data received needs {Util.count_min_bits(self.wr_data)} bits. " +
                "Unable to write data")
            return MEM_DATA_INVALID

        # Write data into memory
        cells_to_write = ARCHITECTURE // 8
        shift_amt = ARCHITECTURE - 8
        for i in range(cells_to_write):
            self.cells[self.address_in + i] = (self.wr_data >> shift_amt) & 0xFF
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
        # Empty
        if mem_cfg.start == MEM_EMPTY:
            self.cells = {i: 0 for i in range(self.capacity)}
        # Read from file
        elif mem_cfg.start == MEM_FROM_FILE:
            instr_file = open(self.mem_file, 'r')
            instructions = instr_file.readlines()
            addr = 0x0
            for i in instructions:
                int_instr = int(i.strip(), 2) 
                self.cells[addr] = (int_instr&0xFF000000) >> 24
                self.cells[addr+1] = (int_instr&0xFF0000) >> 16
                self.cells[addr+2] = (int_instr&0xFF00) >> 8
                self.cells[addr+3] = (int_instr&0xFF)
                addr += 4
        # Random
        else: 
            self.cells = {
                i: random.randint(0, 255)
                for i in range(self.capacity)}

    def __str__(self):
        print_data = ""
        for addr, data in self.cells.items():
            print_data += (hex(addr) + " " + hex(data)) + "\n"
        return print_data
