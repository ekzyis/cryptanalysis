import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.rot import rot_left, rot_right


class TestRot(unittest.TestCase):

    def test_rot_left_adds_left_shifted_bits_to_right_side(self):
        self.assertEqual(rot_left(0b11001, 2), 0b00111)
        self.assertEqual(rot_left(0b1001110, 2), 0b0111010)
        # ignores leading zeroes; overflow happens right after highest set bit
        self.assertEqual(rot_left(0b001001110, 2), 0b0111010)
        self.assertEqual(rot_left(0b10110011, 4), 0b00111011)

    def test_rot_right_adds_right_shifted_bits_to_left_side(self):
        self.assertEqual(rot_right(0b11001, 2), 0b1110)
        self.assertEqual(rot_right(0b1001110, 2), 0b1010011)
        self.assertEqual(rot_right(0b001001110, 2), 0b1010011)
        self.assertEqual(rot_right(0b10110011, 4), 0b00111011)
