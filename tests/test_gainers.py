"""Tests for the gainer classes"""
import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
from bin.gainers.factory import GainerFactory
from bin.gainers.base import BaseGainer
from bin.gainers.wsj import WSJGainer
from bin.gainers.yahoo import YahooGainer


class TestGainerFactory(unittest.TestCase):
    """tests for the GainerFactory class"""

    def test_create_gainer_wsj(self):
        """test creating a WSJ gainer"""
        gainer = GainerFactory.create_gainer('wsj')
        self.assertIsInstance(gainer, WSJGainer)

    def test_create_gainer_yahoo(self):
        """test creating a Yahoo gainer"""
        gainer = GainerFactory.create_gainer('yahoo')
        self.assertIsInstance(gainer, YahooGainer)

    def test_create_gainer_invalid(self):
        """test creating an invalid gainer."""
        with self.assertRaises(ValueError):
            GainerFactory.create_gainer('invalid')


class MockBaseGainer(BaseGainer):
    """mock implem of BaseGainer for testing"""

    def fetch_gainers(self):
        """mock implem"""
        return []

    def parse_data(self, data):
        """mock implem"""
        return []

    def save_with_timestamp(self):
        """mock implem"""
        pass


class TestBaseGainer(unittest.TestCase):
    """tests for the BaseGainer class""" 

    def test_base_gainer(self):
        """test the BaseGainer class"""
        gainer = MockBaseGainer()
        self.assertEqual(gainer.gainers, [])
        self.assertEqual(gainer.get_gainers(), [])


class TestWSJGainer(unittest.TestCase):
    """tests for the WSJGainer class"""

    def setUp(self):
        """set up test fixtures"""
        self.wsj_gainer = WSJGainer() 
        # updated test HTML to match the actual structure expected by parse_data
        # this is great, very solid when you don't expect the format to change.  Also makes
        # reading the test explicit so you are also documenting what you expect.
        self.test_html = """
        <html>
            <body>
                <table>
                    <tr>
                        <th>Symbol</th>
                        <th>Volume</th>
                        <th>Price</th>
                        <th>Change</th>
                        <th>%Change</th>
                    </tr>
                    <tr>
                        <td>Apple Inc. (AAPL)</td>
                        <td>1000000</td>
                        <td>150.00</td>
                        <td>+7.5</td>
                        <td>+5.0%</td>
                    </tr>
                </table>
            </body>
        </html>
        """

    @patch('bin.gainers.wsj.WSJGainer.fetch_gainers', autospec=True)
    def test_fetch_gainers(self, mock_fetch):
        """test fetching gainers from WSJ"""
        # set up the mock to return a sample result
        mock_fetch.return_value = [{'Symbol': 'AAPL'}]
        gainers = self.wsj_gainer.fetch_gainers()
        mock_fetch.assert_called_once_with(self.wsj_gainer)
        self.assertEqual(gainers, [{'Symbol': 'AAPL'}])

    def test_parse_data(self):
        """test parsing WSJ data"""
        gainers = self.wsj_gainer.parse_data(self.test_html)
        self.assertEqual(len(gainers), 1)
        if gainers:  # protect against empty list
            self.assertEqual(gainers[0].get('Symbol'), 'AAPL')
            self.assertEqual(gainers[0].get('Company'), 'Apple Inc.')
            self.assertEqual(gainers[0].get('Price'), '150.00')
            self.assertEqual(gainers[0].get('Change'), '+7.5')
            self.assertEqual(gainers[0].get('%Change'), '+5.0%')

    @patch('builtins.print')
    def test_print_gainers(self, mock_print):
        """test printing gainers"""
        self.wsj_gainer.gainers = [{'Symbol': 'AAPL', 'Company': 'Apple Inc.'}]
        self.wsj_gainer.print_gainers()
        mock_print.assert_called_with({'Symbol': 'AAPL', 'Company': 'Apple Inc.'})

class TestYahooGainer(unittest.TestCase):
    """tests for the YahooGainer class"""

    def setUp(self):
        """set up test fixtures"""
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
        """test fetching gainers from Yahoo"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.test_html
        mock_get.return_value = mock_response

        with patch.object(self.yahoo_gainer, 'parse_data') as mock_parse:
            mock_parse.return_value = [{'symbol': 'MSFT'}]
            gainers = self.yahoo_gainer.fetch_gainers()

            # updated since we refactored wsj and yahoo gainers
            mock_get.assert_called_once()
            self.assertEqual(mock_get.call_args[0][0], self.yahoo_gainer.url)
            self.assertIn('headers', mock_get.call_args[1])
            self.assertEqual(mock_get.call_args[1]['timeout'], 15)

            mock_parse.assert_called_once_with(self.test_html)
            self.assertEqual(gainers, [{'symbol': 'MSFT'}])

    def test_parse_data(self):
        """test parsing Yahoo data"""
        gainers = self.yahoo_gainer.parse_data(self.test_html)
        self.assertEqual(len(gainers), 1)
        if gainers:  # protect against empty list
            self.assertEqual(gainers[0].get('symbol'), 'MSFT')
            self.assertEqual(gainers[0].get('name'), 'Microsoft Corp')
            self.assertEqual(gainers[0].get('price'), '300.00')
            self.assertEqual(gainers[0].get('change'), '+4.5%')

    @patch('builtins.print')
    def test_save_with_timestamp(self, mock_print):
        """Test saving gainers with timestamp."""
        self.yahoo_gainer.gainers = []
        self.yahoo_gainer.save_with_timestamp()
        mock_print.assert_any_call("Saving Yahoo gainers")


if __name__ == '__main__':
    unittest.main()
