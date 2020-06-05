"""Implements wrapping for en- and decryption of _block ciphers_.

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
from typing import Tuple, Any, Mapping

from ciphers.modi.ecb import ecb
from util.encode import encode_wrapper, decode_wrapper
from util.types import CipherFunction, BlockCipherOptions, Formatter


def wrap_block_cipher_functions(encrypt: CipherFunction, decrypt: CipherFunction,
                                args: BlockCipherOptions) -> Tuple[CipherFunction, CipherFunction]:
    """Return the correctly wrapped encryption and decryption functions for block ciphers."""
    """When parsing arguments, the following execution order has to be ensured:
        ===========================================================================
        `feal -x utf8 -m ecb encrypt k m`
         |
         | (k: int, m: str)
         |
         -> [ENCODE]: ENCODE MESSAGE
                |
                | (k: int, encoded_m: int)
                |
                -> [ECB]: SPLIT MESSAGE
                     |
                     | (k: int, m_blocks: [int])
                     |
                     -------------------------------
                     |        |    ...    |        |
                     |        |           |        | (k: int, m_block: int)
                     v        v           v        v
                 [ENCRYPT][ENCRYPT]   [ENCRYPT][ENCRYPT]
                     |        |           |        |
                     |        |           |        | (k: int, encrypted_m_block: int)
                     v        v           v        v
                     -------------------------------
                                    |
                                    | (encrypted_m_blocks: [int])
                                    v
                            [ECB]: CONCAT ENCRYPTED BLOCKS
                                    |
         ----------------------------
         |
         | (encrypted_message: int)
         v
         OUTPUT
        ===========================================================================
         `feal -x utf8 -m ecb ecb decrypt k m`
         |
         | (k: int, m: int)
         |
         --------> [ECB]: SPLIT MESSAGE
                     |
                     | (k: int, m_blocks: [int]
                     |
                     -------------------------------
                     |        |    ...    |        |
                     |        |           |        | (k: int, m_block: int)
                     v        v           v        v
                 [DECRYPT][DECRYPT]   [DECRYPT][DECRYPT]
                     |         |           |       |
                     |         |           |       |
                     v         v           v       v
                     -------------------------------
                               |
                               | (decrypted_m_blocks: [int]
                               v
                       [ECB]: CONCAT DECRYPTED BLOCKS
                               |
            --------------------
            |
            | (decrypted_message: int)
         [DECODE]
            |
         ----
         |
         v
         OUTPUT
        ===========================================================================
        """

    n = int(args['--round-number'])
    ecb_mode: bool = args['-m'] == 'ecb'
    utf8_mode: bool = args['-x'] == 'utf8'
    blocksize: int = args['blocksize']

    # Check if enum arguments are valid
    if args['-x'] not in ['utf8', 'none']:
        raise ValueError("Encoding must be utf8 or none.")
    if args['-m'] not in ['ecb', 'none']:
        raise ValueError("Mode must be ecb or none.")
    if args['-o'] not in ['bin', 'oct', 'dec', 'hex']:
        raise ValueError("Output format must be bin, oct, dec or hex.")
    if n % 2 == 1:
        raise ValueError("Round number must be even.")

    w_encrypt, w_decrypt = encrypt, decrypt
    if ecb_mode and utf8_mode:
        w_encrypt = encode_wrapper(ecb(encrypt, blocksize))
        w_decrypt = text_int_wrapper(decode_wrapper(ecb(decrypt, blocksize)))
    elif ecb_mode and not utf8_mode:
        w_encrypt = text_int_wrapper(ecb(encrypt, blocksize))
        w_decrypt = text_int_wrapper(ecb(decrypt, blocksize))
    elif not ecb_mode and utf8_mode:
        w_encrypt = encode_wrapper(encrypt)
        w_decrypt = decode_wrapper(text_int_wrapper(decrypt))
    elif not ecb_mode and not utf8_mode:
        w_encrypt = text_int_wrapper(encrypt)
        w_decrypt = text_int_wrapper(decrypt)

    # Only format the output if we are not decrypting and using encoding since encoding would format the output
    #   itself already
    _format: Mapping[str, Formatter] = {'bin': bin, 'oct': oct, 'dec': str, 'hex': hex}
    # This should not be able to cause an KeyError because we already checked that all enum arguments are valid
    formatter = _format[args['-o']]
    w_encrypt = format_output_wrapper(w_encrypt, formatter)
    if not utf8_mode:
        w_decrypt = format_output_wrapper(w_decrypt, formatter)

    return w_encrypt, w_decrypt


def format_output_wrapper(cipher_fn: CipherFunction, formatter: Formatter) -> CipherFunction:
    """Return wrapper for cipher functions to cast the output into the specified format."""

    def cipher_fn_wrapper(key: int, text: Any, *args: Any, **kwargs: Any) -> Any:
        return formatter(cipher_fn(key, text, *args, **kwargs))

    return cipher_fn_wrapper


def text_int_wrapper(cipher_fn: CipherFunction) -> CipherFunction:
    """Return wrapper for cipher functions which casts text input to numbers."""
    return format_input_wrapper(cipher_fn, lambda text: int(text, 0))


def format_input_wrapper(cipher_fn: CipherFunction, formatter: Formatter) -> CipherFunction:
    """Return wrapper for cipher functions to cast cipher function text input into the specified format."""

    def cipher_fn_wrapper(key: int, text: int, *args: Any, **kwargs: Any) -> Any:
        return cipher_fn(key, formatter(text), *args, **kwargs)

    return cipher_fn_wrapper
