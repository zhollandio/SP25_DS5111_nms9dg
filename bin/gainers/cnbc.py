"""CNBC Gainer implementation."""
import requests
from bs4 import BeautifulSoup
from .base import BaseGainer
from datetime import datetime


class CNBCGainer(BaseGainer):
    """Class for fetching gainers from CNBC Market Movers."""

    def __init__(self):
        """Initialize the CNBC gainer."""
        super().__init__()
        self.url = "https://www.cnbc.com/us-market-movers/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

    def fetch_gainers(self):
        """Fetch gainers from CNBC."""
        print("Downloading CNBC gainers")
        response = requests.get(self.url, headers=self.headers, timeout=10)
        if response.status_code == 200:
            self.gainers = self.parse_data(response.text)
        else:
            print(f"Failed to fetch data: {response.status_code}")
        return self.gainers

    def parse_data(self, data):
        """Parse the HTML data from CNBC."""
        print("Normalizing CNBC gainers")
        gainers = []
        soup = BeautifulSoup(data, 'html.parser')

        # CNBC market movers page structure
        # The actual structure might need adjustment based on the actual page
        gainer_section = soup.find('div', {'class': 'MarketMoversTable-table'})

        if gainer_section:
            rows = gainer_section.find_all('tr')
            for row in rows[1:]:  # Skip header row
                cells = row.find_all('td')
                if len(cells) >= 4:
                    try:
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
                    except (IndexError, AttributeError):
                        continue

        return gainers

    def save_with_timestamp(self):
        """Save the CNBC gainers to a file with timestamp."""
        print("Saving CNBC gainers")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cnbc_gainers_{timestamp}.csv"

        # Save to CSV file
        try:
            with open(filename, 'w') as f:
                f.write("symbol,name,price,change\n")
                for gainer in self.gainers:
                    f.write(f"{gainer['symbol']},{gainer['name']},{gainer['price']},{gainer['change']}\n")
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
