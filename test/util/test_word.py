import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.word import Word


class TestWord(unittest.TestCase):

    def test_word_with_1_bit(self):
        self.assertEqual(Word(1, 0, 1, 0, bit=1), 0b1010)

    def test_word_with_4_bit(self):
        self.assertEqual(Word(0x3, 0xf, 0xa, 0xe, bit=4), 0x3fae)

    def test_word_with_16_bit(self):
        self.assertEqual(Word(0x3a1c, 0x13bc, 0x84de, bit=16), 0x3a1c13bc84de)

    def test_word_tuple_syntax(self):
        w1 = Word((0xf, 0x0),
                  (0x0, 0xf), bit=4)
        self.assertEqual(w1, 0xf00f)
        w2 = Word((0xf0, 0x0f),
                  (0xac, 0x12), bit=8)
        self.assertEqual(w2, 0xf00fac12)

    def test_word_is_iterable(self):
        b = [0xf, 0xe, 0xd, 0xc]
        for i, byte in enumerate(Word(*b, bit=32)):
            self.assertEqual(byte, b[i])

    def test_word_is_subscriptable(self):
        b = [0xf, 0xe, 0xd, 0xc]
        w = Word(*b, bit=32)
        for i in range(len(b)):
            self.assertEqual(w[i], b[i])

    def test_word_raises_error_when_bit_too_small_for_representation(self):
        with self.assertRaises(ValueError):
            Word(0b10, bit=1)
        with self.assertRaises(ValueError):
            Word(0x10, bit=2)
        with self.assertRaises(ValueError):
            Word(0xF, bit=3)  # 15 needs at least four bits
        with self.assertRaises(ValueError):
            Word(0x10, bit=4)  # 16 needs at least five bits

    def test_word_littleendian(self):
        w1 = Word(0x1, bit=4)
        self.assertEqual(w1.littleendian(), 0x1)
        w1 = Word(0x1, bit=8)
        self.assertEqual(w1.littleendian(), 0x1)
        w2 = Word(0x1, bit=16)
        self.assertEqual(w2.littleendian(), 0x0100)
        w3 = Word(0x1, bit=32)
        self.assertEqual(w3.littleendian(), 0x01000000)
        w4 = Word(0x54, 0x12, 0xAF, bit=8)
        self.assertEqual(w4.littleendian(), 0xAF1254)
        w5 = Word(0x0154, 0x1203, 0x0AFC, bit=16)
        self.assertEqual(w5.littleendian(), 0xFC0A03125401)

    def test_word_hex(self):
        w1 = Word(0x0, bit=16)
        self.assertEqual(w1.hex(), '0x0000')
        w2 = Word(0x13, 0xfa, bit=16)
        self.assertEqual(w2.hex(), '0x001300fa')
