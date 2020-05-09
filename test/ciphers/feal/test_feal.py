import unittest
from unittest import mock

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import feal


def mock_patch_wrapper(*args, **kwargs):
    def wrapper(fn):
        # wraps the test function
        @mock.patch(*args, **kwargs)  # wraps the test function
        def _wrapper(self):
            # needed to pass the `self` argument from `unittest` to the test function
            return fn(self)

        return _wrapper

    return wrapper


default_encrypt_args = mock_patch_wrapper('sys.argv', ['feal', 'encrypt', '0x123456789ABCDEF0123456789ABCDEF', '0'])

default_decrypt_args = mock_patch_wrapper(
    'sys.argv', ['feal', 'decrypt', '0x123456789ABCDEF0123456789ABCDEF', '0x9C9B54973DF685F8'])


class TestFeal(unittest.TestCase):
    @default_encrypt_args
    def test_integration_feal_encrypt(self):
        c = feal()
        self.assertEqual(int(c), 0x9C9B54973DF685F8)

    @default_decrypt_args
    def test_integration_feal_decrypt(self):
        p = feal()
        self.assertEqual(int(p), 0x0)
