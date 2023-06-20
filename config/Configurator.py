import logging
import json
from .MemoryCfg import MemoryCfg

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
        self.mem_cfg = MemoryCfg()

    def get_configuration(self):
        # Try to open the JSON configuration file
        json_cfg = json.loads(self.json_str)

        self.__configure_architecture(json_cfg["architecture"])
        valid_mem_cfg = self.__configure_memory(json_cfg["memory"])
        valid_cache_cfg = self.__configure_cache(json_cfg["cache"])

        return valid_mem_cfg and valid_cache_cfg

    def __configure_memory(self, mem_cfg):
        mem_capacity = mem_cfg["capacity"]
        mem_init_mode = mem_cfg["start"]

        if mem_capacity <= 0:
            log.error("Memory size cannot be negative or zero")
            return False

        # Verify that the size specified is a power of 2
        is_not_pwr_2 = mem_capacity & (mem_capacity - 1)
        if is_not_pwr_2:
            log.error(
                f"Memory size cannot be of size {mem_capacity}, " +
                "it must be a power of 2")
            return False

        self.mem_cfg.capacity_in_bytes = mem_capacity

        if mem_init_mode in MEM_INIT_MODES:
            self.mem_cfg.start = MEM_INIT_MODES[mem_init_mode]
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
                f"Architecture specified is out of bounds " +
                f"({MIN_ARCH_SIZE} - {MAX_ARCH_SIZE}). " +
                f"Using the default value of {DEFAULT_ARCH_SIZE}")
            return

        # Verify that the architecture specified is a power of 2
        is_not_pwr_2 = arch & (arch - 1)
        if is_not_pwr_2:
            log.error(
                f"Architecture must be a power of 2. " +
                f"Using the default archictecture of {DEFAULT_ARCH_SIZE}")
            return

        log.info(f"Architecture set to {arch} bits")
        ARCHITECTURE = arch
