import unittest
from unittest import mock
from unittest.mock import call

from ciphers.modi.ecb import ecb
from util.encode import encode, encode_wrapper


class TestOptionsWrapping(unittest.TestCase):
    def test_ecb_with_encode_wrapper(self):
        encrypt = mock.Mock(wraps=lambda _k, _m: _m)
        ecb_wrap = mock.Mock(wraps=ecb(encrypt, 8))
        k, m = 0xffff, "test"
        o = encode_wrapper(ecb_wrap)(k, m)
        ecb_wrap.assert_called_once_with(k, encode(m))
        # encode(test) == 0x74657374
        #   ecb should split this up into four 8-bit strings:
        #   0x74, 0x65, 0x73, 0x74
        self.assertEqual(encrypt.call_count, 4)
        encrypt.assert_has_calls([call(k, 0x74), call(k, 0x65), call(k, 0x73), call(k, 0x74)])
        self.assertEqual(o, 0x74657374)
