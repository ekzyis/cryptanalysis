#!/usr/bin/env python

"""
FEAL-NX Implementation.

    "In cryptography, FEAL (the Fast data Encipherment ALgorithm) is a block cipher proposed as an alternative
    to the Data Encryption Standard (DES), and designed to be much faster in software. The Feistel based algorithm
    was first published in 1987 by Akihiro Shimizu and Shoji Miyaguchi from NTT. The cipher is susceptible to various
    forms of cryptanalysis, and has acted as a catalyst in the discovery of differential and linear cryptanalysis."
    - Wikipedia, https://en.wikipedia.org/wiki/FEAL

The specification found at https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf is used as a reference
for this implementation.

It follows a short description of the cipher and its implementation:

    "FEAL, the Fast Data Encipherment Algorithm, is a 64-bit block cipher algorithm that enciphers 64-bit plaintexts
    into 64-bit ciphertexts and vice versa. FEAL has three options: key length, round number and key parity.
    The key length selects either 64-bit key or 128-bit key, the round number (N) specifies the internal iteration
    number for data randomization, and the key parity option selects either the use or non-use of parity bits in a key
    block. One subset of FEAL, called FEAL-NX, is N round FEAL using a 128-bit key without key parity."
    - NTT Secure Platform Laboratories, https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf

Usage:
    feal [options] PLAINTEXT

    -n=N, --round-number=N    Number of rounds [default: 32]
"""

from docopt import docopt

from util.rot import rot_left
from util.split import split


def s0(a, b):
    return _s(a, b, 0)


def s1(a, b):
    return _s(a, b, 1)


def _s(a, b, i):
    return rot_left((a + b + i) % 256, 2, 8)


def f(a, b):
    """f-function of FEAL-NX.
    a must be 32-bit and b must be 16-bit long
    Used during en-/decryption.
    See section 5.1 and figure 3 in
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf"""
    if a >= 2 ** 32 or b >= 2 ** 16:
        raise ValueError("Input keys must be 32-bit")
    a = split(n=4, size=8, bits=a)
    b = split(n=2, size=8, bits=b)
    f1 = a[1] ^ b[0]
    f2 = a[2] ^ b[1]
    f1 ^= a[0]
    f2 ^= a[3]
    f1 = s1(f1, f2)
    f2 = s0(f2, f1)
    f0 = s0(a[0], f1)
    f3 = s1(a[3], f2)
    return f0 << 24 | f1 << 16 | f2 << 8 | f3


def fk(a, b):
    """f_k-function of FEAL-NX.
    Input keys must be 32-bit.
    Used during key schedule to generate the subkeys for each iteration.
    See section 5.2 and figure 4 in
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf"""
    if a >= 2 ** 32 or b >= 2 ** 32:
        raise ValueError("Input keys must be 32-bit")
    a = split(n=4, size=8, bits=a)
    b = split(n=4, size=8, bits=b)
    fk1 = a[1] ^ a[0]
    fk2 = a[2] ^ a[3]
    fk1 = s1(fk1, fk2 ^ b[0])
    fk2 = s0(fk2, fk1 ^ b[1])
    fk0 = s0(a[0], fk1 ^ b[2])
    fk3 = s1(a[3], fk2 ^ b[3])
    return fk0 << 24 | fk1 << 16 | fk2 << 8 | fk3


def encrypt(text):
    """Encrpyts the given 64-bit text and returns the 64-bit ciphertext.
    Raises error if text is longer than 64-bit."""
    if text >= 2 ** 64:
        raise ValueError("Plaintext must be 64-bit")


def main():
    args = docopt(__doc__)
    print(args)


if __name__ == "__main__":
    main()
