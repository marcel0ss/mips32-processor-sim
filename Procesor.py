import logging
from fetch.Fetch import Fetch
from decode.Decode import Decode
from execute.Execute import Execute
from memory.Mem import Mem
from config.Configurator import Configurator
from config.ConfigurationStrings import MIPS32_STANDARD_CONFIG
from general.Mux import Mux

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
        while True:
            fetch_result = self.fetch.run_fetch()
            if self.fetch.eop:
                break
            decode_result = self.decode.run_decode(fetch_result)
            execute_result = self.execute.run_execution(decode_result)
            mem_result = self.memory.run_memory(execute_result)

            # write back
            wb_mux = Mux(2)
            wb_mux.set_input(0, mem_result.alu_output)
            wb_mux.set_input(1, mem_result.mem_rd_output)
            wb_mux.select(mem_result.wb_mux_sel)
            self.decode.reg_bank.write_register(mem_result.wr_reg_addr,
                                                wb_mux.output,
                                                mem_result.wr_reg_en)

        
            for addr, reg in self.decode.reg_bank.registers.items():
                print(hex(addr), hex(reg.data))
