import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import feal
from test.ciphers.feal.integration.patchers import default_decrypt_args, default_encrypt_args


class TestFEALOptionModeOfOperation(unittest.TestCase):

    @default_encrypt_args('-m', 'ecb', key='0xffff', text='0xfffafffafffafffafffafffafffafffa')
    def test_integration_feal_encrypt_mode_of_operation_ecb_no_remainder(self):
        c = feal()
        #              KEY    TEXT                  OUTPUT IN HEX
        # feal encrypt 0xffff 0xfffafffafffafffa    0xa281baaa4303e813
        self.assertEqual(c, "0xa281baaa4303e813a281baaa4303e813")

    @default_decrypt_args('-m', 'ecb', key='0xffff', text='0xa281baaa4303e813a281baaa4303e813')
    def test_integration_feal_decrypt_mode_of_operation_ecb_no_remainder(self):
        p = feal()
        self.assertEqual(p, "0xfffafffafffafffafffafffafffafffa")

    @default_encrypt_args('-m', 'ecb', key='0xffff', text='0xfffafffafffafffafffafffa')
    def test_integration_feal_encrypt_mode_of_operation_ecb_with_remainder(self):
        c = feal()
        #              KEY    TEXT                  OUTPUT IN HEX
        # feal encrypt 0xffff 0xfffafffa            0x1ab00c4bbbc208e6
        # feal encrypt 0xffff 0xfffafffafffafffa    0xa281baaa4303e813
        self.assertEqual(c, "0x1ab00c4bbbc208e6a281baaa4303e813")

    @default_decrypt_args('-m', 'ecb', key='0xffff', text='0x1ab00c4bbbc208e6a281baaa4303e813')
    def test_integration_feal_decrypt_mode_of_operation_ecb_with_remainder(self):
        p = feal()
        self.assertEqual(p, "0x00000000fffafffafffafffafffafffa")

    @default_encrypt_args('-m', 'invalid')
    def test_integration_feal_encrypt_mode_of_operation_raises_error_on_invalid_mode_input(self):
        with self.assertRaises(ValueError):
            feal()

    @default_decrypt_args('-m', 'invalid')
    def test_integration_feal_decrypt_mode_of_operation_raises_error_on_invalid_mode_input(self):
        with self.assertRaises(ValueError):
            feal()
