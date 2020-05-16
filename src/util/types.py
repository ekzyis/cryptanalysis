"""Exports custom types used throughout the codebase."""

from typing import Protocol, Any, TypedDict, Callable


class CipherFunction(Protocol):
    # NOTE text should actually be hinted with Union[int,str]
    # NOTE return value should actually be hinted with Union[int,str]
    # But when hinting with Union[int, str] `mypy` also throws error when hinting a function with only int or str.
    # https://github.com/python/mypy/issues/7183
    def __call__(self, key: int, text: Any, *args: Any, **kwargs: Any) -> Any: ...


Formatter = Callable[[Any], Any]

CipherOptions = TypedDict('CipherOptions', {
    '-o': str,
    '--round-number': int,
    '-m': str,
    '-x': str,
    'blocksize': int,
})
