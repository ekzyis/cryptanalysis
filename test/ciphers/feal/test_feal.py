import unittest
from unittest import mock

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal


class TestFeal(unittest.TestCase):
    @mock.patch('sys.argv', ['feal', 'encrypt', '0x123456789ABCDEF0123456789ABCDEF', '0'])
    def test_feal_encrypt_from_cmdline(self):
        c = feal()
        self.assertEqual(int(c), 0x9C9B54973DF685F8)
