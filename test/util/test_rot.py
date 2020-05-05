import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.rot import rot_left, rot_right


class TestRot(unittest.TestCase):

    def test_rot_left_adds_left_shifted_bits_to_right_side(self):
        # max_bit equal to highest bit which leads to wrap-around
        self.assertEqual(rot_left(0b1101, 2, 4), 0b0111)
        # max_bit higher than highest bit with no wrap-around
        self.assertEqual(rot_left(0b001101, 2, 6), 0b110100)
        # max_bit higher than highest bit with wrap-around
        self.assertEqual(rot_left(0b001101, 4, 6), 0b010011)

    def test_rot_right_adds_right_shifted_bits_to_left_side(self):
        # max_bit equal to highest bit with regular wrap-around
        self.assertEqual(rot_right(0b1110, 2, 4), 0b1011)
        # max_bit higher than highest bit which leads to unregular wrap-around
        self.assertEqual(rot_right(0b1101, 2, 8), 0b01000011)
