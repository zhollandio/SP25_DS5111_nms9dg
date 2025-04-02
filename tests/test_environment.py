import sys
import os

def test_os():
    assert os.name == "posix", "Tests should only run on Linux"

def test_python_version(): # just a head's up that you'll need to change the test when you update the validation.yaml
    """Ensure Python version is 3.10 or newer."""
    assert sys.version_info >= (3, 10), "Python version must be 3.10 or newer"
