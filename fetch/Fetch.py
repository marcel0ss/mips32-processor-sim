import logging
from general.Mux import Mux
from general.Register import Register
from memory.Memory import Memory

log = logging.getLogger(__name__)

class Fetch:

    def __init__(self):
        self.mux = Mux(2)
        self.pc = Register()
        self.imem = Memory()