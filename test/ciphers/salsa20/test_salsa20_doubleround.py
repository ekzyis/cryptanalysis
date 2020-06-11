# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.salsa20 import doubleround
from test.helper import BitsTestCase
from util.bitseq import bitseq32, bitseq512


class TestSalsa20DoubleRound(BitsTestCase):
    def test_salsa20_doubleround(self):
        x1 = bitseq32(
            (0x1, 0x0, 0x0, 0x0),
            (0x0, 0x0, 0x0, 0x0) * 3,
        )
        y1 = bitseq32(
            (0x8186a22d, 0x0040a284, 0x82479210, 0x06929051),
            (0x08000090, 0x02402200, 0x00004000, 0x00800000),
            (0x00010200, 0x20400000, 0x08008104, 0x00000000),
            (0x20500000, 0xa0000040, 0x0008180a, 0x612a8020),
        )
        self.assertEqual(doubleround(x1), y1)
        x2 = bitseq32(
            (0xde501066, 0x6f9eb8f7, 0xe4fbbd9b, 0x454e3f57),
            (0xb75540d3, 0x43e93a4c, 0x3a6f2aa0, 0x726d6b36),
            (0x9243f484, 0x9145d1e8, 0x4fa9d247, 0xdc8dee11),
            (0x054bf545, 0x254dd653, 0xd9421b6d, 0x67b276c1),
        )
        y2 = bitseq32(
            (0xccaaf672, 0x23d960f7, 0x9153e63a, 0xcd9a60d0),
            (0x50440492, 0xf07cad19, 0xae344aa0, 0xdf4cfdfc),
            (0xca531c29, 0x8e7943db, 0xac1680cd, 0xd503ca00),
            (0xa74b2ad6, 0xbc331c5c, 0x1dda24c7, 0xee928277),
        )
        self.assertEqual(doubleround(x2), y2)

    def test_salsa20_doubleround_raises_value_error_if_input_not_512_bit(self):
        self.assert_fn_raises_if_arguments_not_of_given_lengths(
            fn=doubleround, correct_args=[bitseq512(0x0)], error=ValueError
        )
