import unittest

# noinspection PyUnresolvedReferences
from bitstring import Bits

from util.bitseq import fhex


class TestFullHexStr(unittest.TestCase):
    def test_fhex_with_single_byte(self):
        b = Bits('0xfa')
        self.assertEqual(str(b), '0xfa')
        self.assertEqual(fhex(b), '0xfa')

    def test_fhex_with_max_chars(self):
        # MAX_CHARS is 250 - see bitstring module
        hex_str = "0x" + "f" * 251
        b = Bits(hex_str)
        # show that str(b) does not return full hex string
        self.assertNotEqual(str(b), hex_str)
        self.assertEqual(str(b)[-3:], '...')
        # show that full_hex_str_ returns full hex string
        self.assertEqual(fhex(b), hex_str)
