"""Implements wrapping for en- and decryption.

Wrappers are for example functions which implement ECB or encoding.
The wrappers are implemented to be general purpose. One can pass cipher functions to them
and a function which has the same interface as the unwrapped cipher function is returned.
This hides the implementation of the wrapper; making them easier to use with many different ciphers.

For example, ecb(encrypt) would return a function which can be interacted with the same as if
the function would not be wrapped with `ecb`.
The only difference is that that now one can use larger strings since `ecb` will split them
and pass them individually to `encrypt` and then return the concatentation of the encrypted blocks
- which is exactly what ECB mode does.
"""
from typing import Any, Callable

from util.bitseq import fhex, bitseq_from_str
from util.types import CipherFunction, Formatter


def output_wrapper(formatter: Formatter) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to cast the output into the specified format."""

    def _wrapper(cipher_fn: CipherFunction):
        def cipher_fn_wrapper(key: Any, text: Any, *args: Any, **kwargs: Any) -> Any:
            return formatter(cipher_fn(key, text, *args, **kwargs))

        return cipher_fn_wrapper

    return _wrapper


def text_input_wrapper(formatter: Formatter) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to cast cipher function text input into the specified format."""

    def _wrapper(cipher_fn: CipherFunction):
        def cipher_fn_wrapper(key: Any, text: Any, *args: Any, **kwargs: Any) -> Any:
            return cipher_fn(key, formatter(text), *args, **kwargs)

        return cipher_fn_wrapper

    return _wrapper


text_input_to_int_wrapper = text_input_wrapper(lambda text: int(text, 0))

fhex_output_wrapper = output_wrapper(fhex)

text_input_to_bitseq_wrapper = text_input_wrapper(bitseq_from_str)


def key_input_wrapper(formatter: Formatter) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to cast key input into specified format."""

    def _wrapper(cipher_fn: CipherFunction):
        def cipher_fn_wrapper(key: Any, text: Any, *args: Any, **kwargs: Any) -> Any:
            return cipher_fn(formatter(key), text, *args, **kwargs)

        return cipher_fn_wrapper

    return _wrapper


key_input_to_bitseq_wrapper = key_input_wrapper(bitseq_from_str)
