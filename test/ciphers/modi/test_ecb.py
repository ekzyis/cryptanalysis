import unittest
from unittest import mock
from unittest.mock import call

# noinspection PyUnresolvedReferences
from bitstring import Bits

from ciphers.modi.ecb import ecb


class TestECB(unittest.TestCase):

    def setUp(self):
        self.cipher_fn = mock.Mock(wraps=lambda k, m: m >> 4)

    def test_ecb_blocksize_16_with_no_remainder_in_blocks(self):
        m, k = Bits("0x1234ABCD5678"), None
        cipher_fn = self.cipher_fn
        c = ecb(cipher_fn, blocksize=16)(k, m)
        self.assertEqual(cipher_fn.call_count, 3)
        cipher_fn.assert_has_calls([call(k, Bits("0x1234")), call(k, Bits("0xABCD")), call(k, Bits("0x5678"))])
        self.assertEqual(c, Bits("0x01230ABC0567"))

    def test_ecb_blocksize_16_with_message_which_has_leading_zeroes(self):
        m, k = Bits("0x00123456"), None
        cipher_fn = self.cipher_fn
        c = ecb(cipher_fn, blocksize=16)(k, m)
        self.assertEqual(cipher_fn.call_count, 2)
        cipher_fn.assert_has_calls([call(k, Bits("0x0012")), call(k, Bits("0x3456"))])
        self.assertEqual(c, Bits("0x00010345"))

    def test_ecb_blocksize_16_with_message_which_has_remainder(self):
        m, k = Bits("0x12ABCD"), None
        cipher_fn = self.cipher_fn
        c = ecb(cipher_fn, blocksize=16)(k, m)
        self.assertEqual(cipher_fn.call_count, 2)
        cipher_fn.assert_has_calls([call(k, Bits("0x0012")), call(k, Bits("0xABCD"))])
        self.assertEqual(c, Bits("0x00010ABC"))
