import unittest
from functools import reduce
from unittest import mock

# noinspection PyUnresolvedReferences
import test.context
from ciphers.salsa20 import expansion, encrypt
from util.types import Text
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
        self.assertEqual(stream[0], Word(
            0xE3BE8FDD8BECA2E3EA8EF9475B29A6E7,
            0x003951E1097A5C38D23B7A5FAD9F6844,
            0xB22C97559E2723C7CBBD3FE4FC8D9A07,
            0x44652A83E72A9C461876AF4D7EF1A117,
            bit=128
        ))
        self.assertEqual(stream[3], Word(
            0x57BE81F47B17D9AE7C4FF15429A73E10,
            0xACF250ED3A90A93C711308A74C6216A9,
            0xED84CD126DA7F28E8ABF8BB63517E1CA,
            0x98E712F4FB2E1A6AED9FDC73291FAA17,
            bit=128
        ))
        self.assertEqual(stream[4], Word(
            0x958211C4BA2EBD5838C635EDB81F513A,
            0x91A294E194F1C039AEEC657DCE40AA7E,
            0x7C0AF57CACEFA40C9F14B71A4B3456A6,
            0x3E162EC7D8D10B8FFB1810D71001B618,
            bit=128
        ))
        self.assertEqual(stream[7], Word(
            0x696AFCFD0CDDCC83C7E77F11A649D79A,
            0xCDC3354E9635FF137E929933A0BD6F53,
            0x77EFA105A3A4266B7C0D089D08F1E855,
            0xCC32B15B93784A36E56A76CC64BC8477,
            bit=128
        ))
        self.assertEqual(reduce(lambda a, b: a ^ b, stream), Word(
            (0x50EC2485, 0x637DB19C, 0x6E795E9C, 0x73938280),
            (0x6F6DB320, 0xFE3D0444, 0xD56707D7, 0xB456457F),
            (0x3DB3E8D7, 0x065AF375, 0xA225A709, 0x51C8AB74),
            (0x4EC4D595, 0xE85225F0, 0x8E2BC03F, 0xE1C42567),
            bit=32
        ))
        m = Text(0x0, bit=512 * 8)
        c = encrypt(k, m)
        self.assertEqual(c, Word(
            *[stream[i] for i in range(8)], bit=512
        ))

    @mock.patch('random.randint', return_value=0x0)
    def test_salsa20_encrypt_256_bit_key_1_with_non_zero_512_bytes_plaintext(self, iv):
        k = Word((0x80000000, 0x0, 0x0, 0x0),
                 (0x00000000, 0x0, 0x0, 0x0),
                 bit=32)
        # 64 bit * 4 * 16 = 256 bit * 16 = 512 bit * 8 = 512 bytes
        m = Text(
            0xdf31a36fbdd19f0d, 0x57519a1a8a9e677b, 0xa7037dc1e72595cb, 0x86ae61b858605ccc,
            0xc3045206b2437afc, 0xe21e6a5c66f631fe, 0xb43a64b51ea2c489, 0x860d212a7c9a72fd,
            0x8ada021ed41e0c95, 0x1f9c8cc391aa8bbc, 0xf4b9d53d3ab1bc13, 0xd950c1ea2762614e,
            0xb115e14e4fdb0c9d, 0x4a678418995c1a9a, 0x61ccda166f77c262, 0x667430d278b5c107,

            0x722b2c668370a829, 0x6bcc754023701aa1, 0xd6358099024336b5, 0xa5db1cd4aac92019,
            0x406278ada2dab814, 0x3bdee36b7885605d, 0x4f4abe76d7a8d507, 0x639c8dbbc15a0b03,
            0xf8c38747894e9e38, 0x55caef1fd0fd04b7, 0xbeff18c08c633936, 0x69c9cc6d6d2741fb,
            0x4fcdd255bdd31fa1, 0x1a4ece13df801d2f, 0x5835f331063f2477, 0x2ad5ae463c36ad36,

            0x5de629ce415a1a06, 0x278dc0e833608a84, 0x6e4073481eb82b8c, 0x86095a3313901208,
            0xb718a3531541fac4, 0xcc13466859ba677c, 0xd026a1897f6cc9ac, 0x473bf708e696bff4,
            0xe961e55e272a88cd, 0x25626d43952c4d8f, 0xbaae1ad014f86193, 0xd2096718f6883a2e,
            0xb7b188fd3034eb6c, 0x11c45600ea3fc1fc, 0x6f98b86f0f451264, 0x0309ac1c004e4f90,

            0xcad8c12db9a129a2, 0x06c622c3cdf6022b, 0x918830f09eb7195d, 0x2ef0acfc26b8a5a1,
            0x8dedc629d734375d, 0xabe1f85b09f7af52, 0xaee3304baa413a3b, 0xa1d87f9a6c96ab7c,
            0x3e3c9d6a9a839202, 0xeed50cadff279074, 0x2fcb41ea235aedcc, 0xc73f0ce821ba342e,
            0xd8ba37249c59f87d, 0x2b3ddb44d2e392a5, 0xacb4a32cf7272f4e, 0xd1153624755c6a38,
            bit=64)
        c = encrypt(k, m)
        stream = Word(
            0xe3be8fdd8beca2e3, 0xea8ef9475b29a6e7, 0x003951e1097a5c38, 0xd23b7a5fad9f6844,
            0xb22c97559e2723c7, 0xcbbd3fe4fc8d9a07, 0x44652a83e72a9c46, 0x1876af4d7ef1a117,
            0x8da2b74eef1b6283, 0xe7e20166abcae538, 0xe9716e4669e2816b, 0x6b20c5c356802001,
            0xcc1403a9a117d12a, 0x2669f456366d6ebb, 0x0f1246f1265150f7, 0x93cdb4b253e348ae,

            0x203d89bc025e802a, 0x7e0e00621d70aa36, 0xb7e07cb1e7d5b38d, 0x5e222b8b0e4b8407,
            0x0142b1e29504767d, 0x76824850320b5368, 0x129fdd74e861b498, 0xe3be8d16f2d7d169,
            0x57be81f47b17d9ae, 0x7c4ff15429a73e10, 0xacf250ed3a90a93c, 0x711308a74c6216a9,
            0xed84cd126da7f28e, 0x8abf8bb63517e1ca, 0x98e712f4fb2e1a6a, 0xed9fdc73291faa17,

            0x958211c4ba2ebd58, 0x38c635edb81f513a, 0x91a294e194f1c039, 0xaeec657dce40aa7e,
            0x7c0af57cacefa40c, 0x9f14b71a4b3456a6, 0x3e162ec7d8d10b8f, 0xfb1810d71001b618,
            0x2f9f73da53b85405, 0xc11f7b2d890fa8ae, 0x0c7f2e926d8a98c7, 0xec4e91b65120e988,
            0x349631a700c6face, 0xc3471cb0413656e7, 0x5e309456584084d7, 0xe12c5b43a41c43ed,

            0x9a048abd9b880da6, 0x5f6a665a20fe7b77, 0xcd292fe62cae644b, 0x7f7df69f32bdb331,
            0x903e6505ce44fdc2, 0x93920c6a9ec7057e, 0x23df7dad298f82dd, 0xf4efb7fdc7bfc622,
            0x696afcfd0cddcc83, 0xc7e77f11a649d79a, 0xcdc3354e9635ff13, 0x7e929933a0bd6f53,
            0x77efa105a3a4266b, 0x7c0d089d08f1e855, 0xcc32b15b93784a36, 0xe56a76cc64bc8477,
            bit=64
        )
        self.assertEqual(c, m ^ stream)

    @mock.patch('random.randint', return_value=0x0)
    def test_salsa20_encrypt_256_bit_key_1_with_non_zero_256_bytes_plaintext(self, iv):
        k = Word((0x80000000, 0x0, 0x0, 0x0),
                 (0x00000000, 0x0, 0x0, 0x0),
                 bit=32)
        # 64 bit * 4 * 8 = 256 bit * 8 = 256 bytes
        m = Text(
            0xdf31a36fbdd19f0d, 0x57519a1a8a9e677b, 0xa7037dc1e72595cb, 0x86ae61b858605ccc,
            0xc3045206b2437afc, 0xe21e6a5c66f631fe, 0xb43a64b51ea2c489, 0x860d212a7c9a72fd,
            0x8ada021ed41e0c95, 0x1f9c8cc391aa8bbc, 0xf4b9d53d3ab1bc13, 0xd950c1ea2762614e,
            0xb115e14e4fdb0c9d, 0x4a678418995c1a9a, 0x61ccda166f77c262, 0x667430d278b5c107,

            0x722b2c668370a829, 0x6bcc754023701aa1, 0xd6358099024336b5, 0xa5db1cd4aac92019,
            0x406278ada2dab814, 0x3bdee36b7885605d, 0x4f4abe76d7a8d507, 0x639c8dbbc15a0b03,
            0xf8c38747894e9e38, 0x55caef1fd0fd04b7, 0xbeff18c08c633936, 0x69c9cc6d6d2741fb,
            0x4fcdd255bdd31fa1, 0x1a4ece13df801d2f, 0x5835f331063f2477, 0x2ad5ae463c36ad36,
            bit=64)
        c = encrypt(k, m)
        stream = Word(
            0xe3be8fdd8beca2e3, 0xea8ef9475b29a6e7, 0x003951e1097a5c38, 0xd23b7a5fad9f6844,
            0xb22c97559e2723c7, 0xcbbd3fe4fc8d9a07, 0x44652a83e72a9c46, 0x1876af4d7ef1a117,
            0x8da2b74eef1b6283, 0xe7e20166abcae538, 0xe9716e4669e2816b, 0x6b20c5c356802001,
            0xcc1403a9a117d12a, 0x2669f456366d6ebb, 0x0f1246f1265150f7, 0x93cdb4b253e348ae,

            0x203d89bc025e802a, 0x7e0e00621d70aa36, 0xb7e07cb1e7d5b38d, 0x5e222b8b0e4b8407,
            0x0142b1e29504767d, 0x76824850320b5368, 0x129fdd74e861b498, 0xe3be8d16f2d7d169,
            0x57be81f47b17d9ae, 0x7c4ff15429a73e10, 0xacf250ed3a90a93c, 0x711308a74c6216a9,
            0xed84cd126da7f28e, 0x8abf8bb63517e1ca, 0x98e712f4fb2e1a6a, 0xed9fdc73291faa17,
            bit=64
        )
        self.assertEqual(c, m ^ stream)

    @mock.patch('random.randint', return_value=0x0)
    def test_salsa20_encrypt_256_bit_key_1_with_non_zero_8_bytes_plaintext(self, iv):
        k = Word((0x80000000, 0x0, 0x0, 0x0),
                 (0x00000000, 0x0, 0x0, 0x0),
                 bit=32)
        m = Text(0xdf31a36fbdd19f0d, bit=64)
        c = encrypt(k, m)
        stream = Word(0xe3be8fdd8beca2e3, bit=64)
        self.assertEqual(c, m ^ stream)

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
        self.assertEqual(stream[0], Word(
            0x01F191C3A1F2CC6EBED78095A05E062E,
            0x1228154AF6BAE80A0E1A61DF2AE15FBC,
            0xC37286440F66780761413F23B0C2C9E4,
            0x678C628C5E7FB48C6EC1D82D47117D9F,
            bit=128
        ))
        self.assertEqual(stream[3], Word(
            0x86D6F824D58012A14A19858CFE137D76,
            0x8E77597B96A4285D6B65D88A7F1A8778,
            0x4BF1A3E44FC9D3525DDC784F5D99BA22,
            0x2712420181CABAB00C4B91AAEDFF521C,
            bit=128
        ))
        self.assertEqual(stream[4], Word(
            0x287A9DB3C4EEDCC96055251B73ED361B,
            0xA727C2F326EF6944F9449FB7A3DDC396,
            0xA88D9D0D853FADE365F82789D57F9B40,
            0x10F963BC498F176A93FD51723FCD4D55,
            bit=128
        ))
        self.assertEqual(stream[7], Word(
            0xE0D62E2E3B37FDD906C934FAA35D5E8A,
            0x89A517DD0F24CF33DE8495C5FF24F4B1,
            0x476B3E826A1C90D74507C3991CEF4067,
            0xE316A04B97AEFFA5E9D1F33CB0609B9E,
            bit=128
        ))
        self.assertEqual(reduce(lambda a, b: a ^ b, stream), Word(
            (0x44936C5A, 0xE8EA9963, 0x0920CEC7, 0xC0FE9E8E),
            (0xA6C51663, 0x66D543D3, 0xA6FCCE3E, 0xAE9B0DF6),
            (0x28C61B62, 0xCABD61B4, 0x4F561044, 0x0C6798E9),
            (0x3B820711, 0x202105D1, 0x20398ECB, 0x96C0C102),
            bit=32
        ))
        m = Text(0x0, bit=512 * 8)
        c = encrypt(k, m)
        self.assertEqual(c, Word(
            *[stream[i] for i in range(8)], bit=512
        ))

    @mock.patch('random.randint', return_value=0x0)
    def test_salsa20_encrypt_256_bit_key_3(self, iv):
        """Key size: 256 bits, IV size: 64 bits, Test vectors -- set 1, vector# 18."""
        k = Word((0x00002000, 0x0, 0x0, 0x0),
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
        self.assertEqual(stream[0], Word(
            0xC29BA0DA9EBEBFACDEBBDD1D16E5F598,
            0x7E1CB12E9083D437EAAAA4BA0CDC909E,
            0x53D052AC387D86ACDA8D956BA9E6F654,
            0x3065F6912A7DF710B4B57F27809BAFE3,
            bit=128
        ))
        self.assertEqual(stream[3], Word(
            0x77DE29C19136852CC5DF78B5903CAC7B,
            0x8C91345350CF97529D90F18055ECB75A,
            0xC86A922B2BD3BD1DE3E2FB6DF9153166,
            0x09BDBAB298B37EA0C5ECD917788E2216,
            bit=128
        ))
        self.assertEqual(stream[4], Word(
            0x1985A31AA8484383B885418C78210D0E,
            0x84CBC7070A2ED22DCAAC6A739EAD5881,
            0x8E5F7755BE3BF0723A27DC69612F18DC,
            0x8BF9709077D22B78A365CE6131744651,
            bit=128
        ))
        self.assertEqual(stream[7], Word(
            0x9618FCA736A8ECA00BD1194FC9855085,
            0x526ECD47A8DE1F8DB298AD49FCE935EA,
            0x63B548597092ABAD6338F41AF87586A7,
            0x0505F2537902B81F55E53599DABA84CC,
            bit=128
        ))
        self.assertEqual(reduce(lambda a, b: a ^ b, stream), Word(
            (0xC442D753, 0x8E8129F0, 0x48E38EA1, 0xA6FFA5F8),
            (0x29F5B54D, 0x26A01DB1, 0xC0FA1B2E, 0x07418FB1),
            (0x872C5D96, 0xCDC25074, 0x6C26BD80, 0x3903E28D),
            (0x7DEC66DE, 0xD9AB7DE6, 0x797C502B, 0x3D1B246D),
            bit=32
        ))
        m = Text(0x0, bit=512 * 8)
        c = encrypt(k, m)
        self.assertEqual(c, Word(
            *[stream[i] for i in range(8)], bit=512
        ))
