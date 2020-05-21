"""Exports function to limit bits to its a given amount of its most significant bits."""


def limit(x: int, x_bits: int, n: int) -> int:
    """Limit the bits of x by only using the n most significant bits of x."""
    return x >> (x_bits - n)
