import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import decrypt, decrypt_preprocessing


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

    def test_decrypt_raises_value_error_if_text_larger_than_64_bit(self):
        with self.assertRaises(ValueError):
            decrypt(2 ** 64, 0x0)
        try:
            decrypt(2 ** 64 - 1, 0x0)
        except ValueError:
            self.fail("decrypt raised unexpected ValueError")

    def test_decrypt_raises_value_error_if_key_larger_than_128_bit(self):
        with self.assertRaises(ValueError):
            decrypt(0x0, 2 ** 128)
        try:
            decrypt(0x0, 2 ** 128 - 1)
        except ValueError:
            self.fail("decrypt raised unexpected ValueError")

    def test_decrypt_preprocessing_matches_specification_in_paper(self):
        # i/o values taken from test for encrypt.
        #   As specified in the paper, the concatenation of the keys r_n, l_n which were calculated
        #   during encryption should be returned when using the output of said encryption as input.
        k34, k35, k36, k37 = 0x9F72, 0x6643, 0xAD32, 0x683A
        c = 0x9C9B54973DF685F8
        out = decrypt_preprocessing(c, [k34, k35, k36, k37])
        self.assertEqual(out, 0x03E932D4932DDF16)
