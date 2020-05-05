import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.feal import s1


class TestFEALCipherS(unittest.TestCase):

    def test_s1_returns_expected_output_as_specified_in_reference(self):
        s = s1(0b00010011, 0b11110010)
        self.assertEqual(s, 0b00011000)
