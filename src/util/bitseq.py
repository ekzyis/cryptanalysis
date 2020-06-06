"""Utility functions to create bitstrings."""

from bitstring import Bits

from util.count_int_str_bits import count_int_str_bits


def bitseq_from_str(*args: str) -> Bits:
    """Create a bitstring out of string arguments.

    The bits of each string argument will be calculated.
    """
    argstr = ""
    for arg in args:
        bit = count_int_str_bits(arg)
        argstr += "uint:{}={}".format(arg, bit)
    argstr = argstr[:-1]
    return Bits(argstr)


def bitseq(*args: int, bit: int) -> Bits:
    """Create a bitstring out of of n-bitstring from integer arguments."""
    argstr = ""
    for arg in args:
        argstr += "uint:{}={},".format(arg, bit)
    argstr = argstr[:-1]
    return Bits(argstr)


def bitseq8(*args: int) -> Bits:
    """Create a bitstring out of 8-bit strings."""
    return bitseq(*args, bit=8)


def bitseq32(*args: int) -> Bits:
    """Create a bitstring out of 32-bit strings."""
    return bitseq(*args, bit=32)


def bitseq64(*args: int) -> Bits:
    """Create a bitstring out of 64-bit strings."""
    return bitseq(*args, bit=64)
