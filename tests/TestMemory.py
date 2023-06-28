import unittest
from config.Configurator import Configurator
from config.ConfigurationStrings import MIPS32_STANDARD_CONFIG
from memory.Memory import *

cfg = Configurator(MIPS32_STANDARD_CONFIG)
cfg.configure()
uut = Memory(cfg.dmem_cfg)


class TestMemory(unittest.TestCase):

    def tearDown(self):
        uut.reset_mem()

    # Write operation

    def test_valid_write_not_enabled(self):
        uut.write_en = 0x0
        uut.wr_data = 0xAF0123E4
        uut.address_in = 0x3fc
        # Try to write data at address 0x3fc
        wr_result = uut.write()
        self.assertEqual(wr_result, MEM_WR_NOT_ENABLE)

    def test_valid_write_enabled(self):
        uut.wr_data = 0xAF0123E4
        uut.address_in= 0x3fc
        uut.write_en = 0x1
        # Try to write data at address 0x3fc
        wr_result = uut.write()
        self.assertEqual(wr_result, MEM_SUCCESS)

    def test_invalid_write_invalid_address(self):
        uut.wr_data = 0xAF0123E4
        uut.address_in = -1
        uut.write_en = 0x1

        wr_result_oob_lower = uut.write()
        self.assertEqual(wr_result_oob_lower, MEM_ADDRESS_NOT_FOUND)

        uut.address_in = 1025

        wr_result_oob_upper = uut.write()
        self.assertEqual(wr_result_oob_upper, MEM_ADDRESS_NOT_FOUND)

    def test_invalid_write_missaligned(self):
        uut.wr_data = 0xAF0123E4
        # Missaligned addresses (must be divisible by 4)
        uut.address_in = 0x1
        uut.write_en = True

        wr_result1 = uut.write()
        self.assertEqual(wr_result1, MEM_DATA_MISSALIGNED)

        uut.address_in = 0x3fb

        wr_result2 = uut.write()
        self.assertEqual(wr_result2, MEM_DATA_MISSALIGNED)

    def test_invalid_write_overflow(self):
        # Data that cant be handle by 32 bits
        uut.wr_data = 0xDE21AAC0F1
        uut.address_in = 0x0
        uut.write_en = True

        wr_result1 = uut.write()
        self.assertEqual(wr_result1, MEM_DATA_INVALID)

        uut.wr_data = 0xDE21AAC01

        wr_result2 = uut.write()
        self.assertEqual(wr_result2, MEM_DATA_INVALID)

    # Read operation

    def test_valid_read_not_enabled(self):
        uut.read_en = 0x0

        uut.address_in = 0x0

        rd_result1 = uut.read()
        self.assertEqual(rd_result1, MEM_RD_NOT_ENABLE)
        self.assertEqual(uut.output, 0x0)

        uut.address_in = 0x3fc

        rd_result2 = uut.read()
        self.assertEqual(rd_result2, MEM_RD_NOT_ENABLE)
        self.assertEqual(uut.output, 0x0)

    def test_valid_read_enabled(self):
        uut.read_en = 0x1
        uut.write_en = 0x1

        uut.address_in = 0x0
        uut.wr_data = 0x17FAE301

        uut.write()
        rd_result1 = uut.read()
        self.assertEqual(rd_result1, MEM_SUCCESS)
        self.assertEqual(uut.output, uut.wr_data)

        uut.address_in = 0x3fc
        uut.wr_data = 0x18FA2300

        uut.write()
        rd_result2 = uut.read()
        self.assertEqual(rd_result2, MEM_SUCCESS)
        self.assertEqual(uut.output, uut.wr_data)

    def test_invalid_read_invalid_address(self):
        uut.address_in = -1
        uut.read_en = 0x1

        rd_result_oob_lower = uut.read()
        self.assertEqual(rd_result_oob_lower, MEM_ADDRESS_NOT_FOUND)

        uut.address_in = 1025

        rd_result_oob_upper = uut.read()
        self.assertEqual(rd_result_oob_upper, MEM_ADDRESS_NOT_FOUND)
