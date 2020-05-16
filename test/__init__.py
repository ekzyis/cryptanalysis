"""Unit and integration tests for ciphers and util functions.

Tests are structured like this:

- ciphers:          Tests for modules in src.ciphers
    - feal:         Tests for FEAl-NX implementation,
    - salsa20:      Tests for Salsa20 implementation.
    - modi:         Tests for modes of operations.
- dca:              Tests which where written to assert statements in a master thesis. See tests for more information.
- util:             Tests for util functions.

If it helps clarity, each function of a module is given a own test file.
"""
