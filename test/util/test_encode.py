import unittest
from unittest import mock

from util.encode import encode, decode, encode_wrapper, decode_wrapper


class TestEncode(unittest.TestCase):
    def test_encode_decode_round_trip(self):
        test = "test"
        self.assertEqual(decode(encode(test)), test)

    def test_encode_decode_round_trip_with_whitespace(self):
        test = "this is a test"
        self.assertEqual(decode(encode(test)), test)

    def test_encode_decode_round_trip_with_punctuation(self):
        test = 'he said: "hello! is this a test?". From the other room, the answer was heard: "yes, indeed."'
        self.assertEqual(decode(encode(test)), test)

    def test_encode_decode_round_trip_with_special_characters(self):
        test = '!"§$%&/()=?`²³{[]}\\´öäü+*~#\'<>|^°,;.:-_@ł€¶ŧ←↓→øþ¨æſðđŋħ̣̣ĸł˝»«¢„“”µ·…–'
        self.assertEqual(decode(encode(test)), test)

    def test_encode_wrapper(self):
        cipher_fn = mock.Mock()
        k, m = 0xffff, "test"
        encode_wrapper(cipher_fn)(k, m)
        cipher_fn.assert_called_once_with(k, encode(m))

    def test_decode_wrapper(self):
        cipher_fn = mock.Mock(wraps=lambda k, m: m)
        k, m = 0xffff, 0x1234
        o = decode_wrapper(cipher_fn)(k, m)
        cipher_fn.assert_called_once_with(k, m)
        self.assertEqual(o, decode(m))
