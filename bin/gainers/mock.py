"""Mock Gainer implem for testing."""
from datetime import datetime
from .base import BaseGainer


class MockGainer(BaseGainer):
    """mock gainer for testing w/o external dependencies"""

    def __init__(self):
        """init"""
        super().__init__()
        self.url = "https://mock.example.com/gainers"
        # predefined test data
        self.mock_data = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': '150.00', 'change': '+5.0%'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'price': '300.00', 'change': '+4.5%'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': '120.00', 'change': '+3.8%'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'price': '135.50', 'change': '+3.2%'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'price': '225.75', 'change': '+2.9%'}
        ]

    def fetch_gainers(self):
        """fetch gainers from mock data"""
        print("Downloading mock gainers")
        # no actual HTTP request is made here
        self.gainers = self.parse_data(None)
        return self.gainers

    def parse_data(self, data):
        """return mock data instead of parsing external HTML"""
        print("Normalizing mock gainers")
        # just return the predefined data
        return self.mock_data

    def save_with_timestamp(self):
        """Save w timestamp"""
        print("Saving Mock gainers")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mock_gainers_{timestamp}.csv"

        print(f"Mock data would be saved to {filename}")
