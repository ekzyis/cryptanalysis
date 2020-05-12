import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import encrypt, encrypt_preprocessing, encrypt_iterative_calculation


class TestFEALCipherEncrypt(unittest.TestCase):

    def test_encrypt_raises_value_error_if_text_larger_than_64_bit(self):
        with self.assertRaises(ValueError):
            encrypt(0x0, 2 ** 64)
        try:
            encrypt(0x0, 2 ** 64 - 1)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")

    def test_encrypt_raises_value_error_if_key_larger_than_128_bit(self):
        with self.assertRaises(ValueError):
            encrypt(2 ** 128, 0)
        try:
            encrypt(2 ** 128 - 1, 0)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")

    def test_encrypt_raises_value_error_if_text_not_number(self):
        with self.assertRaises(ValueError):
            encrypt(0x0, "test")
        try:
            encrypt(0x0, 0x0)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")

    def test_encrypt_raises_value_error_if_key_not_number(self):
        with self.assertRaises(ValueError):
            encrypt("key", 0x0)
        try:
            encrypt(0x0, 0x0)
        except ValueError:
            self.fail("encrypt raised unexpected ValueError")

    def test_encrypt_matches_specification_in_paper(self):
        # input key taken from p.8, section 6.2 and
        #   ciphertext taken from p.16, section 6.4.3 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        k = 0x123456789ABCDEF0123456789ABCDEF
        p = 0x0
        c = encrypt(k, p)
        self.assertEqual(c, 0x9C9B54973DF685F8)

    def test_encrypt_preprocessing_matches_specification_in_paper(self):
        # i/o values taken from p.10, section 6.2.1 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        k32, k33, k34, k35 = 0x196A, 0x9AB1, 0xE015, 0x8190
        p = 0x0
        out = encrypt_preprocessing([k32, k33, k34, k35], p)
        self.assertEqual(out, 0x196A9AB1F97F1B21)

    def test_encrypt_iterative_calculation_matches_specification_in_paper(self):
        # i/o values taken from p.14-15, section 6.4.2.3 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        l0, r0 = 0x196A9AB1, 0xF97F1B21
        sk = [
            0x7519, 0x71F9, 0x84E9, 0x4886, 0x88E5, 0x523B, 0x4EA4, 0x7ADE, 0xFE40, 0x5E76,
            0x9819, 0xEEAC, 0x1BD4, 0x2455, 0xDCA0, 0x653B, 0x3E32, 0x4652, 0x1CC1, 0x34DF,
            0x778B, 0x771D, 0xD324, 0x8410, 0x1CA8, 0xBC64, 0xA0DB, 0xBDD2, 0x1F5F, 0x8F1C,
            0x6B81, 0xB560, 0x196A, 0x9AB1, 0xE015, 0x8190, 0x9F72, 0x6643, 0xAD32, 0x683A
        ]
        l, r = encrypt_iterative_calculation(l0, r0, sk)
        self.assertEqual(l[0], 0x196A9AB1)
        self.assertEqual(l[1], 0xF97F1B21)
        self.assertEqual(l[2], 0x4C3667CD)
        self.assertEqual(l[3], 0xDE025865)
        self.assertEqual(l[4], 0x068245EF)
        self.assertEqual(l[5], 0x69E51495)
        self.assertEqual(l[6], 0x3E276105)
        self.assertEqual(l[7], 0xDA4B207D)
        self.assertEqual(l[8], 0x3B40E0FA)
        self.assertEqual(l[9], 0x83505F94)
        self.assertEqual(l[10], 0x9EA62593)
        self.assertEqual(l[11], 0x6BCC2E80)
        self.assertEqual(l[12], 0xB7797FFC)
        self.assertEqual(l[13], 0x888DEF7A)
        self.assertEqual(l[14], 0x93F874E6)
        self.assertEqual(l[15], 0x37D163B7)
        self.assertEqual(l[16], 0x4446BCE4)
        self.assertEqual(l[17], 0xFAFE290B)
        self.assertEqual(l[18], 0xD86B48E4)
        self.assertEqual(l[19], 0x542D6EBB)
        self.assertEqual(l[20], 0x2C82BF2A)
        self.assertEqual(l[21], 0x5BBAE971)
        self.assertEqual(l[22], 0x3828498B)
        self.assertEqual(l[23], 0x0EA71A8C)
        self.assertEqual(l[24], 0x339CD013)
        self.assertEqual(l[25], 0xC65851F1)
        self.assertEqual(l[26], 0xE0B20838)
        self.assertEqual(l[27], 0x7155D40B)
        self.assertEqual(l[28], 0xBE94A0EA)
        self.assertEqual(l[29], 0x8895B53A)
        self.assertEqual(l[30], 0xE1DBDC34)
        self.assertEqual(l[31], 0xA63FCF84)
        self.assertEqual(l[32], 0x932DDF16)
        self.assertListEqual(l[1:], r[:-1])
        self.assertEqual(r[32], 0x03E932D4)
