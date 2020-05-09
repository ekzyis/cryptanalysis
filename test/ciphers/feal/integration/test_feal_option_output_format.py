import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal
from test.ciphers.feal.integration.wrappers import default_decrypt_args, default_encrypt_args


class TestFeal(unittest.TestCase):
    def test_integration_feal_option_output_format_bin(self):
        @default_encrypt_args('-o', 'bin')
        def test_format_bin_with_encrypt():
            c = feal()
            self.assertEqual(c, '0b1001110010011011010101001001011100111101111101101000010111111000')

        test_format_bin_with_encrypt()

        @default_decrypt_args('-o', 'bin')
        def test_format_bin_with_decrypt():
            p = feal()
            self.assertEqual(p, '0b0')

        test_format_bin_with_decrypt()

    def test_integration_feal_option_output_format_oct(self):
        @default_encrypt_args('-o', 'oct')
        def test_format_oct_with_encrypt():
            c = feal()
            self.assertEqual(c, '0o1162332511347575502770')

        test_format_oct_with_encrypt()

        @default_decrypt_args('-o', 'oct')
        def test_format_oct_with_decrypt():
            p = feal()
            self.assertEqual(p, '0o0')

        test_format_oct_with_decrypt()

    def test_integration_feal_option_output_format_dec(self):
        @default_encrypt_args('-o', 'dec')
        def test_format_dec_with_encrypt():
            c = feal()
            self.assertEqual(c, '11284706299863270904')

        test_format_dec_with_encrypt()

        @default_decrypt_args('-o', 'dec')
        def test_format_dec_with_decrypt():
            p = feal()
            self.assertEqual(p, '0')

        test_format_dec_with_decrypt()

    def test_integration_feal_option_output_format_hex(self):
        @default_encrypt_args('-o', 'hex')
        def test_format_hex_with_encrypt():
            c = feal()
            self.assertEqual(c, '0x9c9b54973df685f8')

        test_format_hex_with_encrypt()

        @default_decrypt_args('-o', 'hex')
        def test_format_hex_with_decrypt():
            p = feal()
            self.assertEqual(p, '0x0')

        test_format_hex_with_decrypt()
