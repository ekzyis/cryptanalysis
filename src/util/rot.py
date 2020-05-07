def rot_left(bits, i, max_bit):
    """Bit rotation / Circular shift to the left.
    Shifts i bits to the left and adds the bits that fall of to the right side.
    max_bit defines the "bit border" after which bits are wrapped around.
    Raises ValueError when max_bit is smaller than the highest bit in bits."""
    if bits > 2**max_bit:
        raise ValueError("max_bit is smaller than highest bit in bits")
    return ((bits % 2 ** (max_bit - i)) << i) | (bits >> (max_bit - i))


def rot_right(bits, i, max_bit):
    """Bit rotation / Circular shift to the right.
    Shifts i bits to the right and adds the bits that fall of to the left side.
    max_bit defines the bit at which bits from the right appear at the left.
    Raises ValueError when max_bit is smaller than the highest bit in bits."""
    if bits > 2**max_bit:
        raise ValueError("max_bit is smaller than highest bit in bits")
    return (bits >> i) | (bits % 2 ** i) << (max_bit - i)
