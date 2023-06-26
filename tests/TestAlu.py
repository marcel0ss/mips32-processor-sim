import unittest
from execute.ALU import ALU

uut = ALU()

class TestAlu(unittest.TestCase):

    def tearDown(self):
        uut.alu_op = 0x0
        uut.alu_output = 0x0
        uut.in1 = 0x0
        uut.in2 = 0x0
        uut.zero = False

    def test_add(self):
        uut.in1 = 0x1AF0 
        uut.in2 = 0xE1D3 
        uut.alu_op = 0x1
        uut.execute_operation()
        
        self.assertEqual(uut.alu_output, 0xFCC3)
    
    def test_and(self):
        uut.in1 = 0x1AF0 
        uut.in2 = 0xE1D3
        uut.alu_op = 0x2
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0xD0)

    def test_nor(self):
        uut.in1 = 0x1AF0A012
        uut.in2 = 0xE1D356B1
        uut.alu_op = 0x3
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0x40C094C)

    def test_or(self):
        uut.in1 = 0x1AF0A012
        uut.in2 = 0xE1D356B1
        uut.alu_op = 0x4
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0xFBF3F6B3)

    def test_lshift(self):
        uut.in1 = 0x5
        uut.in2 = 0x1
        uut.alu_op = 0x5
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0x20)

    def test_rshift(self):
        uut.in1 = 0x2
        uut.in2 = 0xF
        uut.alu_op = 0x6
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0x3)

    def test_sub(self):
        uut.in1 = 0x5AFC
        uut.in2 = 0x65D
        uut.alu_op = 0x7
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0x549F)

    def test_xor(self):
        uut.in1 = 0x1AF0A012
        uut.in2 = 0xE1D356B1
        uut.alu_op = 0x8
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0xFB23F6A3)

    def test_slt(self):
        uut.in1 = 0x1AF0A012
        uut.in2 = 0xE1D356B1
        uut.alu_op = 0x9
        uut.execute_operation()

        self.assertEqual(uut.alu_output, 1)

        uut.in1 = 0xE1D356B1
        uut.in2 = 0x1AF0A012

        uut.execute_operation()

        self.assertEqual(uut.alu_output, 0)

    def test_beq(self):
        uut.in1 = 0x1AF0A012
        uut.in2 = 0x1AF0A012
        uut.alu_op = 0xA
        uut.execute_operation()

        self.assertEqual(uut.zero, True)

        uut.in2 = 0xE1D356B1
        uut.execute_operation()

        self.assertEqual(uut.zero, False)

    def test_bgtz(self):
        uut.in1 = 0x1AF0A012
        uut.alu_op = 0xB
        uut.execute_operation()

        self.assertEqual(uut.zero, True)

        uut.in1 = 0x0
        uut.execute_operation()

        self.assertEqual(uut.zero, False)

    def test_blez(self):
        uut.in1 = -0x1AF0A012
        uut.alu_op = 0xC
        uut.execute_operation()

        self.assertEqual(uut.zero, True)

        uut.in1 = 0x0
        uut.execute_operation()

        self.assertEqual(uut.zero, True)

        uut.in1 = 0x1
        uut.execute_operation()

        self.assertEqual(uut.zero, False)

    def test_bne(self):
        uut.in1 = 0x1AF0A012
        uut.in2 = 0x1AF0A01A
        uut.alu_op = 0xD
        uut.execute_operation()

        self.assertEqual(uut.zero, True)

        uut.in2 = 0x1AF0A012
        uut.execute_operation()

        self.assertEqual(uut.zero, False)
