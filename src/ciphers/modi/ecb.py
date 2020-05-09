from math import log2, ceil

from util.concat_bits import concat_bits
from util.split import split


def ecb(blocksize):
    """Implements the Electronic Code Book Mode (ECB) for ciphers.
    Returns a function which needs the cipher function and the argument for it
    as arguments.
    Works by splitting the argument into the needed blocks, passing those blocks to the
    cipher function and then return the concatenation of the results.

    :param blocksize        Block size of cipher in bits on which we want to use ECB mode
    """

    def _ecb(cipher_fn, key, text, *args, **kwargs):
        # calculate amount of blocks
        min_text_bits = ceil(log2(text + 1))
        n = ceil(min_text_bits / blocksize)
        in_blocks = split(n, blocksize, text)
        out_blocks = [cipher_fn(key, b, *args, **kwargs) for b in in_blocks]
        return concat_bits(*out_blocks, n=blocksize)

    return _ecb
