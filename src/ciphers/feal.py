#!/usr/bin/env python

"""
FEAL-NX Implementation.

The specification found at https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf is used as a reference
for this implementation.

It follows a short description of the cipher and its implementation:

    "In cryptography, FEAL (the Fast data Encipherment ALgorithm) is a block cipher proposed as an alternative
    to the Data Encryption Standard (DES), and designed to be much faster in software. The Feistel based algorithm
    was first published in 1987 by Akihiro Shimizu and Shoji Miyaguchi from NTT. The cipher is susceptible to various
    forms of cryptanalysis, and has acted as a catalyst in the discovery of differential and linear cryptanalysis."
    - Wikipedia, https://en.wikipedia.org/wiki/FEAL

    "FEAL, the Fast Data Encipherment Algorithm, is a 64-bit block cipher algorithm that enciphers 64-bit plaintexts
    into 64-bit ciphertexts and vice versa. FEAL has three options: key length, round number and key parity.
    The key length selects either 64-bit key or 128-bit key, the round number (N) specifies the internal iteration
    number for data randomization, and the key parity option selects either the use or non-use of parity bits in a key
    block. One subset of FEAL, called FEAL-NX, is N round FEAL using a 128-bit key without key parity."
    - NTT Secure Platform Laboratories, https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf

Usage:
    feal encrypt [options] KEY PLAINTEXT
    feal decrypt [options] KEY CIPHERTEXT

    -n=N, --round-number=N  Number of rounds. Must be even. [default: 32]
    -o=[bin,hex,oct,dec]    Specifies the output format. [default: dec]
    -m=[ecb,none]           Specifies the mode of operation [default: none]
    -x=[utf8,none]          Specifies the encoding of the cipher-/plaintext. [default: none]

    KEY                     The key which should be used for en-/decryption.
    PLAINTEXT               The text to encrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
    CIPHERTEXT              The text to decrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
"""

import sys
from pathlib import Path
from typing import Sequence, Tuple, Any, Optional

from docopt import docopt  # type: ignore

# make sure that following imports can be resolved when executing this script from cmdline

sys.path.insert(0, str(Path(__file__).parent / '..'))

from util.wrap import get_wrapped_cipher_functions
from util.concat_bits import concat_bits
from util.rot import rot_left
from util.split import split


def key_schedule(key: int, n: int = 32) -> Sequence[int]:
    """Return the subkeys created by the key scheduler of FEAL-NX.

    Creates the N+8 16-bit subkeys which are needed during en-/decryption.
    Raises error if key is not 128-bit.
    """
    if key >= 2 ** 128:
        raise ValueError("Key for FEAL-NX key scheduler must be 128-bit")
    kl, kr = split(2, 64, key)
    # processing of right key kr
    kr1, kr2 = split(2, 32, kr)
    # insert "filler" element such that the the first added element is at index 1
    #   since in the specification, indices for q start with 1
    q = [0x0]
    for r in range(1, (int(n / 2) + 5)):
        if r % 3 == 1:
            q.append(kr1 ^ kr2)
        elif r % 3 == 2:
            q.append(kr1)
        elif r % 3 == 0:
            q.append(kr2)
    # processing of left key kl
    a0, b0 = split(2, 32, kl)
    a = [a0]
    b = [b0]
    d = [0x0]
    k = []
    for r in range(1, int(n / 2) + 5):
        d.append(a[r - 1])
        a.append(b[r - 1])
        b.append(fk(a[r - 1], b[r - 1] ^ d[r - 1] ^ q[r]))
        br0, br1, br2, br3 = split(4, 8, b[r])
        k.append(concat_bits(br0, br1, n=8))
        k.append(concat_bits(br2, br3, n=8))
    return k


def s0(a: int, b: int) -> int:
    """Return substitution value of S-Box 0."""
    return _s(a, b, 0)


def s1(a: int, b: int) -> int:
    """Return substitution value of S-Box 1."""
    return _s(a, b, 1)


def _s(a: int, b: int, i: int) -> int:
    """General substitution box implementation for FEAL-NX."""
    return rot_left((a + b + i) % 256, 2, 8)


def f(a: int, b: int) -> int:
    """f-function of FEAL-NX.

    a must be 32-bit and b must be 16-bit long.
    Used during en-/decryption.
    See section 5.1 and figure 3 in
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
    """
    if a >= 2 ** 32:
        raise ValueError("a key must be 32-bit")
    if b >= 2 ** 16:
        raise ValueError("b key must be 16-bit")
    a_k = split(n=4, size=8, bits=a)
    b_k = split(n=2, size=8, bits=b)
    f1 = a_k[1] ^ b_k[0]
    f2 = a_k[2] ^ b_k[1]
    f1 ^= a_k[0]
    f2 ^= a_k[3]
    f1 = s1(f1, f2)
    f2 = s0(f2, f1)
    f0 = s0(a_k[0], f1)
    f3 = s1(a_k[3], f2)
    return concat_bits(f0, f1, f2, f3, n=8)


def fk(a: int, b: int) -> int:
    """f_k-function of FEAL-NX.

    Input keys must be 32-bit.
    Used during key schedule to generate the subkeys for each iteration.
    See section 5.2 and figure 4 in
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
    """
    if a >= 2 ** 32 or b >= 2 ** 32:
        raise ValueError("Input keys must be 32-bit")
    a_k = split(n=4, size=8, bits=a)
    b_k = split(n=4, size=8, bits=b)
    fk1 = a_k[1] ^ a_k[0]
    fk2 = a_k[2] ^ a_k[3]
    fk1 = s1(fk1, fk2 ^ b_k[0])
    fk2 = s0(fk2, fk1 ^ b_k[1])
    fk0 = s0(a_k[0], fk1 ^ b_k[2])
    fk3 = s1(a_k[3], fk2 ^ b_k[3])
    return concat_bits(fk0, fk1, fk2, fk3, n=8)


def _encrypt_preprocessing(subkeys: Sequence[int], text: int) -> int:
    p = text ^ concat_bits(*subkeys, n=16)
    l0, r0 = split(2, 32, p)
    p ^= l0
    return p


def _decrypt_preprocessing(subkeys: Sequence[int], text: int) -> int:
    p = text ^ concat_bits(*subkeys, n=16)
    rn, ln = split(2, 32, p)
    p = concat_bits(rn, ln, n=32) ^ rn
    return p


def _encrypt_iterative_calculation(l0: int, r0: int, sk: Sequence[int], n: int = 32) \
        -> Tuple[Sequence[int], Sequence[int]]:
    l, r = [l0], [r0]
    for i in range(1, n + 1):
        r.append(l[i - 1] ^ f(r[i - 1], sk[i - 1]))
        l.append(r[i - 1])
    return l, r


def _decrypt_iterative_calculation(ln: int, rn: int, sk: Sequence[int], n: int = 32) \
        -> Tuple[Sequence[int], Sequence[int]]:
    l, r = [0] * n + [ln], [0] * n + [rn]
    for i in reversed(range(1, n + 1)):
        l[i - 1] = r[i] ^ f(l[i], sk[i - 1])
        r[i - 1] = l[i]
    return l, r


def encrypt(key: int, text: int, *args: Any, **kwargs: Any) -> int:
    """Encrypt the text with the given key using FEAL-NX encryption.

    Raises error if text is longer than 64-bit or key is longer than 128-bit.
    Raises error if text or key is not a number.
    """
    n = kwargs.setdefault('n', 32)
    if type(text) is not int:
        raise ValueError("Plaintext must be a number")
    if type(key) is not int:
        raise ValueError("Key must be a number")
    if text >= 2 ** 64:
        raise ValueError("Plaintext must be 64-bit")
    if key >= 2 ** 128:
        raise ValueError("Key must be 128-bit")
    sk = key_schedule(key, n)
    l0, r0 = split(2, 32, _encrypt_preprocessing(sk[n:n + 4], text))
    l, r = _encrypt_iterative_calculation(l0, r0, sk, n)
    ln, rn = l[n], r[n]
    c = concat_bits(rn, ln, n=32) ^ rn
    c ^= concat_bits(sk[n + 4], sk[n + 5], sk[n + 6], sk[n + 7], n=16)
    return c


def decrypt(key: int, text: int, *args: Any, **kwargs: Any) -> int:
    """Decrypt the ciphertext with the given key using FEAL-NX decryption.

    Raises error if text is longer than 64-bit or key is longer than 128-bit.
    Raises error if text or key is not a number.
    """
    n = kwargs.setdefault('n', 32)
    if type(text) is not int:
        raise ValueError("Ciphertext must be a number")
    if type(key) is not int:
        raise ValueError("Key must be a number")
    if text >= 2 ** 64:
        raise ValueError("Ciphertext must be 64-bit")
    if key >= 2 ** 128:
        raise ValueError("Key must be 128-bit")
    sk = key_schedule(key, n)
    rn, ln = split(2, 32, _decrypt_preprocessing(sk[n + 4:n + 8], text))
    l, r = _decrypt_iterative_calculation(ln, rn, sk, n)
    l0, r0 = l[0], r[0]
    p = concat_bits(l0, r0, n=32) ^ l0
    p ^= concat_bits(sk[n], sk[n + 1], sk[n + 2], sk[n + 3], n=16)
    return p


def feal() -> Optional[int]:
    """Execute FEAL-NX cipher with arguments given on comand line.

    Gets arguments from docopt which parses sys.argv.
    See http://docopt.org/ if you are not familiar with docopt argument parsing.
    """
    args = docopt(__doc__)

    # Wrap encrypt and decrypt functions depending on arguments given on cmdline
    args['blocksize'] = 64
    _encrypt, _decrypt = get_wrapped_cipher_functions(encrypt, decrypt, args)

    text = args['PLAINTEXT'] or args['CIPHERTEXT']
    n = int(args['--round-number'])
    k = int(args['KEY'], 0)
    if args['encrypt']:
        return _encrypt(k, text, n=n)
    elif args['decrypt']:
        return _decrypt(k, text, n=n)
    return None


if __name__ == "__main__":
    try:
        print(feal())
    except ValueError as e:
        print(e)
        exit(1)
