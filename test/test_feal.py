import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import s0


class TestS0(unittest.TestCase):
    def test_case_1(self):
        a = 0b10101010
        b = 0b01010101
        s = s0(a, b)
        self.assertEqual(0b111111, s)
        self.assertEqual(63, s)
