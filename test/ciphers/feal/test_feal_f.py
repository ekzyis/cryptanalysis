import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import f
from util.bitseq import bitseq32, bitseq16, bitseq


class TestFEALCipherF(unittest.TestCase):

    def test_feal_f_matches_specification_in_paper(self):
        # i/o values taken from p.7, section 5.1 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        _f = f(bitseq32(0x00FFFF00), bitseq16(0xFFFF))
        self.assertEqual(_f, "0x10041044")

    def test_feal_f_raises_value_error_when_input_keys_are_not_correctly_sized(self):
        with self.assertRaises(ValueError):
            a = bitseq(0x0, bit=33)
            b = bitseq16(0x0)
            f(a, b)
        with self.assertRaises(ValueError):
            a = bitseq32(0x0)
            b = bitseq(0x0, bit=17)
            f(a, b)
