import unittest

from ciphers.salsa20 import expansion
from util.word import Word


class TestSalsa20CipherExpansion(unittest.TestCase):
    def test_salsa20_expansion_with_32_byte_k(self):
        k = Word(*[x for x in range(1, 17)], *[x for x in range(201, 217)], bit=8)
        n = Word(*[x for x in range(101, 117)], bit=8)
        z = Word(
            (69, 37, 68, 39), (41, 15, 107, 193), (255, 139, 122, 6), (170, 233, 217, 98),
            (89, 144, 182, 106), (21, 51, 200, 65), (239, 49, 222, 34), (215, 114, 40, 126),
            (104, 197, 7, 225), (197, 153, 31, 2), (102, 78, 76, 176), (84, 245, 246, 184),
            (177, 160, 133, 130), (6, 72, 149, 119), (192, 195, 132, 236), (234, 103, 246, 74),
            bit=8
        )
        self.assertEqual(expansion(k, n), z)

    def test_salsa20_expansion_with_16_byte_k(self):
        k = Word(*[x for x in range(1, 17)], bit=8)
        n = Word(*[x for x in range(101, 117)], bit=8)
        z = Word(
            (39, 173, 46, 248), (30, 200, 82, 17), (48, 67, 254, 239), (37, 18, 13, 247),
            (241, 200, 61, 144), (10, 55, 50, 185), (6, 47, 246, 253), (143, 86, 187, 225),
            (134, 85, 110, 246), (161, 163, 43, 235), (231, 94, 171, 51), (145, 214, 112, 29),
            (14, 232, 5, 16), (151, 140, 183, 141), (171, 9, 122, 181), (104, 182, 177, 193),
            bit=8
        )
        self.assertEqual(expansion(k, n), z)

    def test_salsa_20_expansion_raises_value_error_if_k_greater_than_32_byte(self):
        k = Word(*[x for x in range(33)], bit=8)
        with self.assertRaises(ValueError):
            expansion(k, 0x0)
