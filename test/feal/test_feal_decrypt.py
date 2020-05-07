import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import decrypt


class TestFEALCipherDecrypt(unittest.TestCase):

    def test_decrypt_matches_specification_in_paper(self):
        """Checks that the FEAL decryption decrypts the given ciphertext."""
        # i/o values taken from test for encrypt.
        #   Since decryption should reverse encryption, I assume I can
        #   just pass in the output of encrypt into the input of decrypt
        #   and expect the input of encrypt as output of decrypt.
        c = 0x9C9B54973DF685F8
        k = 0x123456789ABCDEF0123456789ABCDEF
        p = decrypt(c, k)
        self.assertEqual(p, 0x0)
