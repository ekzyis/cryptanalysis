import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.modi.wrap import padder
from util.bitseq import bitseq8, bitseq16


class TestPadder(unittest.TestCase):
    def test_padder_with_no_leading_zeros(self):
        _padder = padder(4)
        b = bitseq8(0xfa)
        self.assertEqual(_padder(b), "0xfa")
        _padder = padder(16)
        self.assertEqual(_padder(b), "0x00fa")
        _padder = padder(32)
        self.assertEqual(_padder(b), "0x000000fa")

    def test_padder_with_leading_zeros(self):
        _padder = padder(4)
        b = bitseq16(0x00fa)
        self.assertEqual(_padder(b), "0x00fa")
        _padder = padder(16)
        self.assertEqual(_padder(b), "0x00fa")
        _padder = padder(32)
        self.assertEqual(_padder(b), "0x000000fa")
