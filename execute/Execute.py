import logging
from .ALU import ALU
from general.Mux import Mux

log = logging.getLogger(__name__)

class Execute:

    def __init__(self):
        self.alu = ALU()
        self.alu_in_mux = Mux(2)
        self.wr_reg_mux = Mux(2)

    def run_execution(self, idex):
        
