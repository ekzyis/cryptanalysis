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


def rowround(_y: int) -> int:
    """The rowround function of Salsa20."""
    y = split(16, 32, _y)
    z = [None] * 16
    z[0], z[1], z[2], z[3] = quarterround(Word(y[0], y[1], y[2], y[3]))
    z[5], z[6], z[7], z[4] = quarterround(Word(y[5], y[6], y[7], y[4]))
    z[10], z[11], z[8], z[9] = quarterround(Word(y[10], y[11], y[8], y[9]))
    z[15], z[12], z[13], z[14] = quarterround(Word(y[15], y[12], y[13], y[14]))
    return Word(*z)


def columnround(_x: int) -> int:
    """The columnround function of Salsa20."""
    x = split(16, 32, _x)
    y = [None] * 16
    y[0], y[4], y[8], y[12] = quarterround(Word(x[0], x[4], x[8], x[12]))
    y[5], y[9], y[13], y[1] = quarterround(Word(x[5], x[9], x[13], x[1]))
    y[10], y[14], y[2], y[6] = quarterround(Word(x[10], x[14], x[2], x[6]))
    y[15], y[3], y[7], y[11] = quarterround(Word(x[15], x[3], x[7], x[11]))
    return Word(*y)


def doubleround(x: int) -> int:
    """The doubleround function of Salsa20."""
    return rowround(columnround(x))


def littleendian(_b: int) -> int:
    """The littleendian function of Salsa20."""
    b = split(4, 8, _b)
    b.reverse()
    return Word(*b, bit=8)
