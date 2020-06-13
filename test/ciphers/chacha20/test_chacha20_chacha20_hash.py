# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.chacha20 import chacha20_hash
from test.helper import BitsTestCase
from util.bitseq import bitseq8, bitseq32, littleendian, bitseq_split


class TestChaCha20ChaCha20Hash(BitsTestCase):
    def test_chacha20_chacha20_hash(self):
        """Test for ChaCha20 Block Function IETF version with 96-bit nonce and 32-bit counter."""
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
            chacha20_hash(state),
            bitseq32(
                0x10f1e7e4, 0xd13b5915, 0x500fdd1f, 0xa32071c4,
                0xc7d1f4c7, 0x33c06803, 0x0422aa9a, 0xc3d46c4e,
                0xd2826446, 0x079faa09, 0x14c2d705, 0xd98b02a2,
                0xb5129cd1, 0xde164eb9, 0xcbd083e8, 0xa2503c4e,
            )
        )
