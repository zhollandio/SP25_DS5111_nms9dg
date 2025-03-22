"""WSJ Gainer implementation."""
import requests
from bs4 import BeautifulSoup
from .base import BaseGainer


class WSJGainer(BaseGainer):
    """Class for fetching gainers from Wall Street Journal."""

    def __init__(self):
        """Initialize the WSJ gainer."""
        super().__init__()
        self.url = "https://www.wsj.com/market-data/stocks/afterhours-gainers"

    def fetch_gainers(self):
        """Fetch gainers from WSJ."""
        print("Downloading WSJ gainers")
        response = requests.get(self.url, timeout=10)
        if response.status_code == 200:
            self.gainers = self.parse_data(response.text)
        else:
            print(f"Failed to fetch data: {response.status_code}")
        return self.gainers

    def parse_data(self, data):
        """Parse the HTML data from WSJ."""
        print("Normalizing WSJ gainers")
        gainers = []
        soup = BeautifulSoup(data, 'html.parser')
        # Implement your WSJ parsing logic here
        # Look for table elements containing the gainer data
        # Example (you'll need to adjust based on the actual page structure):
        gainer_table = soup.find('table', class_='WSJTables--table')
        if gainer_table:
            rows = gainer_table.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cells = row.find_all('td')
                if len(cells) >= 4:
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
        """Save the WSJ gainers to a file with timestamp."""
        print("Saving WSJ gainers")
        # Implement saving logic here
        # This could be added to the base class if the implementation is common
