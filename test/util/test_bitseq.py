import unittest

import bitstring

# noinspection PyUnresolvedReferences
import test.context
from util.bitseq import bitseq, bitseq_from_str


class TestBitSeq(unittest.TestCase):

    def setUp(self):
        def assert_bit(b: bitstring.Bits, value: int, length: int):
            """Custom bit assertion function."""
            self.assertEqual(b.uint, value)
            self.assertEqual(len(b), length)

        self.assertBit = assert_bit

    def test_bitseq_returns_bitstring_Bits_instance(self):
        b = bitseq(0x1, 0x2, 0x3, 0x4, bit=4)
        self.assertIsInstance(b, bitstring.Bits)

    def test_bitseq_with_only_integer_arguments(self):
        b1 = bitseq(0x1, 0x2, 0x3, 0x4, bit=4)
        self.assertBit(b1, 0x1234, 16)
        b2 = bitseq(0x1, 0x2, 0x3, 0x4, bit=16)
        self.assertBit(b2, 0x0001000200030004, 64)

    def test_bitseq_with_zero_bits(self):
        # leading zeros
        b1 = bitseq(0x0, 0x0, 0xa, 0xf, bit=4)
        self.assertBit(b1, 0xaf, 16)
        # only zeros
        b2 = bitseq(0x0, 0x0, 0x0, 0x0, bit=4)
        self.assertBit(b2, 0x0, 16)

    def test_bitseq_raises_value_error_if_integer_too_large(self):
        with self.assertRaises(ValueError):
            bitseq(0xf, bit=3)
        try:
            bitseq(0xf, bit=4)
        except ValueError:
            self.fail("bitseq raised unexpected ValueError")

    def test_bitseq_with_tuple_notation(self):
        b1 = bitseq((0x0,) * 4, bit=4)
        self.assertBit(b1, 0x0, 16)
        b2 = bitseq(0x1, (0x0,) * 3, bit=8)
        self.assertBit(b2, 0x01000000, 32)

    def test_bitseq_from_str(self):
        b1 = bitseq_from_str("0x1", "0x2", "0x3", "0x4")
        self.assertBit(b1, 0x1234, 16)
        b2 = bitseq_from_str("0x01", "0x02", "0x03", "0x04")
        self.assertBit(b2, 0x01020304, 32)
