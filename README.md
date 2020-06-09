# cryptanalysis

### Introduction

"In cryptography, linear cryptanalysis is a general form of cryptanalysis based on finding affine approximations to the action of a cipher. Attacks have been developed for block ciphers and stream ciphers. Linear cryptanalysis is one of the two most widely used attacks on block ciphers; the other being differential cryptanalysis."
- Wikipedia, https://en.wikipedia.org/wiki/Linear_cryptanalysis

~~For my bachelor thesis about Linear Cryptanalysis,~~ I have chosen to implement some ciphers such that I can experiment with them and gain in-depth knowledge about their inner workings.

As an additional benefit while implementing, I get a good basic understanding of block ciphers.
For example, I always wondered how one can encrypt messages larger than the block size (see [modes of operation](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)) or use padding to increase the message length for security purposes while still being able to obtain the real message afterwards.

Therefore, I have chosen to implement the following ciphers:
- FEAL-NX
- Salsa20

### General setup

1. Create virtual environment for python:

`python -m venv venv`

2. Activate virtual environment:

`source venv/bin/activate`

3. Install dependencies:

`pip install -r requirements.txt`

4. Run tests (optional):

`python -m unittest`

### FEAL-NX

Reference paper for specification: https://info.isl.ntt.co.jp/crypt/archive/dl/feal/call-3e.pdf

This cipher was chosen since it "has acted as a catalyst in the discovery of differential and linear cryptanalysis" according to Wikipedia (https://en.wikipedia.org/wiki/FEAL).

Therefore, I hope I can use this cipher to gain more in-depth knowledge about linear cryptanalysis by attacking the cipher and playing around with the implementation.

`src/ciphers/block/feal.py`:
```
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
```

### Salsa20

Reference paper for specification: https://cr.yp.to/snuffle/spec.pdf

`src/ciphers/stream/salsa20.py`
```
Usage:
    salsa20 encrypt [options] KEY PLAINTEXT
    salsa20 decrypt [options] KEY CIPHERTEXT

    -r=[8,12,20]            Number of rounds. [default: 20]
    -x=[utf8,none]          Specifies the encoding of the cipher-/plaintext. [default: none]

    KEY                     The key which should be used for en-/decryption.
    PLAINTEXT               The text to encrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
    CIPHERTEXT              The text to decrypt. Must be a number. Can be a code literal such as 0b1011, 0o71, 0xF32C.
```
