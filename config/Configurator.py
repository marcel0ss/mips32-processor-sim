import logging
import json
from .MemoryCfg import MemoryCfg
from general.Util import Util

# Logging
log = logging.getLogger(__name__)

# Global constants
MAX_ARCH_SIZE = 64
MIN_ARCH_SIZE = 8
DEFAULT_ARCH_SIZE = 32

MEM_INIT_MODES = {
    "EMPTY": 0,
    "RANDOM": 1,
    "FILE": 2
}

# Variable configurations
ARCHITECTURE = 32


class Configurator:

    def __init__(self, jstr):
        self.json_str = jstr
        self.dmem_cfg = MemoryCfg()
        self.imem_cfg = MemoryCfg()

    def configure(self):
        # Try to open the JSON configuration file
        json_cfg = json.loads(self.json_str)

        self.__configure_architecture(json_cfg["architecture"])
        valid_imem_cfg = self.__configure_memory(json_cfg["imemory"], self.imem_cfg)
        valid_dmem_cfg = self.__configure_memory(json_cfg["dmemory"], self.dmem_cfg)
        valid_cache_cfg = self.__configure_cache(json_cfg["cache"])

        return valid_dmem_cfg and valid_imem_cfg and valid_cache_cfg

    def __configure_memory(self, mem_cfg, mem):
        mem_capacity = mem_cfg["capacity"]
        mem_init_mode = mem_cfg["start"]

        mem.mem_file = mem_cfg["file"]

        if mem_capacity <= 0:
            log.error("Memory size cannot be negative or zero")
            return False

        # Verify that the size specified is a power of 2
        if Util.is_not_pwr_of_two(mem_capacity):
            log.error(
                f"Memory size cannot be of size {mem_capacity}, " +
                "it must be a power of 2")
            return False

        mem.capacity_in_bytes = mem_capacity

        if mem_init_mode in MEM_INIT_MODES:
            mem.start = MEM_INIT_MODES[mem_init_mode]
        else:
            log.warning(
                f"Memory initialization method {mem_init_mode} is not recognized. " +
                "Initializing empty memory. " +
                "Valid options are (RANDOM, EMPTY, FILE)")

        return True

    def __configure_cache(self, cache_cfg):
        # TODO: Implement
        return True

    def __configure_architecture(self, arch):
        global ARCHITECTURE
        # Verify that the architecture is between the accepted range
        if arch > MAX_ARCH_SIZE or arch < MIN_ARCH_SIZE:
            log.warning(
                "Architecture specified is out of bounds " +
                f"({MIN_ARCH_SIZE} - {MAX_ARCH_SIZE}). " +
                f"Using the default value of {DEFAULT_ARCH_SIZE}")
            return

        # Verify that the architecture specified is a power of 2
        if Util.is_not_pwr_of_two(arch):
            log.error(
                "Architecture must be a power of 2. " +
                f"Using the default archictecture of {DEFAULT_ARCH_SIZE}")
            return

        log.info(f"Architecture set to {arch} bits")
        ARCHITECTURE = arch
