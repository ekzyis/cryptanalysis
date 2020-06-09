import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import feal
from test.ciphers.feal.integration.patchers import default_encrypt_args, default_decrypt_args


class TestFEALOptionEncoding(unittest.TestCase):

    @default_encrypt_args('-x', 'utf8', key="0xffff", text="secret")
    def test_integration_feal_encrypt_encoding_utf8(self):
        c = feal()
        # "secret".encode('utf8').hex()         => 0x736563726574
        # feal encrypt 0xffff 0x736563726574    => 0xc6c0acf427106a8d
        self.assertEqual(c, "0xc6c0acf427106a8d")

    @default_decrypt_args('-x', 'utf8', key="0xffff", text="0xc6c0acf427106a8d")
    def test_integration_feal_decrypt_encoding_utf8(self):
        p = feal()
        self.assertEqual(p, "secret")
