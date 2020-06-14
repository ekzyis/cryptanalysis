# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.chacha import chacha_hash
from test.helper import BitsTestCase
from util.bitseq import bitseq8, bitseq32, littleendian, bitseq_split, bitseq256, bitseq64


def create_djb_state(key, counter, nonce):
    le = littleendian
    constant = bitseq32(0x65787061, 0x6e642033, 0x322d6279, 0x7465206b)
    return bitseq32(
        *bitseq_split(32, constant, formatter=le),
        *bitseq_split(32, key, formatter=le),
        *bitseq_split(32, counter, formatter=le), *bitseq_split(32, nonce, formatter=le)
    )


class TestChaChaChaChaHash(BitsTestCase):
    def test_chacha_chacha_hash_IETF_1_counter_1(self):
        """Test for ChaCha Block Function IETF version with 96-bit nonce and 32-bit counter."""
        constant = bitseq32(0x65787061, 0x6e642033, 0x322d6279, 0x7465206b)
        key = bitseq8(*[x for x in range(32)])
        nonce = bitseq8(0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x4a, 0x00, 0x00, 0x00, 0x00)  # 96-bit nonce
        counter = bitseq8(0x00, 0x00, 0x00, 0x01)  # 32-bit counter
        le = littleendian
        """
          constant  constant  constant  constant
          key       key       key       key
          key       key       key       key
          counter   nonce     nonce     nonce
        """
        state = bitseq32(
            *bitseq_split(32, constant, formatter=le),
            *bitseq_split(32, key, formatter=le),
            counter, *bitseq_split(32, nonce, formatter=le)
        )
        self.assertEqual(
            chacha_hash(state),
            bitseq32(
                0x10f1e7e4, 0xd13b5915, 0x500fdd1f, 0xa32071c4,
                0xc7d1f4c7, 0x33c06803, 0x0422aa9a, 0xc3d46c4e,
                0xd2826446, 0x079faa09, 0x14c2d705, 0xd98b02a2,
                0xb5129cd1, 0xde164eb9, 0xcbd083e8, 0xa2503c4e,
            )
        )

    def test_chacha_chacha_hash_DJB_1_counter_0(self):
        """Test #1 for ChaCha Block function DJB version with 64-bit nonce and 64-bit counter set to 0."""
        key = bitseq256(0x0)
        nonce = bitseq64(0x0)
        counter = bitseq64(0x0)
        state = create_djb_state(key, counter, nonce)
        self.assertEqual(
            chacha_hash(state),
            bitseq8(
                0x76, 0xb8, 0xe0, 0xad, 0xa0, 0xf1, 0x3d, 0x90,
                0x40, 0x5d, 0x6a, 0xe5, 0x53, 0x86, 0xbd, 0x28,
                0xbd, 0xd2, 0x19, 0xb8, 0xa0, 0x8d, 0xed, 0x1a,
                0xa8, 0x36, 0xef, 0xcc, 0x8b, 0x77, 0x0d, 0xc7,
                0xda, 0x41, 0x59, 0x7c, 0x51, 0x57, 0x48, 0x8d,
                0x77, 0x24, 0xe0, 0x3f, 0xb8, 0xd8, 0x4a, 0x37,
                0x6a, 0x43, 0xb8, 0xf4, 0x15, 0x18, 0xa1, 0x1c,
                0xc3, 0x87, 0xb6, 0x69, 0xb2, 0xee, 0x65, 0x86,
            )
        )

    def test_chacha_chacha_hash_DJB_1_counter_1(self):
        """Test #1 for ChaCha Block function DJB version with 64-bit nonce and 64-bit counter set to 1."""
        key = bitseq256(0x0)
        nonce = bitseq64(0x0)
        counter = bitseq64(0x1)
        state = create_djb_state(key, counter, nonce)
        self.assertEqual(
            chacha_hash(state),
            bitseq8(
                0x9f, 0x07, 0xe7, 0xbe, 0x55, 0x51, 0x38, 0x7a,
                0x98, 0xba, 0x97, 0x7c, 0x73, 0x2d, 0x08, 0x0d,
                0xcb, 0x0f, 0x29, 0xa0, 0x48, 0xe3, 0x65, 0x69,
                0x12, 0xc6, 0x53, 0x3e, 0x32, 0xee, 0x7a, 0xed,
                0x29, 0xb7, 0x21, 0x76, 0x9c, 0xe6, 0x4e, 0x43,
                0xd5, 0x71, 0x33, 0xb0, 0x74, 0xd8, 0x39, 0xd5,
                0x31, 0xed, 0x1f, 0x28, 0x51, 0x0a, 0xfb, 0x45,
                0xac, 0xe1, 0x0a, 0x1f, 0x4b, 0x79, 0x4d, 0x6f,
            )
        )

    def test_chacha_chacha_hash_DJB_2_counter_0(self):
        """Test #2 for ChaCha Block function DJB version with 64-bit nonce and 64-bit counter set to 0."""
        key = bitseq8(
            0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        )
        nonce = bitseq64(0x0)
        counter = bitseq64(0x0)
        state = create_djb_state(key, counter, nonce)
        self.assertEqual(
            chacha_hash(state),
            bitseq8(
                0xc5, 0xd3, 0x0a, 0x7c, 0xe1, 0xec, 0x11, 0x93,
                0x78, 0xc8, 0x4f, 0x48, 0x7d, 0x77, 0x5a, 0x85,
                0x42, 0xf1, 0x3e, 0xce, 0x23, 0x8a, 0x94, 0x55,
                0xe8, 0x22, 0x9e, 0x88, 0x8d, 0xe8, 0x5b, 0xbd,
                0x29, 0xeb, 0x63, 0xd0, 0xa1, 0x7a, 0x5b, 0x99,
                0x9b, 0x52, 0xda, 0x22, 0xbe, 0x40, 0x23, 0xeb,
                0x07, 0x62, 0x0a, 0x54, 0xf6, 0xfa, 0x6a, 0xd8,
                0x73, 0x7b, 0x71, 0xeb, 0x04, 0x64, 0xda, 0xc0,
            )
        )

    def test_chacha_chacha_hash_DJB_2_counter_1(self):
        """Test #2 for ChaCha Block function DJB version with 64-bit nonce and 64-bit counter set to 0."""
        key = bitseq8(
            0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        )
        nonce = bitseq64(0x0)
        counter = bitseq64(0x1)
        state = create_djb_state(key, counter, nonce)
        self.assertEqual(
            chacha_hash(state),
            bitseq8(
                0x10, 0xf6, 0x56, 0xe6, 0xd1, 0xfd, 0x55, 0x05,
                0x3e, 0x50, 0xc4, 0x87, 0x5c, 0x99, 0x30, 0xa3,
                0x3f, 0x6d, 0x02, 0x63, 0xbd, 0x14, 0xdf, 0xd6,
                0xab, 0x8c, 0x70, 0x52, 0x1c, 0x19, 0x33, 0x8b,
                0x23, 0x08, 0xb9, 0x5c, 0xf8, 0xd0, 0xbb, 0x7d,
                0x20, 0x2d, 0x21, 0x02, 0x78, 0x0e, 0xa3, 0x52,
                0x8f, 0x1c, 0xb4, 0x85, 0x60, 0xf7, 0x6b, 0x20,
                0xf3, 0x82, 0xb9, 0x42, 0x50, 0x0f, 0xce, 0xac,
            )
        )
