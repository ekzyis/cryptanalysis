import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.block.feal import key_schedule
from util.bitseq import bitseq128, bitseq


class TestFEALCipherKeySchedule(unittest.TestCase):

    def test_feal_key_schedule_matches_specification_in_paper(self):
        # i/o values taken from p.10, section 6.3.1 of
        #   https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
        key = bitseq128(0x0123456789ABCDEF0123456789ABCDEF)
        out = key_schedule(key, n=32)
        self.assertEqual(len(out), 40)
        self.assertEqual(out[0], "0x7519")
        self.assertEqual(out[1], "0x71F9")
        self.assertEqual(out[2], "0x84E9")
        self.assertEqual(out[3], "0x4886")
        self.assertEqual(out[4], "0x88E5")
        self.assertEqual(out[5], "0x523B")
        self.assertEqual(out[6], "0x4EA4")
        self.assertEqual(out[7], "0x7ADE")
        self.assertEqual(out[8], "0xFE40")
        self.assertEqual(out[9], "0x5E76")
        self.assertEqual(out[10], "0x9819")
        self.assertEqual(out[11], "0xEEAC")
        self.assertEqual(out[12], "0x1BD4")
        self.assertEqual(out[13], "0x2455")
        self.assertEqual(out[14], "0xDCA0")
        self.assertEqual(out[15], "0x653B")
        self.assertEqual(out[16], "0x3E32")
        self.assertEqual(out[17], "0x4652")
        self.assertEqual(out[18], "0x1CC1")
        self.assertEqual(out[19], "0x34DF")
        self.assertEqual(out[20], "0x778B")
        self.assertEqual(out[21], "0x771D")
        self.assertEqual(out[22], "0xD324")
        self.assertEqual(out[23], "0x8410")
        self.assertEqual(out[24], "0x1CA8")
        self.assertEqual(out[25], "0xBC64")
        self.assertEqual(out[26], "0xA0DB")
        self.assertEqual(out[27], "0xBDD2")
        self.assertEqual(out[28], "0x1F5F")
        self.assertEqual(out[29], "0x8F1C")
        self.assertEqual(out[30], "0x6B81")
        self.assertEqual(out[31], "0xB560")
        self.assertEqual(out[32], "0x196A")
        self.assertEqual(out[33], "0x9AB1")
        self.assertEqual(out[34], "0xE015")
        self.assertEqual(out[35], "0x8190")
        self.assertEqual(out[36], "0x9F72")
        self.assertEqual(out[37], "0x6643")
        self.assertEqual(out[38], "0xAD32")
        self.assertEqual(out[39], "0x683A")

    def test_feal_key_schedule_raises_value_error_if_key_is_larger_than_128_bit(self):
        with self.assertRaises(ValueError):
            k = bitseq(0x0, bit=129)
            key_schedule(k)
        try:
            k = bitseq128(0x0)
            key_schedule(k)
        except ValueError:
            self.fail("key_schedule raised unexpected ValueError")
