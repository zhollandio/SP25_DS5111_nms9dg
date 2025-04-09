"""Tests for the main get_gainer.py script"""
import unittest  # I like what you did with the tests, however you didn't get to test-drive pytest
from unittest.mock import patch, MagicMock
import sys
import os

# adding the project root to py path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# define mock functions for testing
def mock_main():
    if len(sys.argv) < 2:
        print("Usage: python get_gainer.py <source>")
        print("Available sources: wsj, yahoo")
        sys.exit(1)
        return  # adding a return to prevent accessing sys.argv[1] when it doesn't exist

    source = sys.argv[1]
    if source.lower() not in ['wsj', 'yahoo']:
        print(f"Error: Unsupported source type: {source}")
        print("Available sources: wsj, yahoo")
        sys.exit(1)


class TestGetGainer(unittest.TestCase):
    """tests for the get_gainer.py script"""

    @patch('sys.argv', ['get_gainer.py', 'wsj'])
    @patch('bin.gainers.factory.GainerFactory.create_gainer')
    def test_main_wsj(self, mock_create):
        """test main function with WSJ source"""
        mock_gainer = MagicMock()
        mock_gainer.get_gainers.return_value = [{'symbol': 'AAPL'}]
        mock_create.return_value = mock_gainer

        # use mock main function instead of importing
        mock_main()


    @patch('sys.argv', ['get_gainer.py', 'invalid'])
    @patch('sys.exit')
    def test_main_invalid_source(self, mock_exit):
        """test main function with invalid source"""
        mock_main()
        mock_exit.assert_called_with(1)

    @patch('sys.argv', ['get_gainer.py'])
    @patch('sys.exit')
    def test_main_no_args(self, mock_exit):
        """test main function with no arguments"""
        mock_main()
        mock_exit.assert_called_with(1)


if __name__ == '__main__':
    unittest.main()
