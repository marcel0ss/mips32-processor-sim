import logging
from general.Util import Util
from config.Configurator import ARCHITECTURE

log = logging.getLogger(__name__)


class Mux:

    def __init__(self, num_inputs):
        # Create an array that holds the value of the inputs
        self.inputs = self.__init_mux(num_inputs)
        self.select_ctrl = 0x0
        self.output = 0x0

    def __init_mux(self, num_inputs):
        final_num_inputs = num_inputs

        if num_inputs < 2:
            final_num_inputs = 2
            log.warning(
                f"Invalid number of inputs for a Mux ({num_inputs}). " +
                f"Creating a mux with {final_num_inputs} inputs instead")

        if Util.is_not_pwr_of_two(num_inputs):
            final_num_inputs = Util.next_pwr_of_2(num_inputs)
            log.warning(
                f"Number of inputs {num_inputs} is not a power of 2. " +
                f"Creating a mux with {final_num_inputs} inputs instead")

        return [0x0 for _ in range(final_num_inputs)]

    def set_input(self, input, data):

        # Verify the number of input is valid
        if input >= len(self.inputs) or input < 0:
            log.error(f"Input number is invalid ({input}). " +
                      f"Valid options are from 0 to {len(self.inputs) - 1}")
            return

        # Verify data being assigned to input is valid
        if Util.count_min_bits(data) > ARCHITECTURE:
            log.error(
                f"Mux can only handle {ARCHITECTURE} bits data, " +
                f"but data received needs {Util.count_min_bits(data)} bits. " +
                "Unable set the value of the input")
            return

        self.inputs[input] = data

        # Refesh output data if necessary
        if input == self.select_ctrl:
            self.output = self.inputs[input]

    def select(self, sel):

        if sel >= len(self.inputs) or sel < 0:
            log.error(f"Select signal is invalid ({input}). " +
                      f"Valid options are from 0 to {len(self.inputs) - 1}. " +
                      "Signal value remains unchanged")
            return

        self.select_ctrl = sel
        self.output = self.inputs[self.select_ctrl]
