# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import fk
from test.helper import BitsTestCase
from util.bitseq import bitseq32


class TestFEALFk(BitsTestCase):

    def test_feal_fk_matches_specification_in_paper(self):
        # i/o values taken from p.7, section 5.2 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        f = fk(bitseq32(0x0), bitseq32(0x0))
        self.assertEqual(f, "0x10041044")

    def test_feal_fk_raises_value_error_if_a_or_b_not_32_bit(self):
        self.assert_fn_raises_if_arguments_not_of_given_lengths(
            fn=fk, correct_args=[bitseq32(0x0), bitseq32(0x0)], error=ValueError
        )
