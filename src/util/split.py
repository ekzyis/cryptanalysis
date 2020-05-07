def split(n, size, bits):
    """Splits the input bits into n bitstrings with given size. The highest bits are returned first.
    Raises error when n is equal to 0 or 1 or concatenation of bitstring is smaller than input bits."""
    if n == 0 or n == 1:
        raise ValueError("n can not be 0 or 1")
    if bits >= 2 ** (n * size):
        raise ValueError("Input larger than concatenation of bitstrings")
    bitstrings = [(bits >> i * size) % 2 ** size for i in range(n)]
    bitstrings.reverse()
    return bitstrings
