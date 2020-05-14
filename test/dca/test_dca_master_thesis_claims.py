"""
This file is meant to fully grasp the statements in the
Master Thesis of Christian Bender about Differential Cryptanalysis.
Test cases assert that I come to the same conclusions.

Thesis available under: https://www.cryptool.org/images/ctp/documents/MA_Bender.pdf
"""
import unittest
from collections import defaultdict

# noinspection PyUnresolvedReferences
import test.context


class TestDCAMasterThesisClaims(unittest.TestCase):

    def test_that_there_are_2_to_the_power_of_n_amount_of_pairs_for_each_xor_value(self):
        """
        Assert following sentence from page 42, section 3.1.2 "Substitution".
        "Jede Eingabedifferenz ∆d kann von 2**n verschiedenen Eingabepaaren (m1, m2) mit m1 ⊕ m2 = ∆d erzeugt werden."
        """
        for n in range(8):
            xor_with_pairs = defaultdict(list)
            for a in range(2 ** n):
                for b in range(2 ** n):
                    xor_with_pairs[a ^ b].append((a, b))
            for pairs in xor_with_pairs.values():
                self.assertTrue(len(pairs), 2 ** n)

    def test_that_trivial_input_xor_of_0_leads_to_trivial_xor_output_of_0_after_substitution(self):
        """
        Assert following sentence from page 46, section 3.2.1 "Ein-Runden-Charakteristik".
        "Die triviale Ein-Runden-Charakteristik hat eine Eingabedifferenz von 0,
        was zu einer Ausgabedifferenz von 0 mit einer Wahrscheinlichkeit von 1 führt."
        """

        def s(n):
            """Implements the substitution box for the toy cipher 1 from C. Bender's about DCA."""
            _s = {
                0x0: 0b0110,
                0x1: 0b0100,
                0x2: 0b1100,
                0x3: 0b0101,
                0x4: 0b0000,
                0x5: 0b0111,
                0x6: 0b0010,
                0x7: 0b1110,
                0x8: 0b0001,
                0x9: 0b1111,
                0xA: 0b0011,
                0xB: 0b1101,
                0xC: 0b1000,
                0xD: 0b1010,
                0xE: 0b1001,
                0xF: 0b1011,
            }
            return _s[n]

        n = 4
        pairs_with_xor_equal_to_zero = list()
        for a in range(2 ** n):
            for b in range(2 ** n):
                if a ^ b == 0:
                    # if input xor difference of pair is zero, check the output xor difference of this pair
                    pairs_with_xor_equal_to_zero.append((a, b))
        for a, b in pairs_with_xor_equal_to_zero:
            output_xor = s(a) ^ s(b)
            self.assertEqual(output_xor, 0)
        """Wow, the trivial pairs are really trivial because they are the ones with a = b.
        Now I feel stupid that I needed to test this and didn't come up with this myself.
        I guess I was confused because I thought a ^ b = s(a) ^ s(b) = 0 means that a = s(a) and b = s(b)
        which is not the case. They still get permutated. I just didn't think about a ^ b = 0 <=> a = b
        and thus s(a) = s(b) <=> s(a) ^ s(b) = 0."""
