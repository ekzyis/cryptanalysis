import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal
from test.ciphers.feal.integration.wrappers import default_decrypt_args, default_encrypt_args


class TestFealOptionModeOfOperation(unittest.TestCase):

    def test_integration_feal_option_mode_of_operation_ecb_with_no_remainder(self):
        @default_encrypt_args('-m', 'ecb', key='0xffff', text='0xfffafffafffafffafffafffafffafffa')
        def test_mode_of_operation_ecb_with_encrypt_no_remainder():
            c = feal()
            #              KEY    TEXT                  OUTPUT IN HEX
            # feal encrypt 0xffff 0xfffafffafffafffa    0xa281baaa4303e813
            self.assertEqual(hex(int(c, 0)).lower(), '0xa281baaa4303e813a281baaa4303e813')

        test_mode_of_operation_ecb_with_encrypt_no_remainder()

        @default_decrypt_args('-m', 'ecb', key='0xffff', text='0xa281baaa4303e813a281baaa4303e813')
        def test_mode_of_operation_ecb_with_decrypt_no_remainder():
            p = feal()
            self.assertEqual(hex(int(p, 0)).lower(), '0xfffafffafffafffafffafffafffafffa')

        test_mode_of_operation_ecb_with_decrypt_no_remainder()

    def test_integration_feal_option_mode_of_operation_ecb_with_remainder(self):
        @default_encrypt_args('-m', 'ecb', key='0xffff', text='0xfffafffafffafffafffafffa')
        def test_mode_of_operation_ecb_with_encrypt_remainder():
            c = feal()
            #              KEY    TEXT                  OUTPUT IN HEX
            # feal encrypt 0xffff 0xfffafffa            0x1ab00c4bbbc208e6
            # feal encrypt 0xffff 0xfffafffafffafffa    0xa281baaa4303e813
            self.assertEqual(hex(int(c, 0)).lower(), '0x1ab00c4bbbc208e6a281baaa4303e813')

        test_mode_of_operation_ecb_with_encrypt_remainder()

        @default_decrypt_args('-m', 'ecb', key='0xffff', text='0x1ab00c4bbbc208e6a281baaa4303e813')
        def test_mode_of_operation_ecb_with_decrypt_remainder():
            p = feal()
            self.assertEqual(hex(int(p, 0)).lower(), '0xfffafffafffafffafffafffa')

        test_mode_of_operation_ecb_with_decrypt_remainder()

    def test_integration_feal_option_mode_of_operation_raises_error_on_invalid_mode_input(self):
        @default_encrypt_args('-m', 'invalid')
        def test_mode_of_operation_invalid_with_encrypt():
            with self.assertRaises(KeyError):
                feal()

        test_mode_of_operation_invalid_with_encrypt()

        @default_decrypt_args('-m', 'invalid')
        def test_mode_of_operation_invalid_with_decrypt():
            with self.assertRaises(KeyError):
                feal()

        test_mode_of_operation_invalid_with_decrypt()
