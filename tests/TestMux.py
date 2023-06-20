import unittest
from general.Mux import Mux

# 16-input mux
uut_16 = Mux(16)

# 8-input Mux (Pass a 7 to make sure it corrects it internally)
uut_8 = Mux(7)

class TestMux(unittest.TestCase):

    def tearDown(self):
        for i in range(len(uut_16.inputs)):
            uut_16.inputs[i] = 0x0

    def test_incorrect_num_inputs(self):
        # Verify that when a Mux is set with a
        # number of inputs that is not a power of 2
        # it automatically corrects it
        self.assertEqual(len(uut_8.inputs), 8)

    def test_valid_input_set(self):
        # Valid input number for a 16-input Mux
        in1 = 0
        in2 = 8
        in3 = 15

        # Valid data
        data_in1 = 0x1A7690FF
        data_in2 = 0x2A7670FE
        data_in3 = 0x3A7690FA

        # Set valid Mux inputs
        uut_16.set_input(in1, data_in1)
        uut_16.set_input(in2, data_in2)
        uut_16.set_input(in3, data_in3)

        # Verify that the selected inputs changed
        self.assertEqual(uut_16.inputs[in1], data_in1)
        self.assertEqual(uut_16.inputs[in2], data_in2)
        self.assertEqual(uut_16.inputs[in3], data_in3)

    def test_invalid_input_set(self):
        # Invalid inputs
        in1 = -1
        in2 = len(uut_16.inputs)

        # Valid data
        data_in1 = 0x1A7690FF
        data_in2 = 0x2A7670FE

        uut_16.set_input(in1, data_in1)
        uut_16.set_input(in2, data_in2)

        # Verify that no input was affected
        for i in range(len(uut_16.inputs)):
            self.assertEqual(uut_16.inputs[i], 0x0)

    def test_invalid_set_invalid_data(self):
        # Valid inputs
        in1 = 0
        in2 = 15

        # Invalid data
        data_in1 = 0x1A7690FFF
        data_in2 = 0x2A7670FEA1

        uut_16.set_input(in1, data_in1)
        uut_16.set_input(in2, data_in2)

        # Verify that inputs were not affected
        self.assertEqual(uut_16.inputs[in1], 0x0)
        self.assertEqual(uut_16.inputs[in2], 0x0)

    def test_invalid_selection(self):
        sel1 = 16
        sel2 = -1
        # TODO: Finish
        