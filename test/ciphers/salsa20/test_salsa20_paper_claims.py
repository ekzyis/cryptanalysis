"""
This file is meant to recalculate some calculations made in the paper
  "The Salsa20 family of stream ciphers"
  https://cr.yp.to/snuffle/salsafamily-20071225.pdf
"""

import unittest

from util.rot import rot_left


class TestSalsa20PaperClaims(unittest.TestCase):

    def test_salsa20_matrix_operation_as_described_in_section_4_1(self):
        """
        Starting array for key (1,2,3,4,5,...,32), nonce (3,1,4,1,5,9,2,6) and block 7
            0x61707865, 0x04030201, 0x08070605, 0x0c0b0a09
            0x100f0e0d, 0x3320646e, 0x01040103, 0x06020905
            0x00000007, 0x00000000, 0x79622d32, 0x14131211
            0x18171615, 0x1c1b1a19, 0x201f1e1d, 0x6b206574
        Salsa20 now modifies each below-diagonal word as follows: add the diagonal
        and above-diagonal words, rotate left by 7 bits, and xor into the below-diagonal
        words. The result is the following array:
            0x61707865, 0x04030201, 0x08070605, 0x95b0c8b6
            0xd3c83331, 0x3320646e, 0x01040103, 0x06020905
            0x00000007, 0x91b3379b, 0x79622d32, 0x14131211
            0x18171615, 0x1c1b1a19, 0x130804a0, 0x6b206574
        """
        a = rot_left(0x61707865 + 0x18171615, 7, 32) ^ 0x100f0e0d
        self.assertEqual(a, 0xd3c83331)
        b = rot_left(0x3320646e + 0x04030201, 7, 32) ^ 0x0
        self.assertEqual(b, 0x91b3379b)
        c = rot_left(0x79622d32 + 0x01040103, 7, 32) ^ 0x201f1e1d
        self.assertEqual(c, 0x130804a0)
        d = rot_left(0x6b206574 + 0x14131211, 7, 32) ^ 0x0c0b0a09
        self.assertEqual(d, 0x95b0c8b6)
