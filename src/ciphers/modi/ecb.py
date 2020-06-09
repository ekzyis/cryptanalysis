"""Electronic Code Book mode implementation.

This file exports a wrapper which can implement ECB on given cipher functions.

ECB works by splitting the input into blocks which are then en- or decrypted.
The en- or decrypted blocks are then concatenated.
"""

from typing import Any

from bitstring import Bits

from util.wrap import padder_wrapper
from util.types import CipherFunction


def ecb(cipher_fn: CipherFunction, blocksize: int) -> CipherFunction:
    """Electronic Code Book Mode (ECB) implementation for ciphers.

    Works by splitting the argument into the needed blocks, passing those blocks to the
    cipher function and then return the concatenation of the results.

    :param cipher_fn        The cipher function which we want to wrap with ECB mode
    :param blocksize        Block size of cipher in bits on which we want to use ECB mode
    """

    def _ecb(key: Bits, text: Bits, *args: Any, **kwargs: Any) -> Bits:
        # add padding
        text = padder_wrapper(blocksize)(text)
        # split text into blocks
        in_blocks = [text[i:i + blocksize] for i in range(0, len(text), blocksize)]
        # crypt each block independently
        out_blocks = [cipher_fn(key, b, *args, **kwargs) for b in in_blocks]
        # concatenate blocks
        return sum(out_blocks)

    return _ecb


def feal_ecb(cipher_fn: CipherFunction) -> CipherFunction:
    """FEAL cipher functions wrapped with ECB."""
    return ecb(cipher_fn, blocksize=64)
