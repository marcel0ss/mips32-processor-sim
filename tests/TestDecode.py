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
