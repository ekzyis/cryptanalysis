import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import fk


class TestFEALCipherFk(unittest.TestCase):

    def test_fk_matches_specification_in_paper(self):
        """In section 5.2 of https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf,
        there are example inputs with the expected output.
        """
        f = fk(0x0, 0x0)
        self.assertEqual(f, 0x10041044)

    def test_fk_raises_value_error_when_input_keys_are_not_32_bit(self):
        with self.assertRaises(ValueError):
            fk(2 ** 32, 0x0)
        with self.assertRaises(ValueError):
            fk(0x0, 2 ** 32)
