import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.salsa20 import littleendian
from util.word import Word


class TestSalsa20CipherLittleEndian(unittest.TestCase):
    def test_salsa20_littleendian(self):
        self.assertEqual(littleendian(0x0), 0x0)
        self.assertEqual(littleendian(Word(0x56, 0x4b, 0x1e, 0x9, bit=8)), 0x091e4b56)
        self.assertEqual(littleendian(Word(0xff, 0xff, 0xff, 0xfa, bit=8)), 0xfaffffff)

    def test_salsa20_littleendian_raises_value_error_if_input_larger_than_32_bit(self):
        with self.assertRaises(ValueError):
            littleendian(2 ** 32)
        try:
            littleendian(2 ** 32 - 1)
        except ValueError:
            self.fail("littleendian raised unexpected ValueError")
