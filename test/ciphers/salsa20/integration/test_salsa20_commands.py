import unittest

# noinspection PyUnresolvedReferences
import test.context
from ciphers.stream.salsa20 import salsa20
from test.ciphers.salsa20.integration.patchers import default_decrypt_args, default_encrypt_args
from test.helper import timeit
from util.bitseq import bitseq, bitseq64, fhex


class TestSalsa20Commands(unittest.TestCase):

    @default_encrypt_args()
    @timeit
    def test_integration_salsa20_encrypt(self, _):
        c = bitseq64(
            0x0,
            0xe3be8fdd8beca2e3, 0xea8ef9475b29a6e7, 0x003951e1097a5c38, 0xd23b7a5fad9f6844,
            0xb22c97559e2723c7, 0xcbbd3fe4fc8d9a07, 0x44652a83e72a9c46, 0x1876af4d7ef1a117,
            0x8da2b74eef1b6283, 0xe7e20166abcae538, 0xe9716e4669e2816b, 0x6b20c5c356802001,
            0xcc1403a9a117d12a, 0x2669f456366d6ebb, 0x0f1246f1265150f7, 0x93cdb4b253e348ae,

            0x203d89bc025e802a, 0x7e0e00621d70aa36, 0xb7e07cb1e7d5b38d, 0x5e222b8b0e4b8407,
            0x0142b1e29504767d, 0x76824850320b5368, 0x129fdd74e861b498, 0xe3be8d16f2d7d169,
            0x57be81f47b17d9ae, 0x7c4ff15429a73e10, 0xacf250ed3a90a93c, 0x711308a74c6216a9,
            0xed84cd126da7f28e, 0x8abf8bb63517e1ca, 0x98e712f4fb2e1a6a, 0xed9fdc73291faa17,

            0x958211c4ba2ebd58, 0x38c635edb81f513a, 0x91a294e194f1c039, 0xaeec657dce40aa7e,
            0x7c0af57cacefa40c, 0x9f14b71a4b3456a6, 0x3e162ec7d8d10b8f, 0xfb1810d71001b618,
            0x2f9f73da53b85405, 0xc11f7b2d890fa8ae, 0x0c7f2e926d8a98c7, 0xec4e91b65120e988,
            0x349631a700c6face, 0xc3471cb0413656e7, 0x5e309456584084d7, 0xe12c5b43a41c43ed,

            0x9a048abd9b880da6, 0x5f6a665a20fe7b77, 0xcd292fe62cae644b, 0x7f7df69f32bdb331,
            0x903e6505ce44fdc2, 0x93920c6a9ec7057e, 0x23df7dad298f82dd, 0xf4efb7fdc7bfc622,
            0x696afcfd0cddcc83, 0xc7e77f11a649d79a, 0xcdc3354e9635ff13, 0x7e929933a0bd6f53,
            0x77efa105a3a4266b, 0x7c0d089d08f1e855, 0xcc32b15b93784a36, 0xe56a76cc64bc8477,
        )
        self.assertEqual(salsa20(), fhex(c))

    @default_decrypt_args()
    @timeit
    def test_integration_salsa20_decrypt(self):
        p = bitseq(0x0, bit=4096)
        self.assertEqual(salsa20(), fhex(p))
