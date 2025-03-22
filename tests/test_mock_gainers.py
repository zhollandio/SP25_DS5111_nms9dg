"""Tests for the Mock gainer class."""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bin.gainers.factory import GainerFactory
from bin.gainers.mock import MockGainer

class TestMockGainer(unittest.TestCase):
    """Tests for the MockGainer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_gainer = MockGainer()

    def test_create_mock_gainer(self):
        """Test creating a mock gainer."""
        gainer = GainerFactory.create_gainer('mock')
        self.assertIsInstance(gainer, MockGainer)

    def test_fetch_gainers(self):
        """Test fetching gainers from mock source."""
        gainers = self.mock_gainer.fetch_gainers()
        self.assertEqual(len(gainers), 5)
        self.assertEqual(gainers[0]['symbol'], 'AAPL')
        self.assertEqual(gainers[1]['symbol'], 'MSFT')

    @patch('builtins.print')
    def test_save_with_timestamp(self, mock_print):
        """Test saving mock gainers with timestamp."""
        self.mock_gainer.save_with_timestamp()
        mock_print.assert_any_call("Saving Mock gainers")


if __name__ == '__main__':
    unittest.main()
