#!/usr/bin/env python
"""
This file is meant to fully grasp the statements in the
Master Thesis of Christian Bender about Differential Cryptanalysis.
Test cases assert that I come to the same conclusions.

Thesis available under: https://www.cryptool.org/images/ctp/documents/MA_Bender.pdf
"""
import sys
import unittest
from collections import defaultdict
from pathlib import Path


class TestDCA(unittest.TestCase):

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

    def test_that_trivial_input_xor_of_0_leads_to_output_xor_of_0(self):
        """
        Assert following sentence from page 46, section 3.2.1 "Ein-Runden-Charakteristik".
        "Die triviale Ein-Runden-Charakteristik hat eine Eingabedifferenz von 0,
        was zu einer Ausgabedifferenz von 0 mit einer Wahrscheinlichkeit von 1 führt."
        """
        sys.path.insert(0, str((Path(__file__).parent / '..').resolve()))  # add src folder to path
        from dca.cipher1 import s
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


if __name__ == "__main__":
    unittest.main()
