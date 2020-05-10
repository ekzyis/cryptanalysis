import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal, FEALArgumentException
from test.ciphers.feal.integration.wrappers import default_decrypt_args, default_encrypt_args


class TestFEALOptionModeOfOperation(unittest.TestCase):

    @default_encrypt_args('-m', 'ecb', key='0xffff', text='0xfffafffafffafffafffafffafffafffa')
    def test_integration_feal_encrypt_mode_of_operation_ecb_no_remainder(self):
        c = feal()
        #              KEY    TEXT                  OUTPUT IN HEX
        # feal encrypt 0xffff 0xfffafffafffafffa    0xa281baaa4303e813
        self.assertEqual(hex(int(c, 0)).lower(), '0xa281baaa4303e813a281baaa4303e813')

    @default_decrypt_args('-m', 'ecb', key='0xffff', text='0xa281baaa4303e813a281baaa4303e813')
    def test_integration_feal_decrypt_mode_of_operation_ecb_no_remainder(self):
        p = feal()
        self.assertEqual(hex(int(p, 0)).lower(), '0xfffafffafffafffafffafffafffafffa')

    @default_encrypt_args('-m', 'ecb', key='0xffff', text='0xfffafffafffafffafffafffa')
    def test_integration_feal_encrypt_mode_of_operation_ecb_with_remainder(self):
        c = feal()
        #              KEY    TEXT                  OUTPUT IN HEX
        # feal encrypt 0xffff 0xfffafffa            0x1ab00c4bbbc208e6
        # feal encrypt 0xffff 0xfffafffafffafffa    0xa281baaa4303e813
        self.assertEqual(hex(int(c, 0)).lower(), '0x1ab00c4bbbc208e6a281baaa4303e813')

    @default_decrypt_args('-m', 'ecb', key='0xffff', text='0x1ab00c4bbbc208e6a281baaa4303e813')
    def test_integration_feal_decrypt_mode_of_operation_ecb_with_remainder(self):
        p = feal()
        self.assertEqual(hex(int(p, 0)).lower(), '0xfffafffafffafffafffafffa')

    @default_encrypt_args('-m', 'invalid')
    def test_integration_feal_encrypt_mode_of_operation_raises_error_on_invalid_mode_input(self):
        with self.assertRaises(FEALArgumentException):
            feal()

    @default_decrypt_args('-m', 'invalid')
    def test_integration_feal_decrypt_mode_of_operation_raises_error_on_invalid_mode_input(self):
        with self.assertRaises(FEALArgumentException):
            feal()
