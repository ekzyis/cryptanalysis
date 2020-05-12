def encode(text, encoding='utf8'):
    """Encodes the input text with the given encoding and returns a number."""
    return int(text.encode(encoding).hex(), 16)


def decode(number, encoding='utf8'):
    """Returns the string which the given number represents in the given encoding."""
    return bytes.fromhex(hex(number)[2:]).decode(encoding)


def feal_text_int_wrap(cipher_fn):
    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return cipher_fn(key, int(text, 0), *args, **kwargs)

    return cipher_fn_wrapper


def feal_encode(cipher_fn):
    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return cipher_fn(key, encode(text), *args, **kwargs)

    return cipher_fn_wrapper


def feal_decode(cipher_fn):
    def cipher_fn_wrapper(key, text, *args, **kwargs):
        return decode(feal_text_int_wrap(cipher_fn)(key, text, *args, **kwargs))

    return cipher_fn_wrapper
