from bitstring import Bits

# noinspection PyUnresolvedReferences
import test.context
from test.helper import BitsTestCase
from util.bitseq import littleendian


class TestLittleEndian(BitsTestCase):

    def test_littleendian(self):
        b1 = littleendian(Bits("0x12345678"))
        self.assertBit(b1, 0x78563412, 32)
        b2 = littleendian(Bits("0x01020304"))
        self.assertBit(b2, 0x04030201, 32)
