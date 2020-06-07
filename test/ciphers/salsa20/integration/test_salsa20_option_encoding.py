import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.salsa20 import salsa20
from test.ciphers.salsa20.integration.patchers import default_encrypt_args, default_decrypt_args


class TestSalsa20OptionEncoding(unittest.TestCase):

    @default_encrypt_args('-x', 'utf8', text="secret")
    def test_integration_salsa20_encrypt_encoding_utf8(self, _):
        # "secret".encode('utf8').hex()         => 0x736563726574
        # IV:  0x0
        # key: default
        # salsa20 encrypt key 0x736563726574 => 0x000000000000000090dbecafee98
        self.assertEqual(salsa20(), "0x000000000000000090dbecafee98")

    @default_decrypt_args('-x', 'utf8', text="0x000000000000000090dbecafee98")
    def test_integration_salsa20_decrypt_encoding_utf8(self):
        p = salsa20()
        self.assertEqual(p, "secret")
