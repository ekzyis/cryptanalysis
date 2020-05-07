def concat_bits(*args, n):
    """Concatenates the given subkeys into one key.
    The first key is shifted to the highest n-bits, the second key to the second highest n-bits and so forth.
    Raises error when one subkey is larger than n."""
    args = list(args)  # convert args to list because *args creates tuple
    args.reverse()
    r = 0
    for i, arg in enumerate(args):
        if arg > 2 ** n:
            raise ValueError("subkey is larger than slot given by n")
        r |= arg << (i*n)
    return r
