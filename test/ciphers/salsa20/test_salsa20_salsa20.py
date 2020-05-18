import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.salsa20 import salsa20
from util.word import Word


class TestSalsa20CipherSalsa20(unittest.TestCase):
    def test_salsa20_salsa20(self):
        x1 = Word(0x0 * 16 * 4)
        z1 = 0x0
        self.assertEqual(salsa20(x1), z1)
        x2 = Word(
            (211, 159, 13, 115), (76, 55, 82, 183), (3, 117, 222, 37), (191, 187, 234, 136),
            (49, 237, 179, 48), (1, 106, 178, 219), (175, 199, 166, 48), (86, 16, 179, 207),
            (31, 240, 32, 63), (15, 83, 93, 161), (116, 147, 48, 113), (238, 55, 204, 36),
            (79, 201, 235, 79), (3, 81, 156, 47), (203, 26, 244, 243), (88, 118, 104, 54),
            bit=8
        )
        z2 = Word(
            (109, 42, 178, 168), (156, 240, 248, 238), (168, 196, 190, 203), (26, 110, 170, 154),
            (29, 29, 150, 26), (150, 30, 235, 249), (190, 163, 251, 48), (69, 144, 51, 57),
            (118, 40, 152, 157), (180, 57, 27, 94), (107, 42, 236, 35), (27, 111, 114, 114),
            (219, 236, 232, 135), (111, 155, 110, 18), (24, 232, 95, 158), (179, 19, 48, 202),
            bit=8
        )
        self.assertEqual(salsa20(x2), z2)
        x3 = Word(
            (88, 118, 104, 54), (79, 201, 235, 79), (3, 81, 156, 47), (203, 26, 244, 243),
            (191, 187, 234, 136), (211, 159, 13, 115), (76, 55, 82, 183), (3, 117, 222, 37),
            (86, 16, 179, 207), (49, 237, 179, 48), (1, 106, 178, 219), (175, 199, 166, 48),
            (238, 55, 204, 36), (31, 240, 32, 63), (15, 83, 93, 161), (116, 147, 48, 113),
            bit=8
        )
        z3 = Word(
            (179, 19, 48, 202), (219, 236, 232, 135), (111, 155, 110, 18), (24, 232, 95, 158),
            (26, 110, 170, 154), (109, 42, 178, 168), (156, 240, 248, 238), (168, 196, 190, 203),
            (69, 144, 51, 57), (29, 29, 150, 26), (150, 30, 235, 249), (190, 163, 251, 48),
            (27, 111, 114, 114), (118, 40, 152, 157), (180, 57, 27, 94), (107, 42, 236, 35),
            bit=8
        )
        self.assertEqual(salsa20(x3), z3)
