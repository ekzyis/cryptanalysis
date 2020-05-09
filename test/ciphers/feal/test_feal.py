import unittest
from unittest import mock

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal


class TestFeal(unittest.TestCase):
    @mock.patch('sys.argv', ['feal', 'encrypt', '0x123456789ABCDEF0123456789ABCDEF', '0'])
    def test_integration_feal_encrypt(self):
        c = feal()
        self.assertEqual(int(c), 0x9C9B54973DF685F8)

    @mock.patch('sys.argv', ['feal', 'decrypt', '0x123456789ABCDEF0123456789ABCDEF', '0x9C9B54973DF685F8'])
    def test_integration_feal_decrypt(self):
        p = feal()
        self.assertEqual(int(p), 0x0)
