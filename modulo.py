#!/usr/bin/env python

import unittest

class TestModuloVsBitShift(unittest.TestCase):
  def test_modulo_and_bitshift_are_not_commutative(self):
    m = 256 # modulo
    b = 2   # bit shift
    a = 0
    self.assertEqual( (a % m) >> b, (a >> b) % m)
    a = 256
    # 256 % 256 = 0, 0 >> 2 = 0 vs. 256 >> 2 = 64, 64 % 256 = 64
    self.assertNotEqual( (a % m) >> b, (a >> b) % m)
    
if __name__ == "__main__":
  unittest.main()
