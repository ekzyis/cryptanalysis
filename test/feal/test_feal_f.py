import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import f


class TestFEALCipherF(unittest.TestCase):

    def test_f_matches_specification_in_paper(self):
        """In section 5.1 of https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf,
        there are example inputs with the expected output.
        """
        _f = f(0x00FFFF00, 0xFFFF)
        self.assertEqual(_f, 0x10041044)

    def test_f_raises_value_error_when_input_keys_are_not_32_bit(self):
        with self.assertRaises(ValueError):
            f(2 ** 32, 0x0)
        with self.assertRaises(ValueError):
            f(0x0, 2 ** 16)
