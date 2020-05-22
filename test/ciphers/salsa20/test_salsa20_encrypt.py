import unittest
from unittest import mock

# noinspection PyUnresolvedReferences
import test.context
from ciphers.salsa20 import encrypt
from util.word import Word


class TestSalsa20CipherEncrypt(unittest.TestCase):
    """Test if encryption returns the same results as the test data.

    Test data obtained from:
    https://github.com/das-labor/legacy/blob/master/microcontroller-2/crypto-lib/testvectors/salsa20-full-verified.test-vectors
    """

    @mock.patch('random.randint', return_value=0x0)
    def test_salsa20_encrypt_256_bit_key_1(self, iv):
        """Key size: 256 bits, IV size: 64 bits, Test vectors -- set 1, vector# 0."""
        k = Word((0x80000000, 0x0, 0x0, 0x0),
                 (0x00000000, 0x0, 0x0, 0x0),
                 bit=32)
        m = 0x0
        c = encrypt(k, m)
        self.assertEqual(c, Word(
            (0x50EC2485, 0x637DB19C, 0x6E795E9C, 0x73938280),
            (0x6F6DB320, 0xFE3D0444, 0xD56707D7, 0xB456457F),
            (0x3DB3E8D7, 0x065AF375, 0xA225A709, 0x51C8AB74),
            (0x4EC4D595, 0xE85225F0, 0x8E2BC03F, 0xE1C42567),
            bit=32
        ))

    @mock.patch('random.randint', return_value=0x0)
    def test_salsa20_encrypt_256_bit_key_2(self, iv):
        """Key size: 256 bits, IV size: 64 bits, Test vectors -- set 1, vector# 9."""
        k = Word((0x00400000, 0x0, 0x0, 0x0),
                 (0x00000000, 0x0, 0x0, 0x0),
                 bit=32)
        m = 0x0
        c = encrypt(k, m)
        self.assertEqual(c, Word(
            (0x44936C5A, 0xE8EA9963, 0x0920CEC7, 0xC0FE9E8E),
            (0xA6C51663, 0x66D543D3, 0xA6FCCE3E, 0xAE9B0DF6),
            (0x28C61B62, 0xCABD61B4, 0x4F561044, 0x0C6798E9),
            (0x3B820711, 0x202105D1, 0x20398ECB, 0x96C0C102),
            bit=32
        ))

    @mock.patch('random.randint', return_value=0x0)
    def test_salsa20_encrypt_256_bit_key_3(self, iv):
        """Key size: 256 bits, IV size: 64 bits, Test vectors -- set 1, vector# 27."""
        k = Word((0x00000010, 0x0, 0x0, 0x0),
                 (0x00000000, 0x0, 0x0, 0x0),
                 bit=32)
        m = 0x0
        c = encrypt(k, m)
        self.assertEqual(c, Word(
            (0x00589828, 0x50C947A6, 0x37502384, 0x09A95FFF),
            (0xCA5A5599, 0x90EF1A60, 0xF038ADAA, 0xF965DD6B),
            (0x3931693C, 0x24AF075C, 0xC2766368, 0x3B7B15D1),
            (0x0F7A4B6B, 0xD1AD61F3, 0x5D67A7E6, 0x32ADBF2D),
            bit=32
        ))
