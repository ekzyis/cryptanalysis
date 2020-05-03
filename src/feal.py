#!/usr/bin/env python

import unittest

def s0(a,b):
  return (a + b % 256) >> 2

class TestS0(unittest.TestCase):
  def test_case_1(self):
    a = 0b10101010
    b = 0b01010101
    s = s0(a,b)
    self.assertEqual(0b111111, s)
    self.assertEqual(63, s)

if __name__ == "__main__":
  unittest.main()
