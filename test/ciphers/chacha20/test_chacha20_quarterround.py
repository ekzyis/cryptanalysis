import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.chacha20 import quarterround
from util.bitseq import bitseq32


class TestChaCha20Quarterround(unittest.TestCase):
    def test_chacha20_quarterround(self):
        self.assertEqual(
            quarterround(bitseq32(0x11111111, 0x01020304, 0x9b8d6f43, 0x01234567)),
            bitseq32(0xea2a92f4, 0xcb1cf8ce, 0x4581472e, 0x5881c4bb)
        )
