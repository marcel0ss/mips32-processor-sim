import logging
import random
from config.Configurator import ARCHITECTURE
from config.MemoryCfg import MEM_EMPTY, MEM_RANDOM, MEM_FROM_FILE

log = logging.getLogger(__name__)

class Memory:

    def __init__(self, mem_cfg):
        self.capacity = mem_cfg.capacity_in_bytes
        self.init_mem(mem_cfg)
        self.read_en = False
        self.write_en = False
        self.output = 0
    
    def read(self, address):

        # If the memory is not enabled for reading, do nothing
        if not self.read_en:
            log.error("Read is not enabled in memory")
            return
        
        # Verify the adress is valid and exists
        if address in self.cells:
            log.error("Memory address not found while trying READ operation")
            return
        
        # Read the data from memory
        read_data = ""
        cells_to_read = ARCHITECTURE / 8
        for cur_addr in range(address, address + cells_to_read):
            read_data += self.cells[cur_addr]
        
        self.output = read_data

    def write(self, address, data):

        # If the memory is not enabled for writing, do nothing
        if not self.write_en:
            log.error("Write is not enabled in memory")
            return
        
        # Verify the adress is valid and exists
        if address in self.cells:
            log.error("Memory address not found while trying WRITE operation")
            return
        
        # Verify correct alignment
        if not self.__is_aligment_correct(address):
            log.error("Write operation could not be performed." +
                      "Address is missaligned")
            return

        wr_data = data
        # Verify validity of the data to be written
        if len(data) != ARCHITECTURE:
            log.warning(f"Data to be written must have a size of {ARCHITECTURE}," +
                        f"but data received has a size of {len(data)}." +
                        "Filling up data with zeros")
            missing_len = ARCHITECTURE - len(data)
            fixed_data = missing_len*"0" + data
            wr_data = fixed_data

        # Write data into memory
        split_wr_data = [wr_data[i:i+8] for i in range(0, len(wr_data), 8)]
        for i in range(len(split_wr_data)):
            self.cells[address + i] = split_wr_data[i]

    def __is_aligment_correct(self, address):
        # Convert the address to integer
        int_addr = int(address, 16)
        div = ARCHITECTURE / 8
        # If alignment is correct, the operation output 0, so invert the result
        return not int_addr % div
    
    def init_mem(self, mem_cfg):
        if mem_cfg.start == MEM_EMPTY:
            self.cells = {i:0 for i in range(self.capacity)}
        elif mem_cfg.start == MEM_RANDOM:
            # Calculate the maximum number possible with the architecture size
            max_num_possible = ((1 << ARCHITECTURE) - 1)
            self.cells = {i:random.randint(0, max_num_possible) for i in range(self.capacity)}
        # TODO: Implement starting memory from file

    # TODO: Remove method, testing only
    def get_data_from_address(self, address):
        cells_to_print = ARCHITECTURE // 8
        print_data = ""
        for i in range(cells_to_print):
            print_data += (hex(address + i) + " " + hex(self.cells[address + i])) + "\n"
        return print_data

    def __str__(self):
        print_data = ""
        for addr, data in self.cells.items():
            print_data += (hex(addr) + " " + hex(data)) + "\n"
        return print_data