import unittest
from decode.Decode import Decode

uut = Decode()

class TestDecode(unittest.TestCase):

    def tearDown(self):
        uut.reset()

    def test_correct_decode_cycle(self):
        instr = 0xAF128CD1
        uut.instruction = instr
        uut.run_decode()

        # Verify instruction parts are correctly identified
        self.assertEqual(uut.opcode, 0b101011)
        self.assertEqual((uut.instruction&0x3E00000)>>21, 0b11000)
        self.assertEqual((uut.instruction&0x1F0000)>>16, 0b10010)
        self.assertEqual(uut.wr_reg, 0b10001)
        self.assertEqual(uut.shift_amt, 0b10011)
        self.assertEqual(uut.func_code, 0b10001)
        self.assertEqual(uut.imm, 0xFFFF8CD1)
        

