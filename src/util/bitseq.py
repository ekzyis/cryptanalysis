"""Utility functions to create bitstrings."""
from typing import Union, Tuple, Sequence

from bitstring import Bits

from util.count_int_str_bits import count_int_str_bits


def bitseq_add(b1: Bits, b2: Bits) -> Bits:
    """Adds the values of the two bitstrings together modulo their length.

    Raises error if the bitstrings are not of same length."""
    if len(b1) != len(b2):
        raise ValueError("Bitstrings must be of same length for addition.")
    return bitseq((b1.uint + b2.uint) & 2 ** len(b1) - 1, bit=len(b1))


def bitseq_split(size: int, b: Bits, n=None) -> Union[Bits, Sequence[Bits]]:
    """Split the bitstring into n bitstrings of given size.

    If n is None, try to split the full bitstring.
    If n == 1, returns a single bitstring (no list).
    Raises error if n is None and size is greater than the length.
    Raises error if combination of n and size would lead to "oversplitting", for example when trying to split a
    64-bitstring into 3 32-bitstrings."""
    if size <= 0:
        raise ValueError("size must be greater than 0")
    if n is None:
        if size > len(b):
            raise ValueError("size {} would lead to oversplitting of {}".format(size, b))
        return [b[i:i + size] for i in range(0, len(b), size)]
    else:
        if n <= 0:
            raise ValueError("n must be greater than 0")
        if size * n > len(b):
            raise ValueError("size {} with n {} would lead to oversplitting of {}".format(size, n, b))
        split = [b[i:i + size] for i in range(0, len(b), size)][:n]
        if n == 1:
            return split[0]
        return split


def fhex(b: Bits) -> str:
    """Return full hex string representation of Bits. Workaround for truncation issue in Bits.__str__."""
    if len(b) % 4 != 0:
        raise ValueError("bitstring length must be multiple of 4.")
    return "0x" + hex(b.uint)[2:].zfill(int(len(b) / 4))


def bitseq_from_str(*args: Union[Tuple[str, ...], str], bit: int = None) -> Bits:
    """Create a bitstring out of string arguments.

    The bits of each string argument will be calculated.
    """
    argstr = ""

    def add_to_argstr(argstr_: str, arg_to_add: str) -> str:
        bit_ = bit or count_int_str_bits(arg_to_add)
        argstr_ += "uint:{}={},".format(bit_, int(arg_to_add, 0))
        return argstr_

    for arg in args:
        if isinstance(arg, tuple):
            for tuple_arg in arg:
                argstr = add_to_argstr(argstr, tuple_arg)
        else:
            argstr = add_to_argstr(argstr, arg)

    argstr = argstr[:-1]
    return Bits(argstr)


def littleendian(b: Bits) -> Bits:
    """Return the bitstring.Bits in little endian.

    Example:
        littleendian(Bits("0x123456")) -> Bits("0x563412")
        littleendian(Bits("0x1234")) -> Bits("0x3412")
    """
    le = b.uintle
    return Bits("uint:{}={}".format(len(b), le))


def bitseq(*args: Union[Tuple[Union[int, Bits], ...], int, Bits], bit: int) -> Bits:
    """Create a bitstring out of n-bitstring from integer arguments."""
    argstr = ""

    def add_to_argstr(argstr_: str, arg_to_add: Union[int, Bits]) -> str:
        if isinstance(arg_to_add, Bits):
            arg_to_add = arg_to_add.uint
        argstr_ += "uint:{}={},".format(bit, int(arg_to_add))
        return argstr_

    for arg in args:
        if isinstance(arg, tuple):
            for tuple_arg in arg:
                argstr = add_to_argstr(argstr, tuple_arg)
        else:
            argstr = add_to_argstr(argstr, arg)
    argstr = argstr[:-1]
    return Bits(argstr)


def bitseq8(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 8-bit strings."""
    return bitseq(*args, bit=8)


def bitseq16(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 16-bit strings."""
    return bitseq(*args, bit=16)


def bitseq32(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 32-bit strings."""
    return bitseq(*args, bit=32)


def bitseq64(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 64-bit strings."""
    return bitseq(*args, bit=64)


def bitseq128(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 128-bit strings."""
    return bitseq(*args, bit=128)


def bitseq256(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 256-bit strings."""
    return bitseq(*args, bit=256)


def bitseq512(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 512-bit strings."""
    return bitseq(*args, bit=512)
