"""Decorators used for ChaCha20 tests."""
from unittest import mock


def iv(value):
    """Patch for Initialization vector."""
    return mock.patch('random.randrange', return_value=value)


def initial_counter(value):
    """Patch for initial counter."""
    return mock.patch('ciphers.stream.chacha.initial_counter', return_value=value)
