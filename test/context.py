"""Define import context for tests.

This file is used to insert the src directory into PYTHONPATH.
This way, the imports which are relative to the src directory in the src modules can be resolved when
importing them in test modules.
"""

import sys
from pathlib import Path

src_dir = Path(__file__).parent / '../src'
sys.path.insert(0, str(src_dir))
