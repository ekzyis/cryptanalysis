import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import feal
from test.ciphers.feal.integration.patchers import default_encrypt_args, default_decrypt_args


class TestFEALAllOptionsCombined(unittest.TestCase):
    @default_encrypt_args('-x', 'utf8', '-m', 'ecb', '-o', 'hex', key='0xffff', text='this is a very secret message')
    def test_integration_feal_encrypt_all_options_combined(self):
        c = feal()
        self.assertEqual(c, '0xf8a7378679affc9f0ce10008e47b6c41f738d9b40e809b53ac8e92105a373ad0')

    @default_decrypt_args('-x', 'utf8', '-m', 'ecb', '-o', 'hex', key='0xffff',
                          text="0xf8a7378679affc9f0ce10008e47b6c41f738d9b40e809b53ac8e92105a373ad0")
    def test_integration_feal_decrypt_all_options_combined(self):
        p = feal()
        self.assertEqual(p, "this is a very secret message")
