def encode(text, encoding='utf8'):
    """Encodes the input text with the given encoding and returns a number."""
    return int(text.encode(encoding).hex(), 16)


def decode(number, encoding='utf8'):
    """Returns the string which the given number represents in the given encoding."""
    return bytes.fromhex(hex(number)[2:]).decode(encoding)
