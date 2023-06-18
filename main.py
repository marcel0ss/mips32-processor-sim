import logging
import os
from config.Configurator import Configurator
from memory.Memory import Memory

if __name__ == "__main__":
    print("MIPS Processor Simulator")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    config = "/home/marcelo/Projects/processor-sim/config/config.json"
    config_handle = Configurator(config)
    config_handle.get_configuration()

    main_mem = Memory(config_handle.mem_cfg)
    print(main_mem)
    print(main_mem.get_data_from_address(1020))

