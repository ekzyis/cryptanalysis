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
        encode_wrapper(ecb_wrap)(k, m)
        ecb_wrap.assert_called_once_with(k, encode(m))
        encrypt.assert_has_calls([call(k, b) for b in ecb_wrap(k, encode(m))])
