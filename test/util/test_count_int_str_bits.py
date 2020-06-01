import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.count_int_str_bits import count_int_str_bits


class TestCountIntStrBits(unittest.TestCase):
    def test_count_int_str_bits_with_decimal_integer_string_without_leading_zeros(self):
        self.assertEqual(count_int_str_bits('33'), 8)
        self.assertEqual(count_int_str_bits('32'), 8)
        self.assertEqual(count_int_str_bits('31'), 8)
        self.assertEqual(count_int_str_bits('1'), 4)
        self.assertEqual(count_int_str_bits('0'), 4)

    def test_count_int_str_bits_with_decimal_integer_string_with_leading_zeros(self):
        self.assertEqual(count_int_str_bits('01'), 8)
        self.assertEqual(count_int_str_bits('0255'), 16)
        self.assertEqual(count_int_str_bits('00'), 8)

    def test_count_int_str_bits_with_hexadecimal_integer_string_without_leading_zeros(self):
        self.assertEqual(count_int_str_bits('0x21'), 8)
        self.assertEqual(count_int_str_bits('0x20'), 8)
        self.assertEqual(count_int_str_bits('0x1f'), 8)
        self.assertEqual(count_int_str_bits('0x1'), 4)
        self.assertEqual(count_int_str_bits('0x0'), 4)

    def test_count_int_str_bits_with_hexadecimal_integer_string_with_leading_zeros(self):
        self.assertEqual(count_int_str_bits('0x01'), 8)
        self.assertEqual(count_int_str_bits('0x00FF'), 16)
        self.assertEqual(count_int_str_bits('0x00'), 8)

    def test_count_int_str_bits_with_octal_integer_string_without_leading_zeros(self):
        self.assertEqual(count_int_str_bits('0o41'), 6)
        self.assertEqual(count_int_str_bits('0o40'), 6)
        self.assertEqual(count_int_str_bits('0o37'), 6)
        self.assertEqual(count_int_str_bits('0o1'), 3)
        self.assertEqual(count_int_str_bits('0o0'), 3)

    def test_count_int_str_bits_with_octal_integer_string_with_leading_zeros(self):
        self.assertEqual(count_int_str_bits('0o01'), 6)
        self.assertEqual(count_int_str_bits('0o0377'), 12)
        self.assertEqual(count_int_str_bits('0o00'), 6)

    def test_count_int_str_bits_with_binary_integer_string_without_leading_zeros(self):
        self.assertEqual(count_int_str_bits('0b10000000'), 8)
        self.assertEqual(count_int_str_bits('0b1001'), 4)
        self.assertEqual(count_int_str_bits('0b10'), 2)
        self.assertEqual(count_int_str_bits('0b0'), 1)

    def test_count_int_str_bits_with_binary_integer_string_with_leading_zeros(self):
        self.assertEqual(count_int_str_bits('0b01'), 2)
        self.assertEqual(count_int_str_bits('0b00101'), 5)
        self.assertEqual(count_int_str_bits('0b00'), 2)

    def test_count_int_str_raises_value_error_if_input_is_not_an_integer_string(self):
        with self.assertRaises(ValueError):
            count_int_str_bits('test')
        with self.assertRaises(ValueError):
            count_int_str_bits('0xTEST')
        with self.assertRaises(ValueError):
            count_int_str_bits('0b2')
        with self.assertRaises(ValueError):
            count_int_str_bits('0o9')
