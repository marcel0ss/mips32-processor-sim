import logging
from config.Configurator import ARCHITECTURE
from general.Util import Util

log = logging.getLogger(__name__)


class Register:

    def __init__(self):
        self.data = 0x0

    def write(self, data):
        # Verify validity of the data to be written
        if Util.count_min_bits(data) > ARCHITECTURE:
            log.error(
                f"Data to be written must be {ARCHITECTURE} bits, " +
                f"but data received needs {Util.count_min_bits(data)} bits. " +
                "Unable to write data")
            return False

        self.data = data
        return True

    def reset(self):
        self.data = 0x0
        self.output = 0x0

    def __str__(self):
        return hex(self.data)
