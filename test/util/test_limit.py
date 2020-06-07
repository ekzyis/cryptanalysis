import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.limit import limit


class TestLimit(unittest.TestCase):

    def test_limit_returns_value_limited_to_specified_amount_of_its_most_significant_bits(self):
        self.assertEqual(limit(4, 8, 0b10011011), 0b1001)
        self.assertEqual(limit(4, 8, 0b0010011011), 0b1001)
        self.assertEqual(limit(8, 16, 0xf3ab), 0xf3)
