import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal
from test.ciphers.feal.integration.wrappers import default_decrypt_args, default_encrypt_args


class TestFealOptionRoundNumber(unittest.TestCase):
    @default_encrypt_args('-n', '16')
    def test_integration_feal_encrypt_round_number(self):
        c = feal()
        self.assertEqual(int(c), 0x1A94383EB19BA07)

    @default_decrypt_args('-n', '16', text='0x1A94383EB19BA07')
    def test_integration_feal_decrypt_round_number(self):
        p = feal()
        self.assertEqual(int(p), 0x0)
