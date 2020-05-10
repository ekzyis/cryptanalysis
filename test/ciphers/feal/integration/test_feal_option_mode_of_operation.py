import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal
from test.ciphers.feal.integration.wrappers import default_decrypt_args, default_encrypt_args


class TestFeal(unittest.TestCase):

    def test_integration_feal_option_mode_of_operation_ecb(self):
        @default_encrypt_args('-m', 'ecb', key='0xFFFF', text='0xFFFFAAAAFFFFAAAACCCCDDDD')
        def test_mode_of_operation_ecb_with_encrypt():
            c = feal()
            #              KEY    TEXT                  OUTPUT IN HEX
            # feal encrypt 0xFFFF 0xFFFFAAAAFFFFAAAA    0xf4090052cbdac300
            # feal encrypt 0xFFFF 0xCCCCDDDD            0xd8428cef9fefca96
            self.assertEqual(hex(int(c, 16)), '0xf4090052cbdac300d8428cef9fefca96')

        test_mode_of_operation_ecb_with_encrypt()

        @default_decrypt_args('-m', 'ecb', key='0xFFFF', text='0xf4090052cbdac300d8428cef9fefca96')
        def test_mode_of_operation_ecb_with_decrypt():
            p = feal()
            self.assertEqual(hex(int(p, 16)), '0xFFFFAAAAFFFFAAAACCCCDDDD')

        test_mode_of_operation_ecb_with_decrypt()
