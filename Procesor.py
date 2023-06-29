import logging
from fetch.Fetch import Fetch
from decode.Decode import Decode
from execute.Execute import Execute
from memory.Mem import Mem
from config.Configurator import Configurator
from config.ConfigurationStrings import MIPS32_STANDARD_CONFIG

log = logging.getLogger(__name__)

class Processor:

    def __init__(self):
        self.configurator = Configurator(MIPS32_STANDARD_CONFIG)
        self.configurator.configure()
        self.fetch = Fetch(self.configurator.imem_cfg)
        self.decode = Decode()
        self.execute = Execute()
        self.memory = Mem(self.configurator.dmem_cfg)

    def run(self):
        print(self.fetch.imem)
        return