"""Utility functions to create bitstrings."""
from typing import Union, Tuple

from bitstring import Bits

from util.count_int_str_bits import count_int_str_bits


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
    """Create a bitstring out of of n-bitstring from integer arguments."""
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


def bitseq32(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 32-bit strings."""
    return bitseq(*args, bit=32)


def bitseq64(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 64-bit strings."""
    return bitseq(*args, bit=64)


def bitseq128(*args: Union[Tuple[Union[int, Bits], ...], int, Bits]) -> Bits:
    """Create a bitstring out of 128-bit strings."""
    return bitseq(*args, bit=128)
