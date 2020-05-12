from unittest import mock


def sysv_patcher(*default_args, **default_kwargs):
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


default_encrypt_args = sysv_patcher('feal', 'encrypt', key='0x123456789ABCDEF0123456789ABCDEF', text='0x0')

default_decrypt_args = sysv_patcher('feal', 'decrypt', key='0x123456789ABCDEF0123456789ABCDEF',
                                    text='0x9C9B54973DF685F8')
