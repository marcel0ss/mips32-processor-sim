import logging
from general.Mux import Mux
from general.Register import Register
from memory.Memory import Memory
from config.Configurator import ARCHITECTURE
from memory.Memory import MEM_ADDRESS_NOT_FOUND

log = logging.getLogger(__name__)

# Global constants
MUX_NEXT_ADDR_IN = 0
MUX_JUMP_ADDR_IN = 1
class Fetch:

    def __init__(self, imem_cfg):
        # Components
        self.mux = Mux(2)
        self.pc = Register()
        self.imem = Memory(imem_cfg)
        print(self.imem)

        # Inputs
        self.jump_addr = 0x0
        self.mux_sel = 0x0
        
        # Outputs
        self.next_instr = 0x0

        # Input/Output
        self.next_addr = 0x0

        # Signal to indicate end of program
        self.eop = False

    def run_fetch(self):

        if self.eop:
            log.info("No more instructions found. Reached end of program")
            return

        # Mux 0 -> next instr, no jump
        # Mux 1 -> jump to address
        self.mux.set_input(MUX_NEXT_ADDR_IN, self.next_addr)
        self.mux.set_input(MUX_JUMP_ADDR_IN, self.jump_addr)
        self.mux.select(self.mux_sel)

        log.info(f"Reading from MUX input number {self.mux.select_ctrl}")

        # Set the address in the PC
        self.pc.write(self.mux.output)
        
        # Update next address to be read from imem
        self.next_addr = self.next_addr + (ARCHITECTURE // 8)
        self.mux.set_input(MUX_NEXT_ADDR_IN, self.next_addr)

        # Read instruction at given address from imem
        self.imem.read_en = True
        mem_rd_ret = self.imem.read(self.pc.data)

        if mem_rd_ret == MEM_ADDRESS_NOT_FOUND:
            # Assume that when the address is not found, we have reached eop
            self.eop = True
            return

        log.info(f"Reading next instruction at address {hex(self.pc.data)}. " +
                 f"Found instruction {hex(self.imem.output)}")

        # Update fetch stage outputs
        self.next_instr = self.imem.output

    def reset(self):
        self.mux = Mux(2)
        self.pc = Register()
        self.jump_addr = 0x0
        self.mux_sel = 0x0
        self.next_instr = 0x0
        self.next_addr = 0x0
        self.eop = False

    def __str__(self):
        output_print = (f"Next Instr: {hex(self.next_instr)} " +
                        f"Next Address: {hex(self.next_addr)}")
        return output_print



    