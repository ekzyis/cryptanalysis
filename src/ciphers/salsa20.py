"""Salsa20 implementation.

The specification found at https://cr.yp.to/snuffle/salsafamily-20071225.pdf is used as a reference
for this implementation.

Usage:
    salsa encrypt [options] KEY PLAINTEXT
    salsa decrypt [options] KEY CIPHERTEXT

    -n=N, --round-number=N  Number of rounds. Must be even. [default: 32]
    -o=[bin,hex,oct,dec]    Specifies the output format. [default: dec]
    -m=[ecb,none]           Specifies the mode of operation [default: none]
    -x=[utf8,none]          Specifies the encoding of the cipher-/plaintext. [default: none]

    KEY                     The key which should be used for en-/decryption.
    PLAINTEXT               The text to encrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
    CIPHERTEXT              The text to decrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
"""
