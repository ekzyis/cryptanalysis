"""Exports custom types used throughout the codebase."""

from typing import Protocol, Any, TypedDict, Callable

from util.word import Word


class CipherFunction(Protocol):
    """Class for type hinting cipher functions (functions with signature as __call__)."""

    # NOTE text should actually be hinted with Union[int,str]
    # NOTE return value should actually be hinted with Union[int,str]
    # But when hinting with Union[int, str] `mypy` also throws error when hinting a function with only int or str.
    # https://github.com/python/mypy/issues/7183
    def __call__(self, key: int, text: Any, *args: Any, **kwargs: Any) -> Any:
        """Cipher functions should have as first argument a key as int, and second the text to en- or decrypt."""
        pass


Formatter = Callable[[Any], Any]

CipherOptions = TypedDict('CipherOptions', {
    '-o': str,
    '--round-number': int,
    '-m': str,
    '-x': str,
    'blocksize': int,
})


class Text(Word):
    def __init__(self, *args: Any, bit: int = 32) -> None:
        super().__init__(*args, bit=bit)
        self.bit = len(self.blocks) * bit
        delattr(self, 'blocks')
