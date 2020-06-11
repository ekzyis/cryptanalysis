#!/usr/bin/env python

"""ChaCha20/r implementation.

Description of ChaCha20 from the specification paper used as a reference for this implementation:

    "ChaCha8 is a 256-bit stream cipher based on the 8-round cipher Salsa20/8.
    The changes from Salsa20/8 to ChaCha8 are designed to improve diffusion per round, conjecturally increasing
    resistance to cryptanalysis, while preserving—and often improving—time per round. ChaCha12 and ChaCha20 are
    analogous modifications of the 12-round and 20-round ciphers Salsa20/12 and Salsa20/20."
    - Daniel J. Bernstein, https://cr.yp.to/chacha/chacha-20080120.pdf

It should be noted that at https://www.rfc-editor.org/rfc/rfc7539.txt, one can find a paper which is specifically
designed as an implementation guide for ChaCha20. I have taken the test vectors for my implementation from there.
"""
from bitstring import Bits

from util.bitseq import bitseq32
from util.rot import rot_left_bits


def quarterround(y: Bits) -> Bits:
    """Calculate the ChaCha20 quarterround value of the input as specified in the paper.

    Returns a 128-bit value.
    Raises error if input is not 128-bit.
    """

    def _quarterround_step(x1, x2, x3, shift):
        x1 = bitseq32(x1.uint + x2.uint & 0xFFFFFFFF)
        x3 ^= x1
        x3 = rot_left_bits(x3, shift)
        return x1, x2, x3

    a, b, c, d = y[0:32], y[32:64], y[64:96], y[96:128]
    a, b, d = _quarterround_step(a, b, d, 16)
    c, d, b = _quarterround_step(c, d, b, 12)
    a, b, d = _quarterround_step(a, b, d, 8)
    c, d, b = _quarterround_step(c, d, b, 7)
    return a + b + c + d
