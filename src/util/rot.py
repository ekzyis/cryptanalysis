def rot_left(bits, i):
    """Bit rotation / Circular shift to the left.
    Shifts i bits to the left and adds the bits that fall of to the right side."""
    max_bit = 128
    while 2 ** max_bit > bits:
        max_bit -= 1
    max_bit += 1
    return ((bits % 2 ** (max_bit - i)) << i) | (bits >> (max_bit - i))


def rot_right(bits, i):
    """Bit rotation / Circular shift to the right.
    Shifts i bits to the right and adds the bits that fall of to the left side."""
    max_bit = 128
    while 2 ** max_bit > bits:
        max_bit -= 1
    max_bit += 1
    return (bits >> i) | (bits % 2 ** i) << (max_bit - i)
