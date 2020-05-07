import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.concat_bits import concat_bits


class TestCombine(unittest.TestCase):

    def test_concat_bits_concatenates_four_8_bit_strings_into_one_32_bit_string(self):
        k0 = 0xAF
        k1 = 0x13
        k2 = 0xD3
        k3 = 0x8C
        out = concat_bits(k0, k1, k2, k3, n=8)
        self.assertEqual(out, 0xAF13D38C)

    def test_concat_bits_concatenates_8_four_bit_strings_into_one_32_bit_string(self):
        k0 = 0xA
        k1 = 0xE
        k2 = 0x9
        k3 = 0x1
        k4 = 0x8
        k5 = 0xA
        k6 = 0xB
        k7 = 0x5
        out = concat_bits(k0, k1, k2, k3, k4, k5, k6, k7, n=4)
        self.assertEqual(out, 0xAE918AB5)

    def test_concat_bits_raises_value_error_when_subkey_is_too_large(self):
        with self.assertRaises(ValueError):
            concat_bits(0b101, 0b10, n=2)
