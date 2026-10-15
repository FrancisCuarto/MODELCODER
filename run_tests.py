"""
Test runner script executed inside Blender:
    blender -b --python run_tests.py
"""

import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

loader = unittest.TestLoader()
suite = loader.discover(start_dir=os.path.join(current_dir, "tests"), pattern="test_*.py")

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

if not result.wasSuccessful():
    sys.exit(1)
