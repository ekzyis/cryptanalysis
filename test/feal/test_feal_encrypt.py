import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import encrypt, encrypt_preprocessing


class TestFEALCipherEncrypt(unittest.TestCase):

    def test_encrypt_raises_error_when_text_larger_than_64_bit(self):
        with self.assertRaises(ValueError):
            encrypt(2 ** 64, 0x0)
        try:
            encrypt(2 ** 64 - 1, 0x0)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")

    def test_encrypt_raises_error_when_key_larger_than_128_bit(self):
        with self.assertRaises(ValueError):
            encrypt(0, 2 ** 128)
        try:
            encrypt(0, 2 ** 128 - 1)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")

    def test_encrypt_returns_expected_output_as_specified_in_reference(self):
        k = 0x123456789ABCDEF0123456789ABCDEF
        p = 0x0
        c = encrypt(p, k)
        self.assertEqual(c, 0x9C9B54973DF685F8)

    def test_encrypt_preprocessing_returns_expected_output_as_specified_in_reference(self):
        k32, k33, k34, k35 = 0x196A, 0x9AB1, 0xE015, 0x8190
        p = 0x0
        out = encrypt_preprocessing(p, [k32, k33, k34, k35])
        self.assertEqual(out, 0x196A9AB1F97F1B21)
