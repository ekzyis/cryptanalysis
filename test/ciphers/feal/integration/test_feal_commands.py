import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import feal
from test.ciphers.feal.integration.patchers import default_decrypt_args, default_encrypt_args


class TestFEALCommands(unittest.TestCase):
    @default_encrypt_args()
    def test_integration_feal_encrypt(self):
        c = feal()
        self.assertEqual(c, "0x9C9B54973DF685F8")

    @default_decrypt_args()
    def test_integration_feal_decrypt(self):
        p = feal()
        self.assertEqual(p, "0x0")
