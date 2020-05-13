from ciphers.modi.ecb import ecb
from util.encode import encode_wrapper, decode_wrapper


def get_wrapped_cipher_functions(encrypt, decrypt, args):
    """Returns the correctly wrapped encryption and decryption functions."""
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
    ecb_mode = args['-m'] == 'ecb'
    utf8_mode = args['-x'] == 'utf8'
    blocksize = args['blocksize']
    w_encrypt, w_decrypt = encrypt, decrypt
    if ecb_mode and utf8_mode:
        w_encrypt = encode_wrapper(ecb(encrypt, blocksize))
        w_decrypt = text_int_wrapper(decode_wrapper(ecb(decrypt, blocksize)))
    if ecb_mode and not utf8_mode:
        w_encrypt = text_int_wrapper(ecb(encrypt, blocksize))
        w_decrypt = text_int_wrapper(ecb(decrypt, blocksize))
    if not ecb_mode and utf8_mode:
        w_encrypt = encode_wrapper(encrypt)
        w_decrypt = decode_wrapper(text_int_wrapper(decrypt))
    if not ecb_mode and not utf8_mode:
        w_encrypt = text_int_wrapper(encrypt)
        w_decrypt = text_int_wrapper(decrypt)

    # Only format the output if we are not decrypting and using encoding since encoding would format the output
    #   itself already
    _format = {'bin': bin, 'oct': oct, 'dec': str, 'hex': hex}
    # This should not be able to cause an KeyError because we already checked that all enum arguments are valid
    formatter = _format[args['-o']]
    w_encrypt = format_wrapper(w_encrypt, formatter)
    if not utf8_mode:
        w_decrypt = format_wrapper(w_decrypt, formatter)

    return w_encrypt, w_decrypt


def format_wrapper(cipher_fn, formatter):
    """Wrapper for cipher functions to cast the output into the specified format"""

    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return formatter(cipher_fn(key, text, *args, **kwargs))

    return cipher_fn_wrapper


def text_int_wrapper(cipher_fn):
    """Wrapper for cipher functions to cast the text input to int before passing it to the cipher function."""

    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return cipher_fn(key, int(text, 0), *args, **kwargs)

    return cipher_fn_wrapper
