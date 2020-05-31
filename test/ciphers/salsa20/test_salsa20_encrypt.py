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
        stream0 = expansion(k, Word(0x0, 0x0, bit=64))
        self.assertEqual(stream0, Word(
            0x01F191C3A1F2CC6EBED78095A05E062E,
            0x1228154AF6BAE80A0E1A61DF2AE15FBC,
            0xC37286440F66780761413F23B0C2C9E4,
            0x678C628C5E7FB48C6EC1D82D47117D9F,
            bit=128
        ))
        counter = Word(0x3, bit=64).littleendian()
        stream3 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream3, Word(
            0x86D6F824D58012A14A19858CFE137D76,
            0x8E77597B96A4285D6B65D88A7F1A8778,
            0x4BF1A3E44FC9D3525DDC784F5D99BA22,
            0x2712420181CABAB00C4B91AAEDFF521C,
            bit=128
        ))
        counter = Word(0x4, bit=64).littleendian()
        stream4 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream4, Word(
            0x287A9DB3C4EEDCC96055251B73ED361B,
            0xA727C2F326EF6944F9449FB7A3DDC396,
            0xA88D9D0D853FADE365F82789D57F9B40,
            0x10F963BC498F176A93FD51723FCD4D55,
            bit=128
        ))
        counter = Word(0x7, bit=64).littleendian()
        stream7 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream7, Word(
            0xE0D62E2E3B37FDD906C934FAA35D5E8A,
            0x89A517DD0F24CF33DE8495C5FF24F4B1,
            0x476B3E826A1C90D74507C3991CEF4067,
            0xE316A04B97AEFFA5E9D1F33CB0609B9E,
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
            stream7,
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
        """Key size: 256 bits, IV size: 64 bits, Test vectors -- set 1, vector# 18."""
        k = Word((0x00002000, 0x0, 0x0, 0x0),
                 (0x00000000, 0x0, 0x0, 0x0),
                 bit=32)
        stream0 = expansion(k, Word(0x0, 0x0, bit=64))
        self.assertEqual(stream0, Word(
            0xC29BA0DA9EBEBFACDEBBDD1D16E5F598,
            0x7E1CB12E9083D437EAAAA4BA0CDC909E,
            0x53D052AC387D86ACDA8D956BA9E6F654,
            0x3065F6912A7DF710B4B57F27809BAFE3,
            bit=128
        ))
        counter = Word(0x3, bit=64).littleendian()
        stream3 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream3, Word(
            0x77DE29C19136852CC5DF78B5903CAC7B,
            0x8C91345350CF97529D90F18055ECB75A,
            0xC86A922B2BD3BD1DE3E2FB6DF9153166,
            0x09BDBAB298B37EA0C5ECD917788E2216,
            bit=128
        ))
        counter = Word(0x4, bit=64).littleendian()
        stream4 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream4, Word(
            0x1985A31AA8484383B885418C78210D0E,
            0x84CBC7070A2ED22DCAAC6A739EAD5881,
            0x8E5F7755BE3BF0723A27DC69612F18DC,
            0x8BF9709077D22B78A365CE6131744651,
            bit=128
        ))
        counter = Word(0x7, bit=64).littleendian()
        stream7 = expansion(k, Word(0x0, counter, bit=64))
        self.assertEqual(stream7, Word(
            0x9618FCA736A8ECA00BD1194FC9855085,
            0x526ECD47A8DE1F8DB298AD49FCE935EA,
            0x63B548597092ABAD6338F41AF87586A7,
            0x0505F2537902B81F55E53599DABA84CC,
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
            stream7,
        ]
        self.assertEqual(reduce(lambda a, b: a ^ b, stream), Word(
            (0xC442D753, 0x8E8129F0, 0x48E38EA1, 0xA6FFA5F8),
            (0x29F5B54D, 0x26A01DB1, 0xC0FA1B2E, 0x07418FB1),
            (0x872C5D96, 0xCDC25074, 0x6C26BD80, 0x3903E28D),
            (0x7DEC66DE, 0xD9AB7DE6, 0x797C502B, 0x3D1B246D),
            bit=32
        ))
