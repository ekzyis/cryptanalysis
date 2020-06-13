# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.chacha20 import chacha20_hash
from test.helper import BitsTestCase
from util.bitseq import bitseq8, bitseq32, littleendian


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
            *[le(constant[i:i + 32]) for i in range(0, len(constant), 32)],
            *[le(key[i:i + 32]) for i in range(0, len(key), 32)],
            counter, le(nonce[0:32]), le(nonce[32:64]), nonce[64:96]
        )
        self.assertEqual(
            chacha20_hash(state),
            bitseq32(
                0xe4e7f110, 0x15593bd1, 0x1fdd0f50, 0xc47120a3,
                0xc7f4d1c7, 0x0368c033, 0x9aaa2204, 0x4e6cd4c3,
                0x466482d2, 0x09aa9f07, 0x05d7c214, 0xa2028bd9,
                0xd19c12b5, 0xb94e16de, 0xe883d0cb, 0x4e3c50a2
            )
        )
