import unittest
from memory.Memory import Memory
from config.Configurator import Configurator

class MemoryTest(unittest.TestCase):
    cfg = Configurator("/home/marcelo/Projects/processor-sim/config/config.json")
    cfg.get_configuration()
    uut = Memory(cfg.mem_cfg)

