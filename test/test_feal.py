import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import encrypt


class TestFEALCipher(unittest.TestCase):

    def test_encrypt_raises_error_when_text_larger_than_64_bit(self):
        with self.assertRaises(ValueError):
            encrypt(2 ** 64)
        try:
            encrypt(2 ** 64 - 1)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")
