import unittest
from decode.RegisterBank import RegisterBank

uut = RegisterBank()

class TestRegisterBank(unittest.TestCase):

    def tearDown(self):
        uut.rd1 = 0x0
        uut.rd2 = 0x0
        uut.wr_reg = 0x0
        uut.wr_data = 0x0
        uut.wr_en = False
        uut.r1_output = 0x0
        uut.r2_output = 0x0

        for reg in uut.registers:
            uut.registers[reg].reset()

    def test_invalid_set_register(self):
        ir = 0x20 # Invalid
        r1 = 0xF
        r2 = 0XA

        uut.set_input_register(ir, r1, r2)

        # Verify that the register addresses were not changed
        self.assertNotEqual(ir, uut.rd1)
        self.assertNotEqual(r1, uut.rd2)
        self.assertNotEqual(r2, uut.wr_reg)

    def test_valid_set_register(self):
        # Valid addresses
        r1 = 0x1F
        r2 = 0x0
        r3 = 0xF

        uut.set_input_register(r1, r2, r3)

        # Verify that the register addresses changed
        self.assertEqual(r1, uut.rd1)
        self.assertEqual(r2, uut.rd2)
        self.assertEqual(r3, uut.wr_reg)

    def test_write_not_enabled(self):
        wr_reg = 0x5
        wr_data = 0x6212AF65

        uut.wr_reg = wr_reg

        uut.write_register(wr_data)

        # Verify data was not written when write is not enabled
        self.assertNotEqual(uut.registers[wr_reg].data, wr_data)

    def test_write_invalid_data(self):
        wr_reg = 0x5
        wr_data = 0x6212AF65A

        uut.wr_en = True
        uut.wr_reg = wr_reg

        uut.write_register(wr_data)

        # Verify data was not written when data is > 32 bits
        self.assertNotEqual(uut.registers[wr_reg].data, wr_data)

    def test_valid_write(self):
        wr_reg = 0x5
        wr_data = 0x6212AF65

        uut.wr_en = True
        uut.wr_reg = wr_reg

        uut.write_register(wr_data)

        # Verify data was written when data is correct and write is enabled
        self.assertEqual(uut.registers[wr_reg].data, wr_data)
