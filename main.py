import logging
import os
from config.Configurator import Configurator
from config.ConfigurationStrings import MIPS32_STANDARD_CONFIG

if __name__ == "__main__":
    print("MIPS Processor Simulator")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    config_handle = Configurator(MIPS32_STANDARD_CONFIG)
    config_handle.configure()

# autopep8 --in-place --aggressive --aggressive <filename>
# python3 -m unittest tests/Test*.py
