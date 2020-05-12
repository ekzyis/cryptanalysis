def encode(text, encoding='utf8'):
    """Encodes the input text with the given encoding and returns a number."""
    return int(text.encode(encoding).hex(), 16)


def decode(number, encoding='utf8'):
    """Returns the string which the given number represents in the given encoding."""
    return bytes.fromhex(hex(number)[2:]).decode(encoding)


def text_int_wrapper(cipher_fn):
    """Wrapper for cipher functions to cast the text input to int before passing it to the cipher function."""
    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return cipher_fn(key, int(text, 0), *args, **kwargs)

    return cipher_fn_wrapper


def encode_wrapper(cipher_fn):
    """Wrapper for cipher functions to encode the text input before passing it to the cipher function."""
    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return cipher_fn(key, encode(text), *args, **kwargs)

    return cipher_fn_wrapper


def decode_wrapper(cipher_fn):
    """Wrapper for cipher functions to decode the output of the cipher function.
    Also casts the text input to int before cipher function execution."""
    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return decode(text_int_wrapper(cipher_fn)(key, text, *args, **kwargs))

    return cipher_fn_wrapper
