import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.modi.wrap import padder_wrapper
from util.bitseq import bitseq8


class TestPadder(unittest.TestCase):
    def test_padder_with_text_smaller_than_blocksize(self):
        padder = padder_wrapper(4)
        b = bitseq8(0xfa)
        self.assertEqual(padder(b), "0xfa")
        padder = padder_wrapper(16)
        self.assertEqual(padder(b), "0x00fa")
        padder = padder_wrapper(32)
        self.assertEqual(padder(b), "0x000000fa")

    def test_padder_with_text_bigger_than_blocksize(self):
        padder = padder_wrapper(16)
        b = bitseq8(0xfa, 0xfa, 0xfa)
        self.assertEqual(padder(b), "0x00fafafa")
        padder = padder_wrapper(32)
        b = bitseq8((0xfa,) * 5)
        self.assertEqual(padder(b), "0x000000fafafafafa")
