#!/usr/bin/env python

"""ChaCha20/r implementation.

Specification:
    https://cr.yp.to/chacha/chacha-20080128.pdf

Test vectors:
    https://tools.ietf.org/html/rfc7539 (IETF implementation; uses 96-bit nonce and 32-bit counter)
    https://tools.ietf.org/html/draft-strombergson-chacha-test-vectors-00 (original implementation)

Description of ChaCha20 from the specification paper used as a reference for this implementation:

    "ChaCha8 is a 256-bit stream cipher based on the 8-round cipher Salsa20/8.
    The changes from Salsa20/8 to ChaCha8 are designed to improve diffusion per round, conjecturally increasing
    resistance to cryptanalysis, while preserving—and often improving—time per round. ChaCha12 and ChaCha20 are
    analogous modifications of the 12-round and 20-round ciphers Salsa20/12 and Salsa20/20."
    - Daniel J. Bernstein, https://cr.yp.to/chacha/chacha-20080120.pdf
"""
from bitstring import Bits, pack

from util.bitseq import bitseq32
from util.rot import rot_left_bits

__CHACHA_20_ROUNDS__ = 20


def quarterround(y: Bits) -> Bits:
    """Calculate the ChaCha20 quarterround value of the input as specified in the paper.

    Returns a 128-bit value.
    Raises error if input is not 128-bit.
    """
    if len(y) != 128:
        raise ValueError("Input must be 64-bit")

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


def quarterround_state(state: Bits, i, j, k, l) -> Bits:
    """Calculate the quarterround value of the state with the given indices.

    Returns a 512-bit value.
    State must be 512-bit.
    """
    entry = [state[index:index + 32] for index in range(0, len(state), 32)]
    q = quarterround(sum([entry[i], entry[j], entry[k], entry[l]]))
    entry[i], entry[j], entry[k], entry[l] = [q[index:index + 32] for index in range(0, len(q), 32)]
    return sum(entry)


def chacha20_hash(state_: Bits) -> Bits:
    """Calculate the chacha20 hash value."""
    # copy old state
    state = Bits(state_)
    for i in range(int(__CHACHA_20_ROUNDS__ / 2)):
        # column round
        state = quarterround_state(state, 0, 4, 8, 12)
        state = quarterround_state(state, 1, 5, 9, 13)
        state = quarterround_state(state, 2, 6, 10, 14)
        state = quarterround_state(state, 3, 7, 11, 15)
        # diagonal round
        state = quarterround_state(state, 0, 5, 10, 15)
        state = quarterround_state(state, 1, 6, 11, 12)
        state = quarterround_state(state, 2, 7, 8, 13)
        state = quarterround_state(state, 3, 4, 9, 14)
    original_state_bitseq32 = [state_[i:i + 32] for i in range(0, len(state_), 32)]
    new_state_bitseq32 = [state[i:i + 32] for i in range(0, len(state), 32)]
    state = sum(
        [bitseq32(xi.uint + zi.uint & 0xFFFFFFFF) for xi, zi in zip(original_state_bitseq32, new_state_bitseq32)]
    )
    state = pack("<16L", *[state[i:i + 32].uint for i in range(0, len(state), 32)])
    return state
