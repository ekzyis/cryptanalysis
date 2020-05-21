import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.limit import limit


class TestLimit(unittest.TestCase):

    def test_limit_returns_value_limited_to_specified_amount_of_its_most_significant_bits(self):
        self.assertEqual(limit(0b10011011, 8, 4), 0b1001)
        self.assertEqual(limit(0b0010011011, 8, 4), 0b1001)
        self.assertEqual(limit(0xf3ab, 16, 8), 0xf3)
