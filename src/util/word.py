"""Utility class to store bitstrings in a more readable way."""

from util.concat_bits import concat_bits


class Word(int):
    def __new__(cls, *args, bit=32):
        """Creates an actual integer out of the word representation given with args and bit."""
        return int.__new__(cls, concat_bits(*args, n=bit))
