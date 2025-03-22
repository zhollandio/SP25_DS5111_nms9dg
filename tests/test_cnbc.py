"""Tests for the CNBC gainer class."""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bin.gainers.factory import GainerFactory
from bin.gainers.cnbc import CNBCGainer

class TestCNBCGainer(unittest.TestCase):
    """Tests for the CNBCGainer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.cnbc_gainer = CNBCGainer()
        self.test_html = """
        <html>
            <body>
                <div class="MarketMoversTable-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Symbol</th>
                                <th>Company</th>
                                <th>Price</th>
                                <th>Change</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>NVDA</td>
                                <td>NVIDIA Corporation</td>
                                <td>950.00</td>
                                <td>+3.5%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>
        </html>
        """

    def test_create_cnbc_gainer(self):
        """Test creating a CNBC gainer."""
        gainer = GainerFactory.create_gainer('cnbc')
        self.assertIsInstance(gainer, CNBCGainer)

    @patch('requests.get')
    def test_fetch_gainers(self, mock_get):
        """Test fetching gainers from CNBC."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.test_html
        mock_get.return_value = mock_response

        gainers = self.cnbc_gainer.fetch_gainers()

        # Check that get was called with the correct URL and timeout
        # We don't verify the exact headers since they might change
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], self.cnbc_gainer.url)
        self.assertEqual(kwargs['timeout'], 10)
        self.assertIn('headers', kwargs)

    @patch('builtins.print')
    def test_save_with_timestamp(self, mock_print):
        """Test saving CNBC gainers with timestamp."""
        self.cnbc_gainer.save_with_timestamp()
        mock_print.assert_any_call("Saving CNBC gainers")


if __name__ == '__main__':
    unittest.main()
