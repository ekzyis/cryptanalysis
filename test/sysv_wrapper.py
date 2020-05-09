from unittest import mock


def patch_sysv_wrapper(*default_args, **default_kwargs):
    def additional_args_wrapper(*add_args, **add_kwargs):
        kwargs = dict(default_kwargs, **add_kwargs)
        args = list(default_args + add_args) + [kwargs['key'], kwargs['text']]

        def test_wrapper(fn):  # wraps the test function
            @mock.patch('sys.argv', args)
            def wrapper(*unittest_args):  # needed to pass the `self` argument from `unittest` to the test function
                return fn(*unittest_args)

            return wrapper

        return test_wrapper

    return additional_args_wrapper
