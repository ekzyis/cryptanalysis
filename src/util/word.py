"""Utility class to store bitstrings in a more readable way."""

from itertools import chain
from math import ceil
from typing import List, Any

from bitstring import Bits

from util.concat_bits import concat_bits
from util.count_int_str_bits import count_int_str_bits
from util.split import yield_split


def bitseq_from_str(*args: str) -> Bits:
    argstr = ""
    for arg in args:
        bit = count_int_str_bits(arg)
        argstr += "uint:{}={}".format(arg, bit)
    argstr = argstr[:-1]
    return Bits(argstr)


def bitseq(*args: int, bit: int) -> Bits:
    argstr = ""
    for arg in args:
        argstr += "uint:{}={},".format(arg, bit)
    argstr = argstr[:-1]
    return Bits(argstr)


def bitseq8(*args: int) -> Bits:
    return bitseq(*args, bit=8)


def bitseq32(*args: int) -> Bits:
    return bitseq(*args, bit=32)


def bitseq64(*args: int) -> Bits:
    return bitseq(*args, bit=64)


class Word(int):
    """Words represent integers but can be created in way which is easier to read.

    For example, the word 0xffffffffffffffff consists of four times 0xffff and thus
    can be created for easier reading using this syntax:
        Word(0xffff, 0xffff, 0xffff, 0xffff, bit=16)
    or
        Word((0xffff,) * 4, bit=16)
    """

    # TODO args should actually be hinted with Union[int, Tuple[int, ...]]
    def __new__(cls, *args: Any, bit) -> 'Word':
        """Create an actual integer out of the word representation given with args and bit."""
        _args: List[Any] = list(args)
        if isinstance(args[0], tuple):
            _args = [a for a in chain(*args)]
        # TODO mypy throws error: Too many arguments for "__new__" of "object"
        return int.__new__(cls, concat_bits(*_args, n=bit))

    def __init__(self, *args: Any, bit: int = 32) -> None:
        """Initialize the word by saving the passed-in attributes for later usage."""
        super().__init__()
        self.blocks = args
        self.bit = bit
        self.bits = len(self.blocks) * self.bit

    def __iter__(self):
        """Return an iterator to the blocks of bytes."""
        return self.blocks.__iter__()

    def __getitem__(self, i):
        """Return the i-th block."""
        return self.blocks[i]

    def hex(self):
        return "{0:#0{1}x}".format(self, ceil(self.bits / 4) + 2)

    def littleendian(self):
        """Return integer in little-endian format."""
        b = [x for x in yield_split(8, len(self.blocks) * self.bit, self)]
        b.reverse()
        return Word(*b, bit=8)
