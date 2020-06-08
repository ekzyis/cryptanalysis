import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.modi.wrap import padder
from util.bitseq import bitseq8


class TestPadder(unittest.TestCase):
    def test_padder_with_text_smaller_than_blocksize(self):
        _padder = padder(4)
        b = bitseq8(0xfa)
        self.assertEqual(_padder(b), "0xfa")
        _padder = padder(16)
        self.assertEqual(_padder(b), "0x00fa")
        _padder = padder(32)
        self.assertEqual(_padder(b), "0x000000fa")

    def test_padder_with_text_bigger_than_blocksize(self):
        _padder = padder(16)
        b = bitseq8(0xfa, 0xfa, 0xfa)
        self.assertEqual(_padder(b), "0x00fafafa")
        _padder = padder(32)
        b = bitseq8((0xfa,) * 5)
        self.assertEqual(_padder(b), "0x000000fafafafafa")
