import unittest
from config.Configurator import Configurator
from config.ConfigurationStrings import MIPS32_STANDARD_CONFIG
from fetch.Fetch import Fetch

cfg = Configurator(MIPS32_STANDARD_CONFIG)
cfg.configure()
uut = Fetch(cfg.imem_cfg)

class TestFetch(unittest.TestCase):

    def tearDown(self):
        uut.reset()

    def test_normal_fetch_cycle(self):
        cur_addr = 0x0
        # Verify initial state
        self.assertEqual(uut.next_addr, cur_addr)
        
        # Run one fetch cycle
        uut.run_fetch()

        cur_addr += 4
        # Verify that next address is the previous plus 4
        self.assertEqual(uut.next_addr, cur_addr)

        # Run one fetch cycle
        uut.run_fetch()

        cur_addr += 4
        # Verify that next address is the previous plus 4
        self.assertEqual(uut.next_addr, cur_addr)

    def test_reach_eop(self):
        # Test setup
        uut.next_addr = 0x0

        # Verify eop signal is not triggered
        self.assertEqual(uut.eop, False)
        
        # Out of bounds address
        uut.next_addr = 0xfffffff0

        # This cycle triggers the eop flag
        uut.run_fetch() 

        # Verify eop is triggered
        self.assertEqual(uut.eop, True)

    def test_jump(self):
        # Run one normal cycle to show that it is not jumping yet
        uut.run_fetch()
        self.assertEqual(uut.next_addr, 0x4)

        # Select the jump address
        uut.mux_sel = 0x1
        uut.jump_addr = 0xC
        uut.run_fetch()
        # Verify that Mux selected the jump address
        self.assertEqual(uut.mux.output, uut.jump_addr)
