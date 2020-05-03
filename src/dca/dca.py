#!/usr/bin/env python
"""
This file is meant to fully grasp the statements in the
Master Thesis of Christian Bender about Differential Cryptanalysis.
Test cases assert that I come to the same conclusions.

Thesis available under: https://www.cryptool.org/images/ctp/documents/MA_Bender.pdf
"""


import unittest
from collections import defaultdict


class TestDCA(unittest.TestCase):

    def test_that_there_are_2_to_the_power_of_n_amount_of_pairs_for_each_xor_value(self):
        """
        Assert that the following sentence in C. Bender's Master Thesis about DCA
        in 3.1.2 Substitution is correct (and correctly understood):
        "Jede Eingabedifferenz ∆d kann von 2**n verschiedenen Eingabepaaren (m1, m2) mit m1 ⊕ m2 = ∆d erzeugt werden."
        """
        for n in range(8):
            xor_with_pairs = defaultdict(list)
            for a in range(2 ** n):
                for b in range(2 ** n):
                    xor_with_pairs[a ^ b].append((a, b))
            for pairs in xor_with_pairs.values():
                self.assertTrue(len(pairs), 2 ** n)


if __name__ == "__main__":
    unittest.main()
