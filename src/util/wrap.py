from ciphers.modi.ecb import ecb
from util.encode import encode, decode


def get_wrapped_cipher_functions(encrypt, decrypt, args):
    """Returns the correctly wrapped encryption and decryption functions."""
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
    ecb_mode = args['-m'] == 'ecb'
    utf8_mode = args['-x'] == 'utf8'
    blocksize = args['blocksize']
    w_encrypt, w_decrypt = encrypt, decrypt
    if ecb_mode and utf8_mode:
        w_encrypt = encode(ecb(encrypt, blocksize))
        w_decrypt = ecb(decode(decrypt), blocksize)
    if ecb_mode and not utf8_mode:
        w_encrypt = ecb(encrypt, blocksize)
        w_decrypt = ecb(decrypt, blocksize)
    if not ecb_mode and utf8_mode:
        w_encrypt = encode(encrypt)
        w_decrypt = decode(decrypt)
    return w_encrypt, w_decrypt
