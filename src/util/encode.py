"""Exports function which implement encoding.

Also exports encoding wrapper for ciphers.
"""
from typing import Union

from bitstring import Bits

from util.types import CipherFunction, Any


def encode(text: str, encoding: str = 'utf8') -> Bits:
    """Encode the input text with the given encoding and return a bitstring."""
    return Bits(text.encode(encoding))


def decode(b: Union[Bits, int], encoding: str = 'utf8') -> str:
    """Return the string which the given bitstring represents in the given encoding."""
    if type(b) is int:
        return bytes.fromhex(hex(b)[2:]).decode(encoding).lstrip('\x00')
    elif type(b) is Bits:
        return bytes.fromhex(b.hex).decode(encoding).lstrip('\x00')
    else:
        raise ValueError("input must be of type int or bitstring.Bit")


def encode_wrapper(cipher_fn: CipherFunction) -> CipherFunction:
    """Return wrapper for cipher functions to encode the text input before passing it to the cipher function."""

    def cipher_fn_wrapper(key: Bits, text: str, *args: Any, **kwargs: Any) -> Bits:
        return cipher_fn(key, encode(text), *args, **kwargs)

    return cipher_fn_wrapper


def decode_wrapper(cipher_fn: CipherFunction) -> CipherFunction:
    """Return wrapper for cipher functions to decode the output of the cipher function."""

    def cipher_fn_wrapper(key: Bits, text: Union[Bits, int], *args: Any, **kwargs: Any) -> str:
        return decode(cipher_fn(key, text, *args, **kwargs))

    return cipher_fn_wrapper
