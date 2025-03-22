"""Yahoo Gainer implem"""
import requests
from bs4 import BeautifulSoup
from .base import BaseGainer


class YahooGainer(BaseGainer):
    """fetching gainers from yahoo fin"""

    def __init__(self):
        """init"""
        super().__init__()
        self.url = "https://finance.yahoo.com/gainers"

    def fetch_gainers(self):
        """fetch from yahoo"""
        print("Downloading yahoo gainers")
        response = requests.get(self.url, timeout=10)
        if response.status_code == 200:
            self.gainers = self.parse_data(response.text)
        else:
            print(f"Failed to fetch data: {response.status_code}")
        return self.gainers

    def parse_data(self, data):
        """parse HTML data from yahoo"""
        print("Normalizing yahoo gainers")
        gainers = []
        soup = BeautifulSoup(data, 'html.parser')
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
        """save w timestamp"""
        print("Saving Yahoo gainers")
