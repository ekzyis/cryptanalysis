# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.chacha import encrypt
from test.ciphers.chacha.patchers import iv, initial_counter
from test.helper import BitsTestCase
from util.bitseq import bitseq8, bitseq, bitseq256, bitseq512, bitseq64


class TestChaChaEncrypt(BitsTestCase):
    @iv(0x4a00000000)
    @initial_counter(1)
    def test_chacha_encrypt_ietf(self, *_):
        """2.4.2 Example and Test Vector for the ChaCha20 Cipher @ https://tools.ietf.org/html/rfc7539.
        Rounds: 20
        IETF version of ChaCha20 with 96-bit nonce, 32-bit counter.
        """
        k = bitseq8(*[i for i in range(32)])
        m = bitseq8(
            0x4c, 0x61, 0x64, 0x69, 0x65, 0x73, 0x20, 0x61, 0x6e, 0x64, 0x20, 0x47, 0x65, 0x6e, 0x74, 0x6c,
            0x65, 0x6d, 0x65, 0x6e, 0x20, 0x6f, 0x66, 0x20, 0x74, 0x68, 0x65, 0x20, 0x63, 0x6c, 0x61, 0x73,
            0x73, 0x20, 0x6f, 0x66, 0x20, 0x27, 0x39, 0x39, 0x3a, 0x20, 0x49, 0x66, 0x20, 0x49, 0x20, 0x63,
            0x6f, 0x75, 0x6c, 0x64, 0x20, 0x6f, 0x66, 0x66, 0x65, 0x72, 0x20, 0x79, 0x6f, 0x75, 0x20, 0x6f,
            0x6e, 0x6c, 0x79, 0x20, 0x6f, 0x6e, 0x65, 0x20, 0x74, 0x69, 0x70, 0x20, 0x66, 0x6f, 0x72, 0x20,
            0x74, 0x68, 0x65, 0x20, 0x66, 0x75, 0x74, 0x75, 0x72, 0x65, 0x2c, 0x20, 0x73, 0x75, 0x6e, 0x73,
            0x63, 0x72, 0x65, 0x65, 0x6e, 0x20, 0x77, 0x6f, 0x75, 0x6c, 0x64, 0x20, 0x62, 0x65, 0x20, 0x69,
            0x74, 0x2e,
        )
        iv_ = bitseq(0x4a00000000, bit=96)
        c = encrypt(k, m, version='ietf')
        self.assertEqual(
            c,
            iv_ + bitseq8(
                0x6e, 0x2e, 0x35, 0x9a, 0x25, 0x68, 0xf9, 0x80, 0x41, 0xba, 0x07, 0x28, 0xdd, 0x0d, 0x69, 0x81,
                0xe9, 0x7e, 0x7a, 0xec, 0x1d, 0x43, 0x60, 0xc2, 0x0a, 0x27, 0xaf, 0xcc, 0xfd, 0x9f, 0xae, 0x0b,
                0xf9, 0x1b, 0x65, 0xc5, 0x52, 0x47, 0x33, 0xab, 0x8f, 0x59, 0x3d, 0xab, 0xcd, 0x62, 0xb3, 0x57,
                0x16, 0x39, 0xd6, 0x24, 0xe6, 0x51, 0x52, 0xab, 0x8f, 0x53, 0x0c, 0x35, 0x9f, 0x08, 0x61, 0xd8,
                0x07, 0xca, 0x0d, 0xbf, 0x50, 0x0d, 0x6a, 0x61, 0x56, 0xa3, 0x8e, 0x08, 0x8a, 0x22, 0xb6, 0x5e,
                0x52, 0xbc, 0x51, 0x4d, 0x16, 0xcc, 0xf8, 0x06, 0x81, 0x8c, 0xe9, 0x1a, 0xb7, 0x79, 0x37, 0x36,
                0x5a, 0xf9, 0x0b, 0xbf, 0x74, 0xa3, 0x5b, 0xe6, 0xb4, 0x0b, 0x8e, 0xed, 0xf2, 0x78, 0x5e, 0x42,
                0x87, 0x4d,
            )
        )

    @iv(0x0)
    def test_chacha_encrypt_djb(self, *_):
        """3. Test vectors for ChaCha @ https://tools.ietf.org/html/draft-strombergson-chacha-test-vectors-00.
        Rounds: 20
        Original version of ChaCha20 with 64-bit nonce, 64-bit counter.
        """
        k = bitseq256(0x0)
        m = bitseq512(0x0, 0x0)
        c = encrypt(k, m, version='djb')
        iv_ = bitseq64(0x0)
        key_block_1 = bitseq8(
            0x76, 0xb8, 0xe0, 0xad, 0xa0, 0xf1, 0x3d, 0x90,
            0x40, 0x5d, 0x6a, 0xe5, 0x53, 0x86, 0xbd, 0x28,
            0xbd, 0xd2, 0x19, 0xb8, 0xa0, 0x8d, 0xed, 0x1a,
            0xa8, 0x36, 0xef, 0xcc, 0x8b, 0x77, 0x0d, 0xc7,
            0xda, 0x41, 0x59, 0x7c, 0x51, 0x57, 0x48, 0x8d,
            0x77, 0x24, 0xe0, 0x3f, 0xb8, 0xd8, 0x4a, 0x37,
            0x6a, 0x43, 0xb8, 0xf4, 0x15, 0x18, 0xa1, 0x1c,
            0xc3, 0x87, 0xb6, 0x69, 0xb2, 0xee, 0x65, 0x86,
        )
        key_block_2 = bitseq8(
            0x9f, 0x07, 0xe7, 0xbe, 0x55, 0x51, 0x38, 0x7a,
            0x98, 0xba, 0x97, 0x7c, 0x73, 0x2d, 0x08, 0x0d,
            0xcb, 0x0f, 0x29, 0xa0, 0x48, 0xe3, 0x65, 0x69,
            0x12, 0xc6, 0x53, 0x3e, 0x32, 0xee, 0x7a, 0xed,
            0x29, 0xb7, 0x21, 0x76, 0x9c, 0xe6, 0x4e, 0x43,
            0xd5, 0x71, 0x33, 0xb0, 0x74, 0xd8, 0x39, 0xd5,
            0x31, 0xed, 0x1f, 0x28, 0x51, 0x0a, 0xfb, 0x45,
            0xac, 0xe1, 0x0a, 0x1f, 0x4b, 0x79, 0x4d, 0x6f,
        )
        self.assertEqual(c, iv_ + key_block_1 + key_block_2)

    def test_chacha_encrypt_raises_error_if_key_not_256_bit(self):
        k = bitseq(0x0, bit=257)
        m = bitseq(0x0, bit=1)
        with self.assertRaises(ValueError):
            encrypt(k, m)