from math import ceil, log2


def min_bits(x):
    """Returns the amount of bits needed to represent this number.
    For example. to represent 8, 4 bits are needed: 0b1000.
    To represent 7, only 3 bits are needed: 0b111."""
    return ceil(log2(x + 1))
