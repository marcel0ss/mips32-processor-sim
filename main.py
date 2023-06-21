import logging
import os
from config.Configurator import Configurator
from config.ConfigurationStrings import MIPS32_STANDARD_CONFIG
from fetch.Fetch import Fetch

if __name__ == "__main__":
    print("MIPS Processor Simulator")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    config_handle = Configurator(MIPS32_STANDARD_CONFIG)
    config_handle.configure()

    fetch = Fetch(config_handle.imem_cfg)
    print(fetch.imem)

    fetch.run_fetch()

    fetch.run_fetch()

# autopep8 --in-place --aggressive --aggressive <filename>
