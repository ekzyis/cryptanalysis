import unittest

import bitstring

# noinspection PyUnresolvedReferences
import test.context
from util.bitseq import bitseq, bitseq_from_str


class TestBitSeq(unittest.TestCase):

    def test_bitseq_returns_bitstring_Bits_instance(self):
        b = bitseq(0x1, 0x2, 0x3, 0x4, bit=4)
        self.assertIsInstance(b, bitstring.Bits)

    def test_bitseq_with_only_integer_arguments(self):
        b1 = bitseq(0x1, 0x2, 0x3, 0x4, bit=4)
        self.assertEqual(b1.uint, 0x1234)
        self.assertEqual(len(b1), 16)
        b2 = bitseq(0x1, 0x2, 0x3, 0x4, bit=16)
        self.assertEqual(b2.uint, 0x0001000200030004)
        self.assertEqual(len(b2), 64)

    def test_bitseq_raises_value_error_if_integer_too_large(self):
        with self.assertRaises(ValueError):
            bitseq(0xf, bit=3)
        try:
            bitseq(0xf, bit=4)
        except ValueError:
            self.fail("bitseq raised unexpected ValueError")

    def test_bitseq_from_str(self):
        b1 = bitseq_from_str("0x1", "0x2", "0x3", "0x4")
        self.assertEqual(b1.uint, 0x1234)
        self.assertEqual(len(b1), 16)
        b2 = bitseq_from_str("0x01", "0x02", "0x03", "0x04")
        self.assertEqual(b2.uint, 0x01020304)
        self.assertEqual(len(b2), 32)
