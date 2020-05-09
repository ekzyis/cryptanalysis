import unittest
from unittest import mock

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal


def patch_sysv_wrapper(*default_args, **default_kwargs):
    def additional_args_wrapper(*add_args, **add_kwargs):
        kwargs = dict(default_kwargs, **add_kwargs)
        args = list(default_args + add_args) + [kwargs['key'], kwargs['text']]

        def test_wrapper(fn):  # wraps the test function
            @mock.patch('sys.argv', args)
            def wrapper(*unittest_args):  # needed to pass the `self` argument from `unittest` to the test function
                return fn(*unittest_args)

            return wrapper

        return test_wrapper

    return additional_args_wrapper


default_encrypt_args = patch_sysv_wrapper('feal', 'encrypt', key='0x123456789ABCDEF0123456789ABCDEF', text='0x0')

default_decrypt_args = patch_sysv_wrapper('feal', 'decrypt', key='0x123456789ABCDEF0123456789ABCDEF',
                                          text='0x9C9B54973DF685F8')


class TestFeal(unittest.TestCase):
    @default_encrypt_args()
    def test_integration_feal_encrypt(self):
        c = feal()
        self.assertEqual(int(c), 0x9C9B54973DF685F8)

    @default_decrypt_args()
    def test_integration_feal_decrypt(self):
        p = feal()
        self.assertEqual(int(p), 0x0)

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

    def test_integration_feal_option_round_number(self):
        @default_encrypt_args('-n', '16')
        def test_round_number_with_encrypt():
            c = feal()
            self.assertEqual(int(c), 0x1A94383EB19BA07)

        test_round_number_with_encrypt()

        @default_decrypt_args('-n', '16', text='0x1A94383EB19BA07')
        def test_round_number_with_decrypt():
            p = feal()
            self.assertEqual(int(p), 0x0)

        test_round_number_with_decrypt()
