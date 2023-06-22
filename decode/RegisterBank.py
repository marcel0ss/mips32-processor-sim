import logging
from general.Register import Register
from config.Configurator import ARCHITECTURE
from general.Util import Util

log = logging.getLogger(__name__)

# Global constants
MIPS_NUM_REGISTERS = 32

class RegisterBank:

    def __init__(self):
        # Setup all 32 registers
        self.registers = {i:Register() for i in range(MIPS_NUM_REGISTERS)}

        # Inputs
        self.rd1 = 0x0
        self.rd2 = 0x0
        self.wr_reg = 0x0
        self.wr_data = 0x0
        self.wr_en = False

        # Outputs
        self.r1_output = 0x0
        self.r2_output = 0x0
        
    def read_registers(self):
        self.r1_output = self.registers[self.rd1]
        self.r2_output = self.registers[self.rd2]

    def set_input_register(self, rd1, rd2, wr):
        if rd1 >= MIPS_NUM_REGISTERS or rd2 > MIPS_NUM_REGISTERS \
           or wr > MIPS_NUM_REGISTERS:
            log.error("Unable to set read or write register address. " +
                      f"An invalid register address was found. " +
                      f"Values must be within the range 0 - {MIPS_NUM_REGISTERS - 1}. " +
                      "Values will remain unchanged")
            return
        
        self.rd1 = rd1
        self.rd2 = rd2
        self.wr_reg = wr

    def write_register(self, wr_data):
        
        # Verify write enable signal is active
        if not self.wr_en:
            log.error("Unable to write register. " +
                      "Write is not enabled")
            return

        # Verify data is the correct size
        if Util.count_min_bits(wr_data) > ARCHITECTURE:
            log.error("Unable to write register. " +
                      f"Data is larger than {ARCHITECTURE} bits")
            return
        
        self.registers[self.wr_reg] = wr_data
        