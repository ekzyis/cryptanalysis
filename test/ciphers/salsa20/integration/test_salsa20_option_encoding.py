import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.salsa20 import salsa20
from test.ciphers.salsa20.integration.patchers import default_encrypt_args, default_decrypt_args


class TestSalsa20OptionEncoding(unittest.TestCase):

    @default_encrypt_args('-x', 'utf8', key="0xffff", text="secret")
    def test_integration_salsa20_encrypt_encoding_utf8(self, _):
        c = salsa20()
        # "secret".encode('utf8').hex()         => 0x736563726574
        # IV: 0x0
        # salsa20 encrypt 0xffff 0x736563726574 => 0xa548a376d6d7
        self.assertEqual(int(c), 0xa548a376d6d7)

    @default_decrypt_args('-x', 'utf8', key="0xffff", text="0xc6c0acf427106a8d")
    def test_integration_salsa20_decrypt_encoding_utf8(self):
        p = salsa20()
        self.assertEqual(p, "secret")
