# noinspection PyUnresolvedReferences
import test.context
from test.helper import BitsTestCase
from util.bitseq import bitseq_add, bitseq16, bitseq32


class TestBitseqSplit(BitsTestCase):

    def test_bitseq_add_with_no_overflow(self):
        b1 = bitseq16(0xF0F0)
        b2 = bitseq16(0x0F0F)
        self.assertEqual(bitseq_add(b1, b2), bitseq16(0xFFFF))

    def test_bitseq_add_with_overflow(self):
        b1 = bitseq16(0xFFFF)
        b2 = bitseq16(0x0001)
        self.assertEqual(bitseq_add(b1, b2), bitseq16(0x0))

    def test_bitseq_raises_value_error_if_bitstrings_have_not_same_length(self):
        b1 = bitseq16(0x0)
        b2 = bitseq32(0x0)
        with self.assertRaises(ValueError):
            bitseq_add(b1, b2)
