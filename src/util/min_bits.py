from math import ceil, log2


def min_bits(x):
    """Returns the amount of bits needed to represent this number.
    For example. to represent 8, 4 bits are needed: 0b1000.
    To represent 7, only 3 bits are needed: 0b111.
    Notice, that 2**4 = 16 and not 8. 16 needs five bits because
    we start counting the bits at zero. Therefore, from 0 to 4 there are 5 bits
    and thus 16 needs 5 bits to represent: 0b10000."""
    return ceil(log2(x + 1))
