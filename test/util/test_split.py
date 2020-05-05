import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.split import split


class TestSplit(unittest.TestCase):

    def test_split_splits_input_into_n_equal_sized_bitstrings(self):
        out = split(2, 2, 0)
        self.assertEqual(len(out), 2)
        for o in out:
            self.assertEqual(o, 0)
        out = split(2, 32, 2 ** 64 - 1)
        self.assertEqual(len(out), 2)
        for o in out:
            self.assertEqual(o, 2 ** 32 - 1)
        out = split(4, 8, 2 ** 32 - 1)
        self.assertEqual(len(out), 4)
        for o in out:
            self.assertEqual(o, 2 ** 8 - 1)

    def test_split_returns_correct_order_of_bitstrings(self):
        out = split(4, 4, 0b1010010111000011)
        self.assertEqual(len(out), 4)
        self.assertEqual(out[0], 0b1010)
        self.assertEqual(out[1], 0b0101)
        self.assertEqual(out[2], 0b1100)
        self.assertEqual(out[3], 0b0011)
        out = split(3, 4, 0b110101010011)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[0], 0b1101)
        self.assertEqual(out[1], 0b0101)
        self.assertEqual(out[2], 0b0011)

    def test_split_raises_error_when_input_is_larger_than_concatenation_of_bitstrings(self):
        with self.assertRaises(ValueError):
            split(2, 2, 2 ** 4)
        with self.assertRaises(ValueError):
            split(4, 4, 2 ** 16)
        with self.assertRaises(ValueError):
            split(4, 8, 2 ** 32)
        try:
            split(4, 8, 2 ** 32 - 1)
        except ValueError:
            self.fail("ValueError raised by split when not expected")

    def test_split_raises_error_when_n_is_less_than_or_equal_to_1(self):
        with self.assertRaises(ValueError):
            split(0, 2, 1)
        with self.assertRaises(ValueError):
            split(1, 2, 1)
