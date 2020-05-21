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

from functools import reduce

from util.rot import rot_left
from util.split import split
from util.word import Word


def quarterround(y: int) -> Word:
    """Calculate the quarterround value of the input as specified in the paper.

    Returns a 128-bit value.
    Raises error if input is larger than 128-bit.
    """
    if y >= 2 ** 128:
        raise ValueError("Input must be 128-bit.")
    y_ = split(4, 32, y)
    y0, y1, y2, y3 = y_
    z1 = y1 ^ rot_left((y0 + y3) % (2 ** 32), 7, 32)
    z2 = y2 ^ rot_left((z1 + y0) % (2 ** 32), 9, 32)
    z3 = y3 ^ rot_left((z2 + z1) % (2 ** 32), 13, 32)
    z0 = y0 ^ rot_left((z3 + z2) % (2 ** 32), 18, 32)
    return Word(z0, z1, z2, z3, bit=32)


def rowround(_y: int) -> Word:
    """Calculate the rowround value of the input as specified in the paper.

    Returns a 512-bit value.
    Raises error if input is larger than 512-bit.
    """
    if _y >= 2 ** 512:
        raise ValueError("Input must be 512-bit.")
    y = split(16, 32, _y)
    z = [None] * 16
    z[0], z[1], z[2], z[3] = quarterround(Word(y[0], y[1], y[2], y[3], bit=32))
    z[5], z[6], z[7], z[4] = quarterround(Word(y[5], y[6], y[7], y[4], bit=32))
    z[10], z[11], z[8], z[9] = quarterround(Word(y[10], y[11], y[8], y[9], bit=32))
    z[15], z[12], z[13], z[14] = quarterround(Word(y[15], y[12], y[13], y[14], bit=32))
    return Word(*z, bit=32)


def columnround(_x: int) -> Word:
    """Calculate the columnround value of the input as specified in the paper.

    Returns a 512-bit value.
    Raises error if input is larger than 512-bit.
    """
    if _x >= 2 ** 512:
        raise ValueError("Input must be 512-bit.")
    x = split(16, 32, _x)
    y = [None] * 16
    y[0], y[4], y[8], y[12] = quarterround(Word(x[0], x[4], x[8], x[12], bit=32))
    y[5], y[9], y[13], y[1] = quarterround(Word(x[5], x[9], x[13], x[1], bit=32))
    y[10], y[14], y[2], y[6] = quarterround(Word(x[10], x[14], x[2], x[6], bit=32))
    y[15], y[3], y[7], y[11] = quarterround(Word(x[15], x[3], x[7], x[11], bit=32))
    return Word(*y, bit=32)


def doubleround(x: int) -> Word:
    """Calculate the doubleround value of the input as specified in the paper.

    Returns a 512-bit value.
    Raises error if input is larger than 512-bit.
    """
    # argument checking is done by column- and rowround.
    return rowround(columnround(x))


def littleendian(_b: int) -> Word:
    """Calculate the value of the integer when its bytes are interpreted in reverse order.

    Returns a 32-bit value.
    Raises error if input is larger than 32-bit.
    """
    if _b >= 2 ** 32:
        raise ValueError("Input must be 32-bit.")
    b = split(4, 8, _b)
    b.reverse()
    return Word(*b, bit=8)


def salsa20(x_: int) -> Word:
    """Calculate the salsa20 hash of the value.

    Returns a 64-byte sequence.
    Raises error if input is larger than 512-bit.
    """
    if x_ >= 2 ** 512:
        raise ValueError("Input must be 512-bit.")
    x = split(64, 8, x_)
    # [a, b, c, d, e, f, g, h] -> [ [a,b,c,d], [e,f,g,h] ]
    zipped = [x[i:i + 4] for i in range(0, len(x), 4)]
    word_zipped = [Word(*b, bit=8) for b in zipped]
    littleendian_words = [littleendian(w) for w in word_zipped]
    w = Word(*littleendian_words, bit=32)
    z = split(16, 32, reduce(lambda a, _: doubleround(a), range(10), w))
    return Word(*[littleendian((xi + zi) % 2 ** 32) for xi, zi in zip(w, z)], bit=32)


def expansion(k_: int, n_: int) -> Word:
    """Expand the key and the nonce into a 64-byte sequence.

    Returns a 64-byte sequence.
    Raises error if key is larger than 256-bit or nonce is larger than 128-bit.
    """
    if k_.bit_length() > 8 * 16:
        if k_.bit_length() > 8 * 32:
            raise ValueError("k must be smaller than 32 byte")
        k0, k1 = split(2, 16 * 8, k_)
        n = split(4, 4 * 8, n_)
        sigma = [
            Word(101, 120, 112, 97, bit=8), Word(110, 100, 32, 51, bit=8),
            Word(50, 45, 98, 121, bit=8), Word(116, 101, 32, 107, bit=8)
        ]
        return salsa20(
            Word(sigma[0], *split(4, 4 * 8, k0), sigma[1], *n, sigma[2], *split(4, 4 * 8, k1), sigma[3], bit=32))
    else:
        tau = [
            Word(101, 120, 112, 97, bit=8), Word(110, 100, 32, 49, bit=8),
            Word(54, 45, 98, 121, bit=8), Word(116, 101, 32, 107, bit=8)
        ]
        # split k and n into four slices of four bytes
        k = split(4, 4 * 8, k_)
        n = split(4, 4 * 8, n_)
        return salsa20(Word(tau[0], *k, tau[1], *n, tau[2], *k, tau[3], bit=32))
