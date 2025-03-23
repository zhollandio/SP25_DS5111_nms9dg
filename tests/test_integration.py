import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from io import StringIO

# adding the project root to py path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bin.gainers.factory import GainerFactory


class TestGainerIntegration(unittest.TestCase):
    """integration tests for the gainer system"""

    @patch('sys.stdout', new_callable=StringIO)
    def test_wsj_process_flow(self, mock_stdout):
        """test the complete WSJ process flow"""
        # WSJ gainer with a mock fetch_gainers method
        gainer = GainerFactory.create_gainer('wsj')

        # replace the fetch_gainers method with a mock that prints the message and returns test data
        original_fetch = gainer.fetch_gainers

        def mock_fetch():
            print("Downloading WSJ gainers")
            gainer.gainers = [{'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': '150.00', 'change': '+5.0%'}]
            return gainer.gainers

        gainer.fetch_gainers = mock_fetch

        gainer.process()

        # restore original
        gainer.fetch_gainers = original_fetch

        # check that output contains expected strings
        output = mock_stdout.getvalue()
        self.assertIn("Downloading WSJ gainers", output)
        self.assertIn("Saving WSJ gainers", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_yahoo_process_flow(self, mock_stdout):
        """test the complete Yahoo process flow"""
        # Yahoo gainer with a mock fetch_gainers method
        gainer = GainerFactory.create_gainer('yahoo')

        # replace the fetch_gainers method with a mock that prints the message and returns test data
        original_fetch = gainer.fetch_gainers

        def mock_fetch():
            print("Downloading yahoo gainers")
            gainer.gainers = [{'symbol': 'MSFT', 'name': 'Microsoft Corp', 'price': '300.00', 'change': '+4.5%'}]
            return gainer.gainers

        gainer.fetch_gainers = mock_fetch

        gainer.process()

        # restore the original
        gainer.fetch_gainers = original_fetch

        # check that output contains expected strings
        output = mock_stdout.getvalue()
        self.assertIn("Downloading yahoo gainers", output)
        self.assertIn("Saving Yahoo gainers", output)


if __name__ == '__main__':
    unittest.main()
