import unittest
from functools import reduce
from unittest import mock

# noinspection PyUnresolvedReferences
import test.context
from ciphers.salsa20 import expansion
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
        stream0 = expansion(k, Word(0x0, 0x0, bit=64))
        self.assertEqual(stream0, Word(
            0xE3BE8FDD8BECA2E3EA8EF9475B29A6E7,
            0x003951E1097A5C38D23B7A5FAD9F6844,
            0xB22C97559E2723C7CBBD3FE4FC8D9A07,
            0x44652A83E72A9C461876AF4D7EF1A117,
            bit=128
        ))
        counter = Word(0x3, bit=64).littleendian()
        stream3 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream3, Word(
            0x57BE81F47B17D9AE7C4FF15429A73E10,
            0xACF250ED3A90A93C711308A74C6216A9,
            0xED84CD126DA7F28E8ABF8BB63517E1CA,
            0x98E712F4FB2E1A6AED9FDC73291FAA17,
            bit=128
        ))
        counter = Word(0x4, bit=64).littleendian()
        stream4 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream4, Word(
            0x958211C4BA2EBD5838C635EDB81F513A,
            0x91A294E194F1C039AEEC657DCE40AA7E,
            0x7C0AF57CACEFA40C9F14B71A4B3456A6,
            0x3E162EC7D8D10B8FFB1810D71001B618,
            bit=128
        ))
        counter = Word(0x7, bit=64).littleendian()
        stream7 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream7, Word(
            0x696AFCFD0CDDCC83C7E77F11A649D79A,
            0xCDC3354E9635FF137E929933A0BD6F53,
            0x77EFA105A3A4266B7C0D089D08F1E855,
            0xCC32B15B93784A36E56A76CC64BC8477,
            bit=128
        ))
        stream = [
            stream0,
            expansion(k, Word(0x0, Word(0x1, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x2, bit=64).littleendian(), bit=64)),
            stream3,
            stream4,
            expansion(k, Word(0x0, Word(0x5, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x6, bit=64).littleendian(), bit=64)),
            stream7
        ]
        self.assertEqual(reduce(lambda a, b: a ^ b, stream), Word(
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
        stream = [
            expansion(k, Word(0x0, Word(0x0, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x1, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x2, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x3, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x4, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x5, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x6, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x7, bit=64).littleendian(), bit=64)),
        ]
        self.assertEqual(reduce(lambda a, b: a ^ b, stream), Word(
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
        stream = [
            expansion(k, Word(0x0, Word(0x0, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x1, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x2, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x3, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x4, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x5, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x6, bit=64).littleendian(), bit=64)),
            expansion(k, Word(0x0, Word(0x7, bit=64).littleendian(), bit=64)),
        ]
        self.assertEqual(reduce(lambda a, b: a ^ b, stream), Word(
            (0x00589828, 0x50C947A6, 0x37502384, 0x09A95FFF),
            (0xCA5A5599, 0x90EF1A60, 0xF038ADAA, 0xF965DD6B),
            (0x3931693C, 0x24AF075C, 0xC2766368, 0x3B7B15D1),
            (0x0F7A4B6B, 0xD1AD61F3, 0x5D67A7E6, 0x32ADBF2D),
            bit=32
        ))
