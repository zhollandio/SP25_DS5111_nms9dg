import sys
import os

def test_os():
    assert os.name == "posix", "Tests should only run on Linux"

def test_python_version():
    """Ensure Python version is 3.10 or newer."""
    assert sys.version_info >= (3, 10), "Python version must be 3.10 or newer"
