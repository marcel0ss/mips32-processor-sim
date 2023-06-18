import logging
import json
from .MemoryCfg import MemoryCfg

# Logging
log = logging.getLogger(__name__)

# Global constants
MAX_ARCH_SIZE = 64
MIN_ARCH_SIZE = 8
DEFAULT_ARCH_SIZE = 32

class Configurator:

    def __init__(self, filepath):
        self.filepath = filepath
        self.architecture = DEFAULT_ARCH_SIZE
        self.mem_cfg = MemoryCfg()


    def get_configuration(self):
        # Try to open the JSON configuration file
        try:
            str_cfg = open(self.filepath)
            json_cfg = json.load(str_cfg)
        except:
            log.error(f"File in path {self.filepath} does not exists")
            return False
        
        # Finally check that the file is a JSON file
        if not self.filepath.endswith(".json"):
            log.error("Configuration file must be a JSON file")
            return False
        
        self.__configure_architecture(json_cfg["architecture"])
        valid_mem_cfg = self.__configure_memory(json_cfg["memory"])
        valid_cache_cfg = self.__configure_cache(json_cfg["cache"])

        return valid_mem_cfg and valid_cache_cfg
    
    def __configure_memory(self, mem_cfg):
        mem_capacity = mem_cfg["capacity"]

        if mem_capacity <= 0:
            log.error("Memory size cannot be negative or zero")
            return False
        
        # Verify that the size specified is a power of 2
        is_not_pwr_2 = mem_capacity & (mem_capacity - 1)
        if is_not_pwr_2:
            log.error("Memory size must be a power of 2")
            return False

        self.mem_cfg.capacity_in_bytes = mem_capacity
        return True

    def __configure_cache(self, cache_cfg):
        # TODO: Implement
        return True

    def __configure_architecture(self, arch):
        # Verify that the architecture is between the accepted range
        if arch > MAX_ARCH_SIZE or arch < MIN_ARCH_SIZE:
            log.warning(f"Architecture specified is out of bounds ({MIN_ARCH_SIZE} - {MAX_ARCH_SIZE}). " +
                         f"Using the default value of {DEFAULT_ARCH_SIZE}")
            return
        
        # Verify that the architecture specified is a power of 2
        is_not_pwr_2 = arch & (arch - 1)
        if is_not_pwr_2:
            log.error(f"Architecture must be a power of 2. Using the default archictecture of {DEFAULT_ARCH_SIZE}")
            return

        log.info(f"Architecture set to {arch} bits")
        self.architecture = arch