import logging
import os
from config import Configurator as cfg

if __name__ == "__main__":
    print("MIPS Processor Simulator")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    config = "/home/marcelo/Projects/processor-sim/config/config.json"
    config_handle = cfg.Configurator(config)
    config_handle.get_configuration()

