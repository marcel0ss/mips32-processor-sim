import logging
import os
from config.Configurator import Configurator
from memory.Memory import Memory

if __name__ == "__main__":
    print("MIPS Processor Simulator")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    config = "./config/config.json"
    config_handle = Configurator(config)
    config_handle.get_configuration()

    main_mem = Memory(config_handle.mem_cfg)
    main_mem.read_en = True
    main_mem.read(1020)
    print(main_mem.output, hex(main_mem.output))

    main_mem.write_en = True
    main_mem.write(1020, 2478525685)

    main_mem.read(1020)
    print(main_mem.output, hex(main_mem.output))

