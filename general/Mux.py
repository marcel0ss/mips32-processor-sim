import logging

log = logging.getLogger(__name__)

class Mux:

    def __init__(self, num_inputs):
        # Create an array that holds the value of the inputs
        self.inputs = self.__init_mux(num_inputs)
        self.select = 0x0
        self.output = 0x0

    def __init_mux(self, num_inputs):

        self.inputs = [0x0 for _ in range(num_inputs)]
        

    def select(self, input):
        
        if input >= len(self.inputs):
            log.error(f"Select signal is invalid ({input}). " +
                      f"Valid options are from 0 to {len(self.inputs) - 1}. " +
                      "Output will remain unchanged")
            return
            
        self.output = self.inputs[input]
            