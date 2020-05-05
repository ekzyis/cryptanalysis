import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import fk


class TestFEALCipherFk(unittest.TestCase):

    def test_fk_returns_expected_output_as_specificed_in_reference(self):
        """In section 5.2 of https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf,
        there are example inputs with the expected output.
        """
        f = fk(0x00000000, 0x00000000)
        self.assertEqual(f, 0x10041044)
