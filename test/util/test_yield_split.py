import unittest

# noinspection PyUnresolvedReferences
import test.context
from util.split import yield_split


class TestLimit(unittest.TestCase):

    def test_yield_split_returns_blocks_of_given_size_until_exhausted(self):
        m = 0xf1a3b7ae9281
        blocks = [b for b in yield_split(16, m)]
        self.assertEqual(blocks, [0xf1a3, 0xb7ae, 0x9281])

    def test_yield_split_returns_blocks_of_given_size_except_last_block(self):
        m = 0xf1a3b7ae9281
        blocks = [b for b in yield_split(32, m)]
        self.assertEqual(blocks, [0xf1a3b7ae, 0x9281])
