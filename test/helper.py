"""Helper functions for testing.

(Didn't want to also call it util.py)
"""
import time
import unittest

# https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
import bitstring


def timeit(method):
    """Decorator to print execution time of method."""

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('\n%r  %2.2f ms\n' % (method.__name__, (te - ts) * 1000))
        return result

    return timed


class BitsTestCase(unittest.TestCase):
    """Custom test case class to reuse testing patterns."""

    def setUp(self):
        super(BitsTestCase, self).setUp()

        def assert_bit(b: bitstring.Bits, value: int, length: int):
            """Custom bit assertion function."""
            self.assertEqual(b.uint, value)
            self.assertEqual(len(b), length)

        self.assertBit = assert_bit
