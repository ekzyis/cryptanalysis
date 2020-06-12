# noinspection PyUnresolvedReferences
import test.context
from test.helper import BitsTestCase
from util.bitseq import bitseq16, bitseq32, bitseq_split, bitseq8


class TestBitseqSplit(BitsTestCase):

    def setUp(self):
        self.b = bitseq32(0xFFFFFFFF, 0x0)

    def test_bitseq_split_going_for_full_split(self):
        b = self.b
        self.assertEqual(bitseq_split(32, b), [bitseq32(0xFFFFFFFF), bitseq32(0x0)])
        self.assertEqual(bitseq_split(16, b), [bitseq16(0xFFFF), bitseq16(0xFFFF), bitseq16(0x0), bitseq16(0x0)])

    def test_bitseq_split_with_n_equal_to_1(self):
        b = self.b
        self.assertEqual(bitseq_split(32, b, 1), bitseq32(0xFFFFFFFF))
        self.assertEqual(bitseq_split(8, b, 1), bitseq8(0xFF))

    def test_bitseq_split_with_n_greater_than_1(self):
        b = self.b
        # full split
        self.assertEqual(bitseq_split(32, b, 2), [bitseq32(0xFFFFFFFF), bitseq32(0x0)])
        self.assertEqual(bitseq_split(16, b, 2), [bitseq16(0xFFFF), bitseq16(0xFFFF)])

    def test_bitseq_split_is_identity_function_if_size_equal_to_len_of_input_and_n_equal_1(self):
        b = self.b
        self.assertEqual(bitseq_split(len(b), b, 1), b)

    def test_bitseq_split_raises_value_error_if_size_too_large(self):
        b = self.b
        with self.assertRaises(ValueError):
            bitseq_split(65, b)

    def test_bitseq_split_raises_value_error_if_combination_of_size_and_n_is_would_lead_to_oversplitting(self):
        b = self.b
        with self.assertRaises(ValueError):
            bitseq_split(1, b, 65)

    def test_bitseq_split_raises_value_error_if_n_zero(self):
        b = self.b
        with self.assertRaises(ValueError):
            bitseq_split(32, b, 0)

    def test_bitseq_split_raises_value_error_if_n_negative(self):
        b = self.b
        with self.assertRaises(ValueError):
            bitseq_split(32, b, -1)

    def test_bitseq_split_raises_value_error_if_size_zero(self):
        b = self.b
        with self.assertRaises(ValueError):
            bitseq_split(0, b)

    def test_bitseq_split_raises_value_error_if_size_negative(self):
        b = self.b
        with self.assertRaises(ValueError):
            bitseq_split(-1, b)
