"""Salsa20 implementation.

The specification found at https://cr.yp.to/snuffle/spec.pdf is used as a reference
for this implementation.

Usage:
    salsa encrypt [options] KEY PLAINTEXT
    salsa decrypt [options] KEY CIPHERTEXT

    -n=N, --round-number=N  Number of rounds. Must be even. [default: 32]
    -o=[bin,hex,oct,dec]    Specifies the output format. [default: dec]
    -m=[ecb,none]           Specifies the mode of operation [default: none]
    -x=[utf8,none]          Specifies the encoding of the cipher-/plaintext. [default: none]

    KEY                     The key which should be used for en-/decryption.
    PLAINTEXT               The text to encrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
    CIPHERTEXT              The text to decrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
"""
from typing import List

from util.rot import rot_left
from util.split import split
from util.word import Word


def quarterround(y: int) -> int:
    """The quarterround function of Salsa20."""
    y_: List[int] = split(4, 32, y)
    y0, y1, y2, y3 = y_
    z1 = y1 ^ rot_left((y0 + y3) % (2 ** 32), 7, 32)
    z2 = y2 ^ rot_left((z1 + y0) % (2 ** 32), 9, 32)
    z3 = y3 ^ rot_left((z2 + z1) % (2 ** 32), 13, 32)
    z0 = y0 ^ rot_left((z3 + z2) % (2 ** 32), 18, 32)
    return Word(z0, z1, z2, z3, bit=32)
