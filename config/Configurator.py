import logging
import json
from .MemoryCfg import MemoryCfg

log = logging.getLogger(__name__)

class Configurator:

    def __init__(self, filepath):
        self.filepath = filepath
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



    