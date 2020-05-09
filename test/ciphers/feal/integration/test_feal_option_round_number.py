import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal
from test.ciphers.feal.integration.test_feal import default_decrypt_args, default_encrypt_args


class TestFeal(unittest.TestCase):
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
