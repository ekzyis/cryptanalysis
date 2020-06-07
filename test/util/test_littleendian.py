import unittest

from bitstring import Bits

# noinspection PyUnresolvedReferences
import test.context
from util.bitseq import littleendian


class TestLittleEndian(unittest.TestCase):

    def setUp(self):
        def assert_bit(b: Bits, value: int, length: int):
            """Custom bit assertion function."""
            self.assertEqual(b.uint, value)
            self.assertEqual(len(b), length)

        self.assertBit = assert_bit

    def test_littleendian(self):
        b1 = littleendian(Bits("0x12345678"))
        self.assertBit(b1, 0x78563412, 32)
        b2 = littleendian(Bits("0x01020304"))
        self.assertBit(b2, 0x04030201, 32)
