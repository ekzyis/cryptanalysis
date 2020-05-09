import unittest
from unittest import mock
from unittest.mock import call

# noinspection PyUnresolvedReferences
import test.context
from ciphers.modi.ecb import ecb


class TestECB(unittest.TestCase):

    def setUp(self):
        self.cipher_fn = lambda k, m: m >> 4

    def test_ecb_returns_concatenation_of_cipher_fn_results(self):
        m = 0x1234ABCD5678
        k = None
        cipher_fn = mock.Mock(wraps=self.cipher_fn)
        c = ecb(blocksize=16)(cipher_fn, k, m, 3 * 16)
        self.assertEqual(cipher_fn.call_count, 3)
        cipher_fn.assert_has_calls([call(k, 0x1234), call(k, 0xABCD), call(k, 0x5678)])
        self.assertEqual(c, 0x01230ABC0567)

    def test_ecb_returns_concatentation_of_cipher_fn_results_with_message_which_has_leading_zero_bits(self):
        m = 0x00123456
        k = None
        cipher_fn = mock.Mock(wraps=self.cipher_fn)
        c = ecb(blocksize=16)(cipher_fn, k, m, 2 * 16)
        self.assertEqual(cipher_fn.call_count, 2)
        cipher_fn.assert_has_calls([call(k, 0x0012), call(k, 0x3456)])
        self.assertEqual(c, 0x00010345)
