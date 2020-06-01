"""Exports function which counts the bits in an integer string."""


def count_int_str_bits(x: str) -> int:
    """Count the bits of the given integer string.

    Useful to get the bits of a integer string including the leading zero bits.

    The output for hexadecimal integer strings are always multiple of 4
    since a single letter in hexadecimal represents 16 numbers
    for which one needs 4 bits - or in other, more mathematical words:
        log(16, 2) = 4

    To stay consistent with this argument, the output for decimal integer strings
    are also always multiple of 4 because
        ceil(log(10, 2)) = ceil(3.3219280948873626) = 4

    This means in general, count_int_str_bits(x) != int(x, 0).bit_length() !

    Examples:
        count_int_str_bits('0b00110010') -> 8
        count_int_str_bits('0x70') -> 8
        count_int_str_bit('0x0') -> 4
        count_int_str_bits('32') -> 8
    """
    pass
