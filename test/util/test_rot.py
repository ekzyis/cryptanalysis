import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.rot import rot_left, rot_right


class TestRot(unittest.TestCase):

    def test_rot_left_adds_left_shifted_bits_to_right_side(self):
        self.assertEqual(rot_left(0b11001, 2), 0b00111)
        self.assertEqual(rot_left(0b1001110, 2), 0b1101001)

    def test_rot_right_adds_right_shifted_bits_to_left_side(self):
        self.assertEqual(rot_right(0b11001, 2), 0b1110)
        self.assertEqual(rot_right(0b1001110, 2), 0b1010011)
