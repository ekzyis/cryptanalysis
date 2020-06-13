#!/usr/bin/env python

"""FEAL-NX Implementation.

Specification:
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf

Test vectors:
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf

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
    -o=[bin,hex,dec]        Specifies the output format. [default: hex]
    -m=[ecb,none]           Specifies the mode of operation [default: none]
    -x=[utf8,none]          Specifies the encoding of the cipher-/plaintext. [default: none]

    KEY                     The key which should be used for en-/decryption.
    PLAINTEXT               The text to encrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
    CIPHERTEXT              The text to decrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
"""

import sys
from pathlib import Path
from typing import Sequence, Tuple, Any, Union, Dict, Mapping, Optional

from bitstring import Bits
from docopt import docopt  # type: ignore

# make sure that following imports can be resolved when executing this script from cmdline
sys.path.insert(0, str(Path(__file__).parent / '../..'))

from ciphers.modi.ecb import ecb
from util.bitseq import bitseq32, bitseq8, bitseq64, bitseq_split
from util.encode import decode_wrapper, encode_wrapper
from util.wrap import key_input_to_bitseq_wrapper, text_input_to_bitseq_wrapper, output_wrapper, \
    text_input_padder, key_input_padder
from util.rot import rot_left_bits
from util.types import CipherFunction, Formatter


def key_schedule(key: Bits, n: int = 32) -> Sequence[Bits]:
    """Return the subkeys created by the key scheduler of FEAL-NX.

    Creates the N+8 16-bit subkeys which are needed during en-/decryption.
    Raises error if key is not 128-bit.
    """
    if len(key) != 128:
        raise ValueError("Key for FEAL-NX key scheduler must be 128-bit")
    kl, kr = bitseq_split(64, key)
    # processing of right key kr
    kr1, kr2 = bitseq_split(32, kr)
    # insert "filler" element such that the the first added element is at index 1
    #   since in the specification, indices for q start with 1
    q = [bitseq32(0x0)]
    for r in range(1, (int(n / 2) + 5)):
        if r % 3 == 1:
            q.append(kr1 ^ kr2)
        elif r % 3 == 2:
            q.append(kr1)
        elif r % 3 == 0:
            q.append(kr2)
    # processing of left key kl
    a0, b0 = bitseq_split(32, kl)
    a = [a0]
    b = [b0]
    d = [bitseq32(0x0)]
    k = []
    for r in range(1, int(n / 2) + 5):
        d.append(a[r - 1])
        a.append(b[r - 1])
        b.append(fk(a[r - 1], b[r - 1] ^ d[r - 1] ^ q[r]))
        br = b[r]
        br0, br1, br2, br3 = bitseq_split(8, br)
        k.append(br0 + br1)
        k.append(br2 + br3)
    return k


def s0(a: Bits, b: Bits) -> Bits:
    """Return substitution value of S-Box 0."""
    return _s(a, b, 0)


def s1(a: Bits, b: Bits) -> Bits:
    """Return substitution value of S-Box 1."""
    return _s(a, b, 1)


def _s(a: Bits, b: Bits, i: int) -> Bits:
    """General substitution box implementation for FEAL-NX."""
    return rot_left_bits(bitseq8((a.uint + b.uint + i) & 0xFF), 2)


def f(a: Bits, b: Bits) -> Bits:
    """f-function of FEAL-NX.

    a must be 32-bit and b must be 16-bit long.
    Used during en-/decryption.
    See section 5.1 and figure 3 in
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
    """
    if len(a) != 32:
        raise ValueError("a key must be 32-bit")
    if len(b) != 16:
        raise ValueError("b key must be 16-bit")
    a_k = bitseq_split(8, a)
    b_k = bitseq_split(8, b)
    f1 = a_k[1] ^ b_k[0]
    f2 = a_k[2] ^ b_k[1]
    f1 ^= a_k[0]
    f2 ^= a_k[3]
    f1 = s1(f1, f2)
    f2 = s0(f2, f1)
    f0 = s0(a_k[0], f1)
    f3 = s1(a_k[3], f2)
    return sum([f0, f1, f2, f3])


def fk(a: Bits, b: Bits) -> Bits:
    """f_k-function of FEAL-NX.

    Input keys must be 32-bit.
    Used during key schedule to generate the subkeys for each iteration.
    See section 5.2 and figure 4 in
    https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf
    """
    if len(a) != 32 or len(b) != 32:
        raise ValueError("Input keys must be 32-bit")
    a_k = bitseq_split(8, a)
    b_k = bitseq_split(8, b)
    fk1 = a_k[1] ^ a_k[0]
    fk2 = a_k[2] ^ a_k[3]
    fk1 = s1(fk1, fk2 ^ b_k[0])
    fk2 = s0(fk2, fk1 ^ b_k[1])
    fk0 = s0(a_k[0], fk1 ^ b_k[2])
    fk3 = s1(a_k[3], fk2 ^ b_k[3])
    return sum([fk0, fk1, fk2, fk3])


def _encrypt_preprocessing(subkeys: Sequence[Bits], text: Bits) -> Bits:
    p = text ^ sum(subkeys)
    l0 = p[:32]
    p ^= bitseq64(l0)
    return p


def _decrypt_preprocessing(subkeys: Sequence[Bits], text: Bits) -> Bits:
    p = text ^ sum(subkeys)
    rn = p[:32]
    p ^= bitseq64(rn)
    return p


def _encrypt_iterative_calculation(l0: Bits, r0: Bits, sk: Sequence[Bits], n: int = 32) \
        -> Tuple[Sequence[Bits], Sequence[Bits]]:
    l, r = [l0], [r0]
    for i in range(1, n + 1):
        r.append(l[i - 1] ^ f(r[i - 1], sk[i - 1]))
        l.append(r[i - 1])
    return l, r


def _decrypt_iterative_calculation(ln: Bits, rn: Bits, sk: Sequence[Bits], n: int = 32) \
        -> Tuple[Sequence[Bits], Sequence[Bits]]:
    l, r = [0] * n + [ln], [0] * n + [rn]
    for i in reversed(range(1, n + 1)):
        l[i - 1] = r[i] ^ f(l[i], sk[i - 1])
        r[i - 1] = l[i]
    return l, r


def encrypt(key: Bits, text: Bits, *args: Any, **kwargs: Any) -> Bits:
    """Encrypt the text with the given key using FEAL-NX encryption.

    Raises error if text is longer than 64-bit or key is longer than 128-bit.
    Raises error if text or key is not a number.
    """
    n = kwargs.setdefault('n', 32)
    if len(text) != 64:
        raise ValueError("Plaintext must be 64-bit")
    if len(key) != 128:
        raise ValueError("Key must be 128-bit")
    sk = key_schedule(key, n)
    preproc = _encrypt_preprocessing(sk[n:n + 4], text)
    l0, r0 = bitseq_split(32, preproc)
    l, r = _encrypt_iterative_calculation(l0, r0, sk, n)
    ln, rn = l[n], r[n]
    c = (rn + ln) ^ bitseq64(rn)
    c ^= sum([sk[n + 4], sk[n + 5], sk[n + 6], sk[n + 7]])
    return c


def decrypt(key: Bits, text: Bits, *args: Any, **kwargs: Any) -> Bits:
    """Decrypt the ciphertext with the given key using FEAL-NX decryption.

    Raises error if text is longer than 64-bit or key is longer than 128-bit.
    Raises error if text or key is not a number.
    """
    n = kwargs.setdefault('n', 32)
    if len(text) != 64:
        raise ValueError("Ciphertext must be 64-bit")
    if len(key) != 128:
        raise ValueError("Key must be 128-bit")
    sk = key_schedule(key, n)
    preproc = _decrypt_preprocessing(sk[n + 4:n + 8], text)
    rn, ln = bitseq_split(32, preproc)
    l, r = _decrypt_iterative_calculation(ln, rn, sk, n)
    l0, r0 = l[0], r[0]
    p = (l0 + r0) ^ bitseq64(l0)
    p ^= sum([sk[n], sk[n + 1], sk[n + 2], sk[n + 3]])
    return p


def _feal_options_wrap(args: Dict[str, Union[str, int]]) -> CipherFunction:
    """Wrap encrypt and decrypt cipher function with options wrapper to implement option-specific behaviour.

    Returns wrapped encrypt when encrypting; wrapped decrypt when decrypting.
    """
    """When parsing arguments, the following execution order has to be ensured:
        ===========================================================================
        `feal -x utf8 -m ecb encrypt k m`
         |
         | (k: int, m: str)
         |
         -> [ENCODE]: ENCODE MESSAGE
                |
                | (k: int, encoded_m: int)
                |
                -> [ECB]: SPLIT MESSAGE
                     |
                     | (k: int, m_blocks: [int])
                     |
                     -------------------------------
                     |        |    ...    |        |
                     |        |           |        | (k: int, m_block: int)
                     v        v           v        v
                 [ENCRYPT][ENCRYPT]   [ENCRYPT][ENCRYPT]
                     |        |           |        |
                     |        |           |        | (k: int, encrypted_m_block: int)
                     v        v           v        v
                     -------------------------------
                                    |
                                    | (encrypted_m_blocks: [int])
                                    v
                            [ECB]: CONCAT ENCRYPTED BLOCKS
                                    |
         ----------------------------
         |
         | (encrypted_message: int)
         v
         OUTPUT
        ===========================================================================
         `feal -x utf8 -m ecb ecb decrypt k m`
         |
         | (k: int, m: int)
         |
         --------> [ECB]: SPLIT MESSAGE
                     |
                     | (k: int, m_blocks: [int]
                     |
                     -------------------------------
                     |        |    ...    |        |
                     |        |           |        | (k: int, m_block: int)
                     v        v           v        v
                 [DECRYPT][DECRYPT]   [DECRYPT][DECRYPT]
                     |         |           |       |
                     |         |           |       |
                     v         v           v       v
                     -------------------------------
                               |
                               | (decrypted_m_blocks: [int]
                               v
                       [ECB]: CONCAT DECRYPTED BLOCKS
                               |
            --------------------
            |
            | (decrypted_message: int)
         [DECODE]
            |
         ----
         |
         v
         OUTPUT
        ===========================================================================
    """

    n = int(args['--round-number'])
    if n % 2 == 1:
        raise ValueError("Round number must be even.")
    ecb_mode: bool = args['-m'] == 'ecb'
    utf8_mode: bool = args['-x'] == 'utf8'
    blocksize: int = args['blocksize']

    _format: Mapping[str, Formatter] = {
        'bin': lambda b: '0b' + b.bin, 'dec': lambda b: str(b.uint), 'hex': lambda b: '0x' + b.hex
    }
    # This should not be able to cause an KeyError because docopt already checked that all enum arguments are valid
    formatter = _format[args['-o']]
    output_format_wrapper = output_wrapper(formatter)

    feal_key_input_padder = key_input_padder(128)
    feal_text_input_padder = text_input_padder(64)
    _encrypt, _decrypt = feal_key_input_padder(encrypt), feal_key_input_padder(decrypt)
    _encrypt, _decrypt = feal_text_input_padder(_encrypt), feal_text_input_padder(_decrypt)

    _encrypt, _decrypt = key_input_to_bitseq_wrapper(_encrypt), key_input_to_bitseq_wrapper(_decrypt)

    if args['encrypt']:
        if ecb_mode:
            _encrypt = ecb(_encrypt, blocksize)
        if utf8_mode:
            _encrypt = text_input_padder(blocksize)(_encrypt)
            _encrypt = encode_wrapper(_encrypt)
        else:
            _encrypt = text_input_to_bitseq_wrapper(_encrypt)
        _encrypt = output_format_wrapper(_encrypt)
        return _encrypt
    elif args['decrypt']:
        if ecb_mode:
            _decrypt = ecb(_decrypt, blocksize)
        _decrypt = text_input_to_bitseq_wrapper(_decrypt)
        if utf8_mode:
            _decrypt = decode_wrapper(_decrypt)
        else:
            _decrypt = output_format_wrapper(_decrypt)
        return _decrypt
    else:
        raise ValueError("args must be a dict with key 'encrypt' or 'decrypt' set.")


def validate(args):
    """Validates the arguments passed on the command line."""
    if int(args['--round-number']) % 2 != 0:
        raise ValueError("round number must be even.")
    if args['-o'] not in ['bin', 'hex', 'dec']:
        raise ValueError("output format must be bin, hex or dec")
    if args['-m'] not in ['ecb', 'none']:
        raise ValueError("mode of operation must be ecb or none")
    if args['-x'] not in ['utf8', 'none']:
        raise ValueError("encoding must be utf8 or none")


def feal() -> Optional[str]:
    """Execute FEAL-NX cipher with arguments given on command line.

    Gets arguments from docopt which parses sys.argv.
    See http://docopt.org/ if you are not familiar with docopt argument parsing.
    """
    args = docopt(__doc__)
    validate(args)

    # Wrap encrypt and decrypt functions depending on arguments given on cmdline
    args['blocksize'] = 64
    text = args['PLAINTEXT'] or args['CIPHERTEXT']
    n = int(args['--round-number'])
    k = args['KEY']
    cfn = _feal_options_wrap(args)
    return cfn(k, text, n=n)


if __name__ == "__main__":
    try:
        print(feal())
    except ValueError as e:
        print(e)
        exit(1)
