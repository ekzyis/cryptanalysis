import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.salsa20 import quarterround
from util.word import Word


class TestSalsa20CipherEncrypt(unittest.TestCase):
    def test_salsa20_quarterround(self):
        self.assertEqual(quarterround(Word(0x00000000, 0x00000000, 0x00000000, 0x00000000)),
                         Word(0x00000000, 0x00000000, 0x00000000, 0x00000000))
        self.assertEqual(quarterround(Word(0x00000001, 0x00000000, 0x00000000, 0x00000000)),
                         Word(0x08008145, 0x00000080, 0x00010200, 0x20500000))
        self.assertEqual(quarterround(Word(0x00000000, 0x00000001, 0x00000000, 0x00000000)),
                         Word(0x88000100, 0x00000001, 0x00000200, 0x00402000))
        self.assertEqual(quarterround(Word(0x00000000, 0x00000000, 0x00000001, 0x00000000)),
                         Word(0x88040000, 0x00000000, 0x00000001, 0x00002000))
        self.assertEqual(quarterround(Word(0x00000000, 0x00000000, 0x00000000, 0x00000001)),
                         Word(0x00048044, 0x00000080, 0x00010000, 0x20100001))
        self.assertEqual(quarterround(Word(0xe7e8c006, 0xc4f9417d, 0x6479b4b2, 0x68c67137)),
                         Word(0xe876d72b, 0x9361dfd5, 0xf1460244, 0x948541a3))
        self.assertEqual(quarterround(Word(0xd3917c5b, 0x55f1c407, 0x52a58a7a, 0x8f887a3b)),
                         Word(0x3e2f308c, 0xd90a8f36, 0x6ab2a923, 0x2883524c))
