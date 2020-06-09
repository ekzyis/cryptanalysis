import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import s1
from util.bitseq import bitseq8


class TestFEALCipherS(unittest.TestCase):

    def test_feal_s1_matches_specification_in_paper(self):
        # i/o values taken from p.8, section 5.3 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        s = s1(bitseq8(0b00010011), bitseq8(0b11110010))
        self.assertEqual(s, "0b00011000")
