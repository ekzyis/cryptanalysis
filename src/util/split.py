"""Exports function which splits numbers into an array of bitstrings."""
from typing import List, Iterator


def split(n: int, size: int, bits: int) -> List[int]:
    """Split a number into an array of bitstrings.

    Split the input bits into n bitstrings with given size. The most significant bits are returned first.

    Example:
        split(3, 2, 0b110110) -> [0b11, 0b01, 0b10]

    Raises error when n is equal to 0 or 1 or concatenation of bitstring is smaller than input bits.
    """
    if n == 0 or n == 1:
        raise ValueError("n can not be 0 or 1")
    if bits >= 2 ** (n * size):
        raise ValueError("Input larger than concatenation of bitstrings")
    bitstrings = [(bits >> i * size) % 2 ** size for i in range(n)]
    bitstrings.reverse()
    return bitstrings


def yield_split(n: int, x_bits: int, x: int) -> Iterator[int]:
    """Split a number into bitstrings of given size.

    Returns n-bitstrings by removing the n most significant bits from x."""
    pass
