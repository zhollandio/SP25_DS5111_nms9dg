"""Mock Gainer implementation for testing."""
from datetime import datetime
from .base import BaseGainer


class MockGainer(BaseGainer):
    """Mock gainer for testing without external dependencies."""

    def __init__(self):
        """Initialize the mock gainer."""
        super().__init__()
        self.url = "https://mock.example.com/gainers"
        # Predefined test data
        self.mock_data = [
            {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': '150.00', 'change': '+5.0%'},
            {'symbol': 'MSFT', 'name': 'Microsoft Corp.', 'price': '300.00', 'change': '+4.5%'},
            {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': '120.00', 'change': '+3.8%'},
            {'symbol': 'AMZN', 'name': 'Amazon.com Inc.', 'price': '135.50', 'change': '+3.2%'},
            {'symbol': 'META', 'name': 'Meta Platforms Inc.', 'price': '225.75', 'change': '+2.9%'}
        ]

    def fetch_gainers(self):
        """Fetch gainers from mock data (no external request)."""
        print("Downloading mock gainers")
        # No actual HTTP request is made here
        self.gainers = self.parse_data(None)
        return self.gainers

    def parse_data(self, data):
        """Return mock data instead of parsing external HTML."""
        print("Normalizing mock gainers")
        # Simply return the predefined data
        return self.mock_data

    def save_with_timestamp(self):
        """Save mock gainers with timestamp."""
        print("Saving Mock gainers")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mock_gainers_{timestamp}.csv"

        print(f"Mock data would be saved to {filename}")

        # No actual file writing occurs in mock mode
        # But we could implement it like this:
        # with open(filename, 'w') as f:
        #     f.write("symbol,name,price,change\n")
        #     for gainer in self.gainers:
        #         f.write(f"{gainer['symbol']},{gainer['name']},{gainer['price']},{gainer['change']}\n")
