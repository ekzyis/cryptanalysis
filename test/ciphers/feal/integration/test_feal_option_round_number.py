import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import feal
from test.ciphers.feal.integration.patchers import default_decrypt_args, default_encrypt_args


class TestFEALOptionRoundNumber(unittest.TestCase):
    @default_encrypt_args('-n', '16')
    def test_integration_feal_encrypt_round_number(self):
        c = feal()
        self.assertEqual(c, str(0x01a94383eb19ba07))

    @default_decrypt_args('-n', '16', text='0x01a94383eb19ba07')
    def test_integration_feal_decrypt_round_number(self):
        p = feal()
        self.assertEqual(p, "0")

    @default_encrypt_args('-n', '1')
    def test_integration_feal_encrypt_raises_error_on_uneven_round_number(self):
        with self.assertRaises(ValueError):
            feal()
