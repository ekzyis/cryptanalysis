"""Exports function which concatenates bitstrings into one bitstring."""


def concat_bits(*args: int, n: int) -> int:
    """Concatenates the given bitstring arguments into one bitstring.

    The first key is shifted to the most significant n-bits, the second key to the second most significant n-bits
    and so forth.
    Raises error when one subkey is larger than n.
    """
    args_ = list(args)  # convert args to list because *args creates tuple
    args_.reverse()
    r = 0
    for i, arg in enumerate(args_):
        if arg.bit_length() > n:
            raise ValueError("bitstring is larger than slot given by n")
        r |= arg << (i * n)
    return r
