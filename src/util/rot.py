"""Exports functions which implement bit rotation."""
from bitstring import Bits


def rot_left_bits(bits: Bits, i: int) -> Bits:
    """Bit rotation / Circular shift to the left for bitstring.Bits.

    Wrapper for rot_left.
    """
    rotated = rot_left(bits.uint, i, len(bits))
    return Bits("uint:{}={}".format(len(bits), rotated))


def rot_left(bits: int, i: int, max_bit: int) -> int:
    """Bit rotation / Circular shift to the left.

    Shifts i bits to the left and adds the bits that fall of to the right side.
    max_bit defines the "bit border" after which bits are wrapped around.
    Raises ValueError when max_bit is smaller than the highest bit in bits.
    """
    if bits > 2 ** max_bit:
        raise ValueError("max_bit is smaller than highest bit in bits")
    return ((bits % 2 ** (max_bit - i)) << i) | (bits >> (max_bit - i))


def rot_right(bits: int, i: int, max_bit: int) -> int:
    """Bit rotation / Circular shift to the right.

    Shifts i bits to the right and adds the bits that fall of to the left side.
    max_bit defines the bit at which bits from the right appear at the left.
    Raises ValueError when max_bit is smaller than the highest bit in bits.
    """
    if bits > 2 ** max_bit:
        raise ValueError("max_bit is smaller than highest bit in bits")
    return (bits >> i) | (bits % 2 ** i) << (max_bit - i)
