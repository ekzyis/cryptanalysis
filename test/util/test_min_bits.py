import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.min_bits import min_bits


class TestMinBits(unittest.TestCase):
    def test_min_bits(self):
        self.assertEqual(min_bits(8), 4)
        self.assertEqual(min_bits(7), 3)
        self.assertEqual(min_bits(256), 9)
        self.assertEqual(min_bits(255), 8)
        self.assertEqual(min_bits(129), 8)
        self.assertEqual(min_bits(128), 8)
        self.assertEqual(min_bits(127), 7)
