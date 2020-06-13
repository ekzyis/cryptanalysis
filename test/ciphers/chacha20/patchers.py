"""Decorators used for ChaCha20 tests."""
from unittest import mock


def iv_patch(*args, **kwargs):
    """Patch for Initialization vector."""
    return mock.patch('random.randrange', *args, **kwargs)


def initial_counter(value):
    """Patch for initial counter."""
    return mock.patch('ciphers.stream.chacha20.initial_counter', return_value=value)
