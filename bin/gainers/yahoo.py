"""Yahoo Gainer implementation."""
import requests
from bs4 import BeautifulSoup
from .base import BaseGainer


class YahooGainer(BaseGainer):
    """Class for fetching gainers from Yahoo Finance."""

    def __init__(self):
        """Initialize the Yahoo gainer."""
        super().__init__()
        self.url = "https://finance.yahoo.com/gainers"

    def fetch_gainers(self):
        """Fetch gainers from Yahoo."""
        print("Downloading yahoo gainers")
        response = requests.get(self.url, timeout=10)
        if response.status_code == 200:
            self.gainers = self.parse_data(response.text)
        else:
            print(f"Failed to fetch data: {response.status_code}")
        return self.gainers

    def parse_data(self, data):
        """Parse the HTML data from Yahoo."""
        print("Normalizing yahoo gainers")
        gainers = []
        soup = BeautifulSoup(data, 'html.parser')
        # Implement your Yahoo parsing logic here
        # Example (you'll need to adjust based on the actual page structure):
        gainer_table = soup.find('table', {'data-test': 'gainers-table'})
        if gainer_table:
            rows = gainer_table.find('tbody').find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 5:
                    symbol = cells[0].text.strip()
                    name = cells[1].text.strip()
                    price = cells[2].text.strip()
                    change = cells[3].text.strip()
                    gainers.append({
                        'symbol': symbol,
                        'name': name,
                        'price': price,
                        'change': change
                    })
        return gainers

    def save_with_timestamp(self):
        """Save the Yahoo gainers to a file with timestamp."""
        print("Saving Yahoo gainers")
        # Implement saving logic here
