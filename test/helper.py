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

        def _assert_fn_raises_with_mutated_argument_length_wrapper(arg_len_mutator):
            def _assert_fn_raises_with_mutated_argument_length(fn, correct_args, arg_index_to_check, error):
                length = len(correct_args[arg_index_to_check])
                with self.assertRaises(error):
                    x = bitseq(0x0, bit=arg_len_mutator(length))
                    args = correct_args.copy()
                    args[arg_index_to_check] = x
                    fn(*args)

            return _assert_fn_raises_with_mutated_argument_length

        _assert_fn_raises_if_argument_smaller_than_given_length = \
            _assert_fn_raises_with_mutated_argument_length_wrapper(lambda l: l - 1)

        _assert_fn_raises_if_argument_greater_than_given_length = \
            _assert_fn_raises_with_mutated_argument_length_wrapper(lambda l: l + 1)

        def _assert_fn_raises_if_argument_not_of_given_length(fn, correct_args, arg_index_to_check, error):
            _assert_fn_raises_if_argument_greater_than_given_length(fn, correct_args, arg_index_to_check, error)
            _assert_fn_raises_if_argument_smaller_than_given_length(fn, correct_args, arg_index_to_check, error)
            try:
                fn(*correct_args)
            except ValueError:
                self.fail("{} raised unexpected ValueError".format(fn.__name__))

        def _assert_fn_arguments_length_iterator_wrapper(assert_argument_length_fn):
            def _assert_fn_raises_if_assert_fn_called_on_arg_length(fn, correct_args, error, arg_index_to_check=None):
                if arg_index_to_check is None:
                    for i, arg in enumerate(correct_args):
                        assert_argument_length_fn(
                            fn=fn, correct_args=correct_args, arg_index_to_check=i, error=error
                        )
                else:
                    assert_argument_length_fn(
                        fn=fn, correct_args=correct_args, arg_index_to_check=arg_index_to_check, error=error
                    )

            return _assert_fn_raises_if_assert_fn_called_on_arg_length

        assert_fn_raises_if_arguments_not_of_given_lengths = _assert_fn_arguments_length_iterator_wrapper(
            _assert_fn_raises_if_argument_not_of_given_length
        )

        assert_fn_raises_if_arguments_smaller_than_given_lengths = _assert_fn_arguments_length_iterator_wrapper(
            _assert_fn_raises_if_argument_smaller_than_given_length
        )

        assert_fn_raises_if_arguments_greater_than_given_lengths = _assert_fn_arguments_length_iterator_wrapper(
            _assert_fn_raises_if_argument_greater_than_given_length
        )

        self.assertBit = assert_bit
        self.assert_fn_raises_if_arguments_not_of_given_lengths = assert_fn_raises_if_arguments_not_of_given_lengths
        self.assert_fn_raises_if_arguments_smaller_than_given_lengths = \
            assert_fn_raises_if_arguments_smaller_than_given_lengths
        self.assert_fn_raises_if_arguments_greater_than_given_lengths = \
            assert_fn_raises_if_arguments_greater_than_given_lengths

    def shortDescription(self):
        return self._testMethodDoc
