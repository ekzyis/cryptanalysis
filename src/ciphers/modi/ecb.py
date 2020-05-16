"""Electronic Code Book mode implementation.

This file exports a wrapper which can implement ECB on given cipher functions.

ECB works by splitting the input into blocks which are then en- or decrypted.
The en- or decrypted blocks are then concatenated.
"""

from math import ceil

from util.concat_bits import concat_bits
from util.min_bits import min_bits
from util.split import split


def ecb(cipher_fn, blocksize):
    """Electronic Code Book Mode (ECB) implementation for ciphers.

    Works by splitting the argument into the needed blocks, passing those blocks to the
    cipher function and then return the concatenation of the results.

    :param cipher_fn        The cipher function which we want to wrap with ECB mode
    :param blocksize        Block size of cipher in bits on which we want to use ECB mode
    """

    def _ecb(key, text, *args, **kwargs):
        # calculate amount of blocks
        n = ceil(min_bits(text) / blocksize)
        in_blocks = split(n, blocksize, text)
        out_blocks = [cipher_fn(key, b, *args, **kwargs) for b in in_blocks]
        return concat_bits(*out_blocks, n=blocksize)

    return _ecb


def feal_ecb(cipher_fn):
    """FEAL cipher functions wrapped with ECB."""
    return ecb(cipher_fn, blocksize=64)
