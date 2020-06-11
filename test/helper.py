"""Helper functions for testing.

(Didn't want to also call it util.py)
"""
import time
import unittest

# https://medium.com/pythonhive/python-decorator-to-measure-the-execution-time-of-methods-fa04cb6bb36d
import bitstring

from util.bitseq import bitseq


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

        def assert_fn_raises_if_argument_not_of_given_length(fn, correct_args, arg_index_to_check, length, error):
            with self.assertRaises(error):
                x = bitseq(0x0, bit=length + 1)
                args = correct_args.copy()
                args[arg_index_to_check] = x
                fn(*args)
            with self.assertRaises(error):
                x = bitseq(0x0, bit=length - 1)
                args = correct_args.copy()
                args[arg_index_to_check] = x
                fn(*args)
            try:
                fn(*correct_args)
            except ValueError:
                self.fail("{} raised unexpected ValueError".format(fn.__name__))

        def assert_fn_raises_if_arguments_not_of_given_lengths(fn, correct_args, error):
            for i, arg in enumerate(correct_args):
                assert_fn_raises_if_argument_not_of_given_length(
                    fn=fn, correct_args=correct_args, arg_index_to_check=i, length=len(arg), error=error
                )

        self.assertBit = assert_bit
        self.assert_fn_raises_if_argument_not_of_given_length = assert_fn_raises_if_argument_not_of_given_length
        self.assert_fn_raises_if_arguments_not_of_given_lengths = assert_fn_raises_if_arguments_not_of_given_lengths
