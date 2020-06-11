# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.salsa20 import quarterround
from test.helper import BitsTestCase
from util.bitseq import bitseq32, bitseq128


class TestSalsa20Quarterround(BitsTestCase):
    def test_salsa20_quarterround(self):
        x1 = bitseq32((0x0,) * 4)
        self.assertEqual(x1, x1)

        x2 = bitseq32(0x1, (0x0,) * 3)
        y2 = bitseq32(0x08008145, 0x00000080, 0x00010200, 0x20500000)
        self.assertEqual(quarterround(x2), y2)

        x3 = bitseq32(0x0, 0x1, 0x0, 0x0)
        y3 = bitseq32(0x88000100, 0x00000001, 0x00000200, 0x00402000)
        self.assertEqual(quarterround(x3), y3)

        x4 = bitseq32(0x00000000, 0x00000000, 0x00000001, 0x00000000)
        y4 = bitseq32(0x80040000, 0x00000000, 0x00000001, 0x00002000)
        self.assertEqual(quarterround(x4), y4)

        x5 = bitseq32((0x0,) * 3, 0x1)
        y5 = bitseq32(0x00048044, 0x00000080, 0x00010000, 0x20100001)
        self.assertEqual(quarterround(x5), y5)

        x6 = bitseq32(0xe7e8c006, 0xc4f9417d, 0x6479b4b2, 0x68c67137)
        y6 = bitseq32(0xe876d72b, 0x9361dfd5, 0xf1460244, 0x948541a3)
        self.assertEqual(quarterround(x6), y6)

        x7 = bitseq32(0xd3917c5b, 0x55f1c407, 0x52a58a7a, 0x8f887a3b)
        y7 = bitseq32(0x3e2f308c, 0xd90a8f36, 0x6ab2a923, 0x2883524c)
        self.assertEqual(quarterround(x7), y7)

    def test_salsa20_quarterround_raises_value_error_if_input_not_128_bit(self):
        self.assert_fn_raises_if_arguments_not_of_given_lengths(
            fn=quarterround, correct_args=[bitseq128(0x0)], error=ValueError
        )
