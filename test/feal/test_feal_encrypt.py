import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import encrypt


class TestFEALCipherEncrypt(unittest.TestCase):

    def test_encrypt_raises_error_when_text_larger_than_64_bit(self):
        with self.assertRaises(ValueError):
            encrypt(2 ** 64, 0x0)
        try:
            encrypt(2 ** 64 - 1, 0x0)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")

    def test_encrypt_returns_expected_output_as_specified_in_reference(self):
        k = 0x123456789ABCDEF0123456789ABCDEF
        p = 0x0
        c = encrypt(p, k)
        self.assertEqual(c, 0x9C9B54973DF685F8)
