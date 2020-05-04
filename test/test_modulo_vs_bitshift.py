import unittest

# noinspection PyUnresolvedReferences
import test.context


class TestModuloVsBitShift(unittest.TestCase):
    def test_modulo_and_bit_shift_are_not_commutative(self):
        """
        This test case "proves" that the commutative law does not hold "%" and ">>"
        """
        m = 256  # modulo
        b = 2  # bit shift
        a = 0
        self.assertEqual((a % m) >> b, (a >> b) % m)
        a = 256
        # 256 % 256 = 0, 0 >> 2 = 0 vs. 256 >> 2 = 64, 64 % 256 = 64
        self.assertNotEqual((a % m) >> b, (a >> b) % m)

    def test_modulo_with_power_of_two_can_be_rewritten_with_bitwise_and(self):
        for n in range(10):
            for x in range(1024):
                e = 2 ** n
                self.assertEqual(x % e, x & (e - 1))


if __name__ == "__main__":
    unittest.main()
