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
