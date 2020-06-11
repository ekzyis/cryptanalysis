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
