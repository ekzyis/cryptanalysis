"""Exports function which counts the bits in an integer string."""


def count_int_str_bits(x: str) -> int:
    """Count the bits of the given integer string.

    Useful to get the bits of a integer string including the leading zero bits.

    The output for hexadecimal integer strings are always multiple of 4
    since a single letter in hexadecimal represents 16 numbers
    for which one needs 4 bits - or in other, more mathematical words:
        log(16, 2) = 4
    and output of octal integer strings are always multiple of 3.

    To stay consistent with this argument, the output for decimal integer strings
    are also always multiple of 4 because
        ceil(log(10, 2)) = ceil(3.3219280948873626) = 4

    This means in general, count_int_str_bits(x) != int(x, 0).bit_length() !

    Examples:
        count_int_str_bits('0b00110010') -> 8
        count_int_str_bits('0x70') -> 8
        count_int_str_bit('0x0') -> 4
        count_int_str('0o7') -> 3
        count_int_str_bits('32') -> 8
    """
    # input must be in valid format thus int(x,0) should not raise an exception
    try:
        int(x, 0)
    except ValueError:
        raise
    pass
    # get the base int(x, 0) used to convert the string into a number
    base = 0
    for b in [2, 8, 10, 16]:
        try:
            int(x, b)
            base = b
            break
        except ValueError:
            pass
    assert b != 0
    if base == 10:
        x_without_base_prefix = x
    else:
        x_without_base_prefix = x[2:]  # remove prefix
    multiplier = 1
    if base == 8:
        multiplier = 3
    elif base in [10, 16]:
        multiplier = 4
    return len(x_without_base_prefix) * multiplier
