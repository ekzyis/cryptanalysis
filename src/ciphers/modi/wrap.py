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

from bitstring import Bits

from util.bitseq import fhex, bitseq_from_str, bitseq
from util.types import CipherFunction, Formatter


def output_wrapper(formatter: Formatter) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to cast the output into the specified format."""

    def _output_wrapper(cipher_fn: CipherFunction):
        def cfn_output_wrapped(key: Any, text: Any, *args: Any, **kwargs: Any) -> Any:
            return formatter(cipher_fn(key, text, *args, **kwargs))

        return cfn_output_wrapped

    return _output_wrapper


def text_input_wrapper(formatter: Formatter) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to cast cipher function text input into the specified format."""

    def _text_input_wrapper(cipher_fn: CipherFunction):
        def cfn_text_input_wrapped(key: Any, text: Any, *args: Any, **kwargs: Any) -> Any:
            return cipher_fn(key, formatter(text), *args, **kwargs)

        return cfn_text_input_wrapped

    return _text_input_wrapper


text_input_to_int_wrapper = text_input_wrapper(lambda text: int(text, 0))

fhex_output_wrapper = output_wrapper(fhex)

text_input_to_bitseq_wrapper = text_input_wrapper(bitseq_from_str)


def padder_wrapper(blocksize: int) -> Callable[[Bits], Bits]:
    """Return function which left-pads text input with zeros to fit blocksize."""

    def _padder(text: Bits):
        # add padding
        pad_amount = (blocksize - len(text) % blocksize) % blocksize
        if pad_amount != 0:
            padding = bitseq(0x0, bit=pad_amount)
            return padding + text
        return text

    return _padder


def text_input_padder(blocksize: int) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to left-pad text input with zeros to fit blocksize."""
    return text_input_wrapper(padder_wrapper(blocksize))


def key_input_wrapper(formatter: Formatter) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to cast key input into specified format."""

    def _key_input_wrapper(cipher_fn: CipherFunction):
        def cfn_key_input_wrapped(key: Any, text: Any, *args: Any, **kwargs: Any) -> Any:
            return cipher_fn(formatter(key), text, *args, **kwargs)

        return cfn_key_input_wrapped

    return _key_input_wrapper


def key_input_padder(keysize: int) -> Callable[[CipherFunction], CipherFunction]:
    """Return wrapper for cipher functions to left-pad key input with zeros to fit keysize.

    If the key is too long, then an error will be raised anyway during en-/decryption because
    the size does not match. This only helps for keys which are too small.
    """
    return key_input_wrapper(padder_wrapper(keysize))


key_input_to_bitseq_wrapper = key_input_wrapper(bitseq_from_str)
