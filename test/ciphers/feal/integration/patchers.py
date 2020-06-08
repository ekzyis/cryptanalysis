"""Decorators used for FEAL integration tests."""

from test.ciphers.sysv_patcher import sysv_patcher

default_encrypt_args = sysv_patcher('feal', 'encrypt', key='0x0123456789ABCDEF0123456789ABCDEF',
                                    text='0x0000000000000000')

default_decrypt_args = sysv_patcher('feal', 'decrypt', key='0x0123456789ABCDEF0123456789ABCDEF',
                                    text='0x9C9B54973DF685F8')
