#!/usr/bin/env python

"""Salsa20/r implementation.

The specification found at https://cr.yp.to/snuffle/spec.pdf is used as a reference
for this implementation.

Usage:
    salsa20 encrypt [options] KEY PLAINTEXT
    salsa20 decrypt [options] KEY CIPHERTEXT

    -r=[8,12,20]            Number of rounds. [default: 20]
    -o=[bin,hex,oct,dec]    Specifies the output format. [default: dec]
    -x=[utf8,none]          Specifies the encoding of the cipher-/plaintext. [default: none]

    KEY                     The key which should be used for en-/decryption.
    PLAINTEXT               The text to encrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
    CIPHERTEXT              The text to decrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
"""

import random
import sys
from functools import reduce
from math import ceil
from pathlib import Path
from time import time
from typing import Any, Optional

from bitstring import Bits, pack
from docopt import docopt  # type: ignore

# make sure that following imports can be resolved when executing this script from cmdline
sys.path.insert(0, str(Path(__file__).parent / '..'))

from util.wrap import wrap_stream_cipher_functions
from util.rot import rot_left_bits
from util.word import Word
from util.bitseq import bitseq_from_str, bitseq8, bitseq32


def quarterround(y: Bits) -> Bits:
    """Calculate the quarterround value of the input as specified in the paper.

    Returns a 128-bit value.
    Raises error if input is not 128-bit.
    """
    if len(y) != 128:
        raise ValueError("Input must be 128-bit.")

    y0, y1, y2, y3 = y[0:32], y[32:64], y[64:96], y[96:128]
    z1 = y1 ^ rot_left_bits((bitseq32(y0.uint + y3.uint & 0xFFFFFFFF)), 7)
    z2 = y2 ^ rot_left_bits((bitseq32(z1.uint + y0.uint & 0xFFFFFFFF)), 9)
    z3 = y3 ^ rot_left_bits((bitseq32(z2.uint + z1.uint & 0xFFFFFFFF)), 13)
    z0 = y0 ^ rot_left_bits((bitseq32(z3.uint + z2.uint & 0xFFFFFFFF)), 18)
    return z0 + z1 + z2 + z3


def rowround(y_: Bits) -> Bits:
    """Calculate the rowround value of the input as specified in the paper.

    Returns a 512-bit value.
    Raises error if input is not 512-bit.
    """
    if len(y_) != 512:
        raise ValueError("Input must be 512-bit.")
    y = [y_[i:i + 32] for i in range(0, 512, 32)]
    z = [None] * 16
    q = quarterround(bitseq32(y[0], y[1], y[2], y[3]))
    z[0], z[1], z[2], z[3] = [q[i:i + 32] for i in range(0, 128, 32)]
    q = quarterround(bitseq32(y[5], y[6], y[7], y[4]))
    z[5], z[6], z[7], z[4] = [q[i:i + 32] for i in range(0, 128, 32)]
    q = quarterround(bitseq32(y[10], y[11], y[8], y[9]))
    z[10], z[11], z[8], z[9] = [q[i:i + 32] for i in range(0, 128, 32)]
    q = quarterround(bitseq32(y[15], y[12], y[13], y[14]))
    z[15], z[12], z[13], z[14] = [q[i:i + 32] for i in range(0, 128, 32)]
    return bitseq32(*z)


def columnround(x_: Bits) -> Bits:
    """Calculate the columnround value of the input as specified in the paper.

    Returns a 512-bit value.
    Raises error if input is not 512-bit.
    """
    if len(x_) != 512:
        raise ValueError("Input must be 512-bit.")
    x = [x_[i:i + 32] for i in range(0, 512, 32)]
    y = [None] * 16
    q = quarterround(bitseq32(x[0], x[4], x[8], x[12]))
    y[0], y[4], y[8], y[12] = [q[i:i + 32] for i in range(0, 128, 32)]
    q = quarterround(bitseq32(x[5], x[9], x[13], x[1]))
    y[5], y[9], y[13], y[1] = [q[i:i + 32] for i in range(0, 128, 32)]
    q = quarterround(bitseq32(x[10], x[14], x[2], x[6]))
    y[10], y[14], y[2], y[6] = [q[i:i + 32] for i in range(0, 128, 32)]
    q = quarterround(bitseq32(x[15], x[3], x[7], x[11]))
    y[15], y[3], y[7], y[11] = [q[i:i + 32] for i in range(0, 128, 32)]
    return bitseq32(*y)


def doubleround(x: Bits) -> Bits:
    """Calculate the doubleround value of the input as specified in the paper.

    Returns a 512-bit value.
    Raises error if input is not 512-bit.
    """
    # argument checking is done by column- and rowround.
    return rowround(columnround(x))


def salsa20_hash(x_: Bits) -> Bits:
    """Calculate the salsa20 hash of the value.

    Returns a 64-byte sequence.
    Raises error if input is not 512-bit.
    """
    if len(x_) != 512:
        raise ValueError("Input must be 512-bit.")

    # view each 4-byte sequence as a word in little-endian form.
    x = pack("<16L", *[x_[i:i + 32].uint for i in range(0, 512, 32)])
    z = reduce(lambda a, _: doubleround(a), range(10), x)
    x_bitseq32 = [x[i:i + 32] for i in range(0, 512, 32)]
    z_bitseq32 = [z[i:i + 32] for i in range(0, 512, 32)]
    return sum([bitseq32(xi.uint + zi.uint & 0xFFFFFFFF) for xi, zi in zip(x_bitseq32, z_bitseq32)])


def expansion(k: Bits, n: Bits) -> Bits:
    """Expand the key and the nonce into a 64-byte sequence.

    Returns a 64-byte sequence.
    Raises error if key is not 256-bit or nonce is not 128-bit.
    """
    if len(n) != 128:
        raise ValueError("n must be 128-bit.")
    if len(k) != 128:
        if len(k) != 256:
            raise ValueError("k must be 128 or 256-bit.")
        k0, k1 = k[:128], k[128:]
        sigma = [bitseq8(101, 120, 112, 97), bitseq8(110, 100, 32, 51),
                 bitseq8(50, 45, 98, 121), bitseq8(116, 101, 32, 107)]
        return salsa20_hash(sigma[0] + k0 + sigma[1] + n + sigma[2] + k1 + sigma[3])
    elif len(k) == 128:
        tau = [bitseq8(101, 120, 112, 97), bitseq8(110, 100, 32, 49),
               bitseq8(54, 45, 98, 121), bitseq8(116, 101, 32, 107)]
        return salsa20_hash(tau[0] + k + tau[1] + n + tau[2] + k + tau[3])
    else:
        raise ValueError("k must be 128 or 256-bit.")


def xcrypt(k: Bits, text: Bits, *args: Any, **kwargs: Any) -> Bits:
    """En- or decrypt the message with the given key with Salsa20.

    En- and decryption use the same algorithm because the inverse of XOR is XOR thus this function is called 'xcrypt'.

    En-/Decryption is done by XOR'ing the plain-/ciphertext with the stream generated by the expansion function.
    The nonce for the expansion function is dependent on current time thus ensuring that the same nonce
    will never be used again with the same key.

    The nonce for the expansion function should never be reused with the same key!
    Else, this happens: https://crypto.stackexchange.com/a/108/80458
    """
    if 'iv' not in kwargs:
        raise TypeError("xcrypt needs initialization vector as keyword argument")
    # first 64 bits of the nonce is the unique message number / initialization vector
    iv = kwargs['iv']
    if len(iv) != 64:
        raise ValueError("IV must be 64-bit.")

    def create_nonce(cnt: int) -> Bits:
        # last 64 bits of the nonce are the counter in littleendian
        return iv + pack('<1Q', cnt)

    stream_blocks_needed = ceil(len(text) / 512)
    stream = sum([expansion(k, create_nonce(counter)) for counter in range(stream_blocks_needed)])
    return text ^ stream[:len(text)]


def encrypt(k: Bits, text: Bits) -> Bits:
    """Encrypt the message with the given key with Salsa20.

    Make initialization vector dependent of current time to make sure a message is never
    encrypted again with the same key and IV.
    Raises error if key is not 256-bit.
    """
    if len(k) != 256:
        raise ValueError("key must be 256-bit.")

    random.seed(time())
    iv = Word(random.randint(0, 2 ** 64), bit=64)
    c = xcrypt(k, text, iv=iv)
    return iv + c


def decrypt(k: Bits, text: Bits) -> Bits:
    """Decrypt the message with the given key with Salsa20, extracting the IV from the ciphertext.

    Raises error if key is not 256-bit or text is not 64-bit.
    """
    if len(k) != 256:
        raise ValueError("key must be 256-bit.")

    if len(text) <= 64:
        # text can not be smaller than or equal to 64 bits because the IV itself is already 64-bits long.
        raise ValueError("text must be larger than 64-bit.")
    iv, c = text[:64], text[64:]
    return xcrypt(k, c, iv=iv)


def salsa20() -> Optional[Bits]:
    """Execute Salsa20 cipher with arguments given on comand line.

    Gets arguments from docopt which parses sys.argv.
    See http://docopt.org/ if you are not familiar with docopt argument parsing.
    """
    args = docopt(__doc__)

    _encrypt, _decrypt = wrap_stream_cipher_functions(encrypt, decrypt, args)

    text = bitseq_from_str(args['PLAINTEXT'] or args['CIPHERTEXT'])
    r = int(args['-r'])
    k = bitseq_from_str(args['KEY'])
    if args['encrypt']:
        return _encrypt(k, text)
    elif args['decrypt']:
        return _decrypt(k, text)
    return None


if __name__ == "__main__":
    try:
        print(salsa20())
    except ValueError as e:
        print(e)
        exit(1)
