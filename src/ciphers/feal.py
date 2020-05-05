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

    -n=N, --round-number=N    Number of rounds
"""

from docopt import docopt


def main():
    args = docopt(__doc__)
    print(args)


if __name__ == "__main__":
    main()
