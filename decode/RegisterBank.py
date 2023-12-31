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

        # Outputs
        self.r1_output = 0x0
        self.r2_output = 0x0
        
    def read_registers(self, rd1, rd2):
        if rd1 >= MIPS_NUM_REGISTERS or rd2 > MIPS_NUM_REGISTERS:
            log.error("Unable to set read or write register address. " +
                      "An invalid register address was found. " +
                      "Values must be within the range " +
                      f"0 - {MIPS_NUM_REGISTERS - 1}. " +
                      "Values will remain unchanged")
            return
        
        self.rd1 = rd1
        self.rd2 = rd2
        
        self.r1_output = self.registers[rd1].data
        self.r2_output = self.registers[rd2].data

    def write_register(self, wr_reg, wr_data, wr_en):
        
        # Verify write enable signal is active
        if not wr_en:
            log.error("Unable to write register. " +
                      "Write is not enabled")
            return

        # Verify data is the correct size
        if Util.count_min_bits(wr_data) > ARCHITECTURE:
            log.error("Unable to write register. " +
                      f"Data is larger than {ARCHITECTURE} bits")
            return
        
        self.registers[wr_reg].write(wr_data)

    def __str__(self):
        return (f"rd1 = {self.rd1}\n" +
                f"rd2 = {self.rd2}\n")
        