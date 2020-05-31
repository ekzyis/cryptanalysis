import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.types import Text


class TestText(unittest.TestCase):
    def test_type_text_bit_is_set_to_number_of_bits(self):
        t = Text(0x0, 0x0, bit=64)
        self.assertEqual(t.bit, 128)

    def test_type_text_blocks_attribute_from_word_is_deleted(self):
        t = Text(0x0, bit=16)
        with self.assertRaises(AttributeError):
            t.blocks
