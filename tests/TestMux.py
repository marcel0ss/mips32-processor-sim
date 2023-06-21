import unittest
from general.Mux import Mux

# 16-input mux
uut_16 = Mux(16)

# 8-input Mux (Pass a 7 and 1 to make sure it corrects it internally)
uut_8 = Mux(7)
uut_1 = Mux(1)


class TestMux(unittest.TestCase):

    def tearDown(self):
        uut_16.select_ctrl = 0x0
        for i in range(len(uut_16.inputs)):
            uut_16.inputs[i] = 0x0

    def test_incorrect_num_inputs(self):
        # Verify that when a Mux is set with a
        # number of inputs that is not a power of 2
        # it automatically corrects it
        self.assertEqual(len(uut_8.inputs), 8)

        # Verify that when specified only one input
        # it is corrected internally
        self.assertEqual(len(uut_1.inputs), 2)

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

    def test_invalid_selection_oob(self):
        sel1 = 16
        sel2 = -1

        # Verify initial state of the select signal
        self.assertEqual(uut_16.select_ctrl, 0x0)

        # Verify invalid selection does not change the signal
        uut_16.select(sel1)
        self.assertEqual(uut_16.select_ctrl, 0x0)
        uut_16.select(sel2)
        self.assertEqual(uut_16.select_ctrl, 0x0)

    def test_valid_selection(self):
        sel1 = 0
        sel2 = 8
        sel3 = 15

        # Valid data
        data_in1 = 0x1A7690FF
        data_in2 = 0x2A7670FE
        data_in3 = 0x3A7690FA

        # Set valid Mux inputs
        uut_16.set_input(sel1, data_in1)
        uut_16.set_input(sel2, data_in2)
        uut_16.set_input(sel3, data_in3)

        # Verify that valid selection, sets the correct output
        uut_16.select(sel1)
        self.assertEqual(uut_16.output, data_in1)

        uut_16.select(sel2)
        self.assertEqual(uut_16.output, data_in2)

        uut_16.select(sel3)
        self.assertEqual(uut_16.output, data_in3)
