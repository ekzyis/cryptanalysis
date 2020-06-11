# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import f
from test.helper import BitsTestCase
from util.bitseq import bitseq32, bitseq16


class TestFEALF(BitsTestCase):

    def test_feal_f_matches_specification_in_paper(self):
        # i/o values taken from p.7, section 5.1 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        _f = f(bitseq32(0x00FFFF00), bitseq16(0xFFFF))
        self.assertEqual(_f, "0x10041044")

    def test_feal_f_raises_value_error_if_a_not_32_bit_or_b_not_16_bit(self):
        self.assert_fn_raises_if_arguments_not_of_given_lengths(
            fn=f, correct_args=[bitseq32(0x0), bitseq16(0x0)], error=ValueError
        )
