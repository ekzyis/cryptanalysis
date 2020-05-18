import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.salsa20 import quarterround
from util.word import Word


class TestSalsa20CipherQuarterround(unittest.TestCase):
    def test_salsa20_quarterround(self):
        self.assertEqual(quarterround(Word(0x00000000, 0x00000000, 0x00000000, 0x00000000, bit=32)),
                         Word(0x00000000, 0x00000000, 0x00000000, 0x00000000, bit=32))
        self.assertEqual(quarterround(Word(0x00000001, 0x00000000, 0x00000000, 0x00000000, bit=32)),
                         Word(0x08008145, 0x00000080, 0x00010200, 0x20500000, bit=32))
        self.assertEqual(quarterround(Word(0x00000000, 0x00000001, 0x00000000, 0x00000000, bit=32)),
                         Word(0x88000100, 0x00000001, 0x00000200, 0x00402000, bit=32))
        self.assertEqual(quarterround(Word(0x00000000, 0x00000000, 0x00000001, 0x00000000, bit=32)),
                         Word(0x80040000, 0x00000000, 0x00000001, 0x00002000, bit=32))
        self.assertEqual(quarterround(Word(0x00000000, 0x00000000, 0x00000000, 0x00000001, bit=32)),
                         Word(0x00048044, 0x00000080, 0x00010000, 0x20100001, bit=32))
        self.assertEqual(quarterround(Word(0xe7e8c006, 0xc4f9417d, 0x6479b4b2, 0x68c67137, bit=32)),
                         Word(0xe876d72b, 0x9361dfd5, 0xf1460244, 0x948541a3, bit=32))
        self.assertEqual(quarterround(Word(0xd3917c5b, 0x55f1c407, 0x52a58a7a, 0x8f887a3b, bit=32)),
                         Word(0x3e2f308c, 0xd90a8f36, 0x6ab2a923, 0x2883524c, bit=32))
