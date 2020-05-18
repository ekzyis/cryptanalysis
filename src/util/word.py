"""Utility class to store bitstrings in a more readable way."""

from itertools import chain

from util.concat_bits import concat_bits


class Word(int):
    def __new__(cls, *args: int, bit: int = 32) -> 'Word':
        """Creates an actual integer out of the word representation given with args and bit."""
        if isinstance(args[0], tuple):
            args = [a for a in chain(*args)]
        return int.__new__(cls, concat_bits(*args, n=bit))
