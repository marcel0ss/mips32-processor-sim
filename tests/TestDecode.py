import unittest
from decode.Decode import Decode
from fetch.Ifid_reg import IFID
from decode.Idex_reg import IDEX

uut = Decode()

class TestDecode(unittest.TestCase):

    def tearDown(self):
        uut.reset()

    # TODO: Fix test when control signals are fully added
    def test_correct_decode_cycle(self):
        instr = 0xAF128CD1
        idex = uut.run_decode(IFID(instr, 0x0))


    def test_valid_reg_write(self):
        instr = 0xAF128CD1
        wr_data = 0xFA179830
        uut.run_decode(IFID(instr, 0x0))

        uut.write_register(uut.wr_reg, wr_data, True)
        
        # Verify the data was written in the register
        self.assertEqual(uut.reg_bank.registers[uut.wr_reg].data, wr_data)

    def test_reg_write_not_enabled(self):
        instr = 0xAF128CD1
        wr_data = 0xFA179830
        uut.run_decode(IFID(instr, 0x0))

        uut.write_register(uut.wr_reg, wr_data, False)
        
        # Verify the data was written in the register
        self.assertEqual(uut.reg_bank.registers[uut.wr_reg].data, 0x0)
