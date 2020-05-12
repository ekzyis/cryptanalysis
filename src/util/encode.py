def encode(text, encoding='utf8'):
    """Encodes the input text with the given encoding and returns a number."""
    return int(text.encode(encoding).hex(), 16)


def decode(number, encoding='utf8'):
    """Returns the string which the given number represents in the given encoding."""
    return bytes.fromhex(hex(number)[2:]).decode(encoding)


def encode_wrapper(cipher_fn):
    """Wrapper for cipher functions to encode the text input before passing it to the cipher function."""

    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return cipher_fn(key, encode(text), *args, **kwargs)

    return cipher_fn_wrapper


def decode_wrapper(cipher_fn):
    """Wrapper for cipher functions to decode the output of the cipher function."""

    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return decode(cipher_fn(key, text, *args, **kwargs))

    return cipher_fn_wrapper
