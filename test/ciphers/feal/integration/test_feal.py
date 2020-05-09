import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal
from test.sysv_patcher import sysv_patcher

default_encrypt_args = sysv_patcher('feal', 'encrypt', key='0x123456789ABCDEF0123456789ABCDEF', text='0x0')

default_decrypt_args = sysv_patcher('feal', 'decrypt', key='0x123456789ABCDEF0123456789ABCDEF',
                                    text='0x9C9B54973DF685F8')


class TestFeal(unittest.TestCase):
    @default_encrypt_args()
    def test_integration_feal_encrypt(self):
        c = feal()
        self.assertEqual(int(c), 0x9C9B54973DF685F8)

    @default_decrypt_args()
    def test_integration_feal_decrypt(self):
        p = feal()
        self.assertEqual(int(p), 0x0)
