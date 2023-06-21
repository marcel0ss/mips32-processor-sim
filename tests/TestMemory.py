import unittest
from memory.Memory import Memory
from config.Configurator import Configurator
from config.ConfigurationStrings import MIPS32_STANDARD_CONFIG

cfg = Configurator(MIPS32_STANDARD_CONFIG)
cfg.configure()
uut = Memory(cfg.dmem_cfg)


class TestMemory(unittest.TestCase):

    def tearDown(self):
        uut.reset_mem()

    # Write operation

    def test_valid_write_not_enabled(self):
        uut.write_en = False
        wr_data = 0xAF0123E4
        wr_addr = 0x3fc
        # Try to write data at address 0x3fc
        wr_result = uut.write(wr_addr, wr_data)
        self.assertEqual(wr_result, False)

    def test_valid_write_enabled(self):
        wr_data = 0xAF0123E4
        wr_addr = 0x3fc
        uut.write_en = True
        # Try to write data at address 0x3fc
        wr_result = uut.write(wr_addr, wr_data)
        self.assertEqual(wr_result, True)

    def test_invalid_write_invalid_address(self):
        wr_data = 0xAF0123E4
        wr_addr_oob_lower = -1
        wr_addr_oob_upper = 1025
        uut.write_en = True

        wr_result_oob_lower = uut.write(wr_addr_oob_lower, wr_data)
        self.assertEqual(wr_result_oob_lower, False)

        wr_result_oob_upper = uut.write(wr_addr_oob_upper, wr_data)
        self.assertEqual(wr_result_oob_upper, False)

    def test_invalid_write_missaligned(self):
        wr_data = 0xAF0123E4
        # Missaligned addresses (must be divisible by 4)
        wr_addr1 = 0x1
        wr_addr2 = 0x3fb
        uut.write_en = True

        wr_result1 = uut.write(wr_addr1, wr_data)
        self.assertEqual(wr_result1, False)

        wr_result2 = uut.write(wr_addr2, wr_data)
        self.assertEqual(wr_result2, False)

    def test_invalid_write_overflow(self):
        # Data that cant be handle by 32 bits
        wr_data1 = 0xDE21AAC0F1
        wr_data2 = 0xDE21AAC01
        wr_addr = 0x0
        uut.write_en = True

        wr_result1 = uut.write(wr_addr, wr_data1)
        self.assertEqual(wr_result1, False)

        wr_result2 = uut.write(wr_addr, wr_data2)
        self.assertEqual(wr_result2, False)

    # Read operation

    def test_valid_read_not_enabled(self):
        uut.read_en = False

        rd_addr1 = 0x0
        rd_addr2 = 0x3fc

        rd_result1 = uut.read(rd_addr1)
        self.assertEqual(rd_result1, False)
        self.assertEqual(uut.output, 0x0)

        rd_result2 = uut.read(rd_addr2)
        self.assertEqual(rd_result2, False)
        self.assertEqual(uut.output, 0x0)

    def test_valid_read_enabled(self):
        uut.read_en = True
        uut.write_en = True

        rd_addr1 = 0x0
        rd_addr2 = 0x3fc
        wr_data1 = 0x17FAE301
        wr_data2 = 0x18FA2300

        uut.write(rd_addr1, wr_data1)
        rd_result1 = uut.read(rd_addr1)
        self.assertEqual(rd_result1, True)
        self.assertEqual(uut.output, wr_data1)

        uut.write(rd_addr2, wr_data2)
        rd_result2 = uut.read(rd_addr2)
        self.assertEqual(rd_result2, True)
        self.assertEqual(uut.output, wr_data2)

    def test_invalid_read_invalid_address(self):
        wr_addr_oob_lower = -1
        wr_addr_oob_upper = 1025
        uut.read_en = True

        rd_result_oob_lower = uut.read(wr_addr_oob_lower)
        self.assertEqual(rd_result_oob_lower, False)

        rd_result_oob_upper = uut.read(wr_addr_oob_upper)
        self.assertEqual(rd_result_oob_upper, False)


# Run command: python3 -m unittest tests/TestMemory.py
