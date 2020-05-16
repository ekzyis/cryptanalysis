"""Exports function which implement encoding.

Also exports encoding wrapper for ciphers.
"""
from util.types import CipherFunction, Any


def encode(text: str, encoding: str = 'utf8') -> int:
    """Encode the input text with the given encoding and returns a number."""
    return int(text.encode(encoding).hex(), 16)


def decode(number: int, encoding: str = 'utf8') -> str:
    """Return the string which the given number represents in the given encoding."""
    return bytes.fromhex(hex(number)[2:]).decode(encoding)


def encode_wrapper(cipher_fn: CipherFunction) -> CipherFunction:
    """Return wrapper for cipher functions to encode the text input before passing it to the cipher function."""

    def cipher_fn_wrapper(key: int, text: str, *args: Any, **kwargs: Any) -> int:
        return cipher_fn(key, encode(text), *args, **kwargs)

    return cipher_fn_wrapper


def decode_wrapper(cipher_fn: CipherFunction) -> CipherFunction:
    """Return wrapper for cipher functions to decode the output of the cipher function."""

    def cipher_fn_wrapper(key: int, text: int, *args: Any, **kwargs: Any) -> str:
        return decode(cipher_fn(key, text, *args, **kwargs))

    return cipher_fn_wrapper
