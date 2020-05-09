import unittest
from unittest import mock
from unittest.mock import call

# noinspection PyUnresolvedReferences
import test.context
from ciphers.modi.ecb import ecb


class TestECB(unittest.TestCase):
    def test_ecb_returns_concatenation_of_cipher_fn_results(self):
        m = 0x1234ABCD5678

        def encrypt(m):
            return m >> 4

        cipher_fn = mock.Mock(wraps=encrypt)
        c = ecb(blocksize=16)(cipher_fn, m, 3 * 16)
        self.assertEqual(cipher_fn.call_count, 3)
        cipher_fn.assert_has_calls([call(0x1234), call(0xABCD), call(0x5678)])
        self.assertEqual(c, 0x01230ABC0567)
