import sys
import unittest
from unittest.suite import TestSuite

# import _test
from _testCase import Verbosity
from _builder import SuiteBuilder
import _testCase
import tests



_testCase.VERBOSITY = Verbosity.silent



testSuite = TestSuite()

builder = SuiteBuilder(testSuite)
builder.addTests(package = tests, recursive = True)
 
runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=20)
runner.run(testSuite)