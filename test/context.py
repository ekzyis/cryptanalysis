"""Define import context for tests.

This file is used to insert the src directory into PYTHONPATH.
This way, the imports which are relative to the src directory in the src modules can be resolved when
importing them in test modules.
"""

import sys
import unittest
from pathlib import Path
from time import time

src_dir = Path(__file__).parent / '../src'
sys.path.insert(0, str(src_dir))

__SHOW_TEST_EXECUTION_TIME__ = False

if __SHOW_TEST_EXECUTION_TIME__:
    # monkey patch unittest.TestCase such that it shows execution time of all test methods
    @classmethod
    def setUpClass(cls):
        cls.startTime = time()


    @classmethod
    def tearDownClass(cls):
        print("\n%s: %.3fs" % (cls.__module__, time() - cls.startTime))


    unittest.TestCase.setUpClass = setUpClass
    unittest.TestCase.tearDownClass = tearDownClass
