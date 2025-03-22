"""Tests for the gainer classes."""
import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
from bin.gainers.factory import GainerFactory
from bin.gainers.base import BaseGainer
from bin.gainers.wsj import WSJGainer
from bin.gainers.yahoo import YahooGainer


class TestGainerFactory(unittest.TestCase):
    """Tests for the GainerFactory class."""

    def test_create_gainer_wsj(self):
        """Test creating a WSJ gainer."""
        gainer = GainerFactory.create_gainer('wsj')
        self.assertIsInstance(gainer, WSJGainer)

    def test_create_gainer_yahoo(self):
        """Test creating a Yahoo gainer."""
        gainer = GainerFactory.create_gainer('yahoo')
        self.assertIsInstance(gainer, YahooGainer)

    def test_create_gainer_invalid(self):
        """Test creating an invalid gainer."""
        with self.assertRaises(ValueError):
            GainerFactory.create_gainer('invalid')


class MockBaseGainer(BaseGainer):
    """Mock implementation of BaseGainer for testing."""

    def fetch_gainers(self):
        """Mock implementation."""
        return []

    def parse_data(self, data):
        """Mock implementation."""
        return []

    def save_with_timestamp(self):
        """Mock implementation."""
        pass


class TestBaseGainer(unittest.TestCase):
    """Tests for the BaseGainer class."""

    def test_base_gainer(self):
        """Test the BaseGainer class."""
        gainer = MockBaseGainer()
        self.assertEqual(gainer.gainers, [])
        self.assertEqual(gainer.get_gainers(), [])


class TestWSJGainer(unittest.TestCase):
    """Tests for the WSJGainer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.wsj_gainer = WSJGainer()
        self.test_html = """
        <html>
            <body>
                <table class="WSJTables--table">
                    <tr>
                        <th>Symbol</th>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Change</th>
                    </tr>
                    <tr>
                        <td>AAPL</td>
                        <td>Apple Inc.</td>
                        <td>150.00</td>
                        <td>+5.0%</td>
                    </tr>
                </table>
            </body>
        </html>
        """

    @patch('requests.get')
    def test_fetch_gainers(self, mock_get):
        """Test fetching gainers from WSJ."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.test_html
        mock_get.return_value = mock_response

        with patch.object(self.wsj_gainer, 'parse_data') as mock_parse:
            mock_parse.return_value = [{'symbol': 'AAPL'}]
            gainers = self.wsj_gainer.fetch_gainers()

            mock_get.assert_called_once_with(self.wsj_gainer.url, timeout=10)
            mock_parse.assert_called_once_with(self.test_html)
            self.assertEqual(gainers, [{'symbol': 'AAPL'}])

    def test_parse_data(self):
        """Test parsing WSJ data."""
        # This test will depend on your actual implementation
        # Adjust the expected output based on your parse_data implementation
        gainers = self.wsj_gainer.parse_data(self.test_html)

        # Assuming your parse_data correctly extracts the data from the test HTML
        self.assertEqual(len(gainers), 1)
        if gainers:  # Protect against empty list
            self.assertEqual(gainers[0].get('symbol'), 'AAPL')
            self.assertEqual(gainers[0].get('name'), 'Apple Inc.')
            self.assertEqual(gainers[0].get('price'), '150.00')
            self.assertEqual(gainers[0].get('change'), '+5.0%')

    @patch('builtins.print')
    def test_print_gainers(self, mock_print):
        """Test printing gainers."""
        self.wsj_gainer.gainers = [{'symbol': 'AAPL', 'name': 'Apple Inc.'}]
        self.wsj_gainer.print_gainers()
        mock_print.assert_called_with({'symbol': 'AAPL', 'name': 'Apple Inc.'})


class TestYahooGainer(unittest.TestCase):
    """Tests for the YahooGainer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.yahoo_gainer = YahooGainer()
        self.test_html = """
        <html>
            <body>
                <table data-test="gainers-table">
                    <tbody>
                        <tr>
                            <td>MSFT</td>
                            <td>Microsoft Corp</td>
                            <td>300.00</td>
                            <td>+4.5%</td>
                            <td>Other</td>
                        </tr>
                    </tbody>
                </table>
            </body>
        </html>
        """

    @patch('requests.get')
    def test_fetch_gainers(self, mock_get):
        """Test fetching gainers from Yahoo."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.test_html
        mock_get.return_value = mock_response

        with patch.object(self.yahoo_gainer, 'parse_data') as mock_parse:
            mock_parse.return_value = [{'symbol': 'MSFT'}]
            gainers = self.yahoo_gainer.fetch_gainers()

            mock_get.assert_called_once_with(self.yahoo_gainer.url, timeout=10)
            mock_parse.assert_called_once_with(self.test_html)
            self.assertEqual(gainers, [{'symbol': 'MSFT'}])

    def test_parse_data(self):
        """Test parsing Yahoo data."""
        # This test will depend on your actual implementation
        # Adjust the expected output based on your parse_data implementation
        gainers = self.yahoo_gainer.parse_data(self.test_html)

        # Assuming your parse_data correctly extracts the data from the test HTML
        self.assertEqual(len(gainers), 1)
        if gainers:  # Protect against empty list
            self.assertEqual(gainers[0].get('symbol'), 'MSFT')
            self.assertEqual(gainers[0].get('name'), 'Microsoft Corp')
            self.assertEqual(gainers[0].get('price'), '300.00')
            self.assertEqual(gainers[0].get('change'), '+4.5%')

    @patch('builtins.print')
    def test_save_with_timestamp(self, mock_print):
        """Test saving gainers with timestamp."""
        self.yahoo_gainer.save_with_timestamp()
        mock_print.assert_called_with("Saving Yahoo gainers")


if __name__ == '__main__':
    unittest.main()
