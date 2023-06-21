import unittest
from general.Register import Register

uut = Register()


class TestRegister(unittest.TestCase):

    def tearDown(self):
        uut.reset()

    def test_valid_write(self):
        wr_data = 0xAA761F90
        # Verify the previous state, should be 0x0 on the output
        self.assertEqual(uut.output, 0x0)

        # Write new value
        wr_result = uut.write(wr_data)
        self.assertEqual(wr_result, True)

        # Verify actual written value
        uut.read()
        self.assertEqual(uut.output, wr_data)

    def test_invalid_write_invalid_data(self):
        wr_data = 0xAA761F90A1

        # Try to write invalid data
        wr_result = uut.write(wr_data)
        self.assertEqual(wr_result, False)

        # Verify no value was actually written
        uut.read()
        self.assertEqual(uut.output, 0x0)
