"""WSJ Strategy implementation."""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .base_strategy import GainerStrategy


class WSJStrategy(GainerStrategy):
    """Strategy for fetching gainers from WSJ."""
    
    def __init__(self):
        """Initialize the WSJ strategy."""
        self.url = "https://www.wsj.com/market-data/stocks/afterhours-gainers"
    
    def fetch_data(self):
        """Fetch data from WSJ."""
        print("Downloading WSJ gainers")
        response = requests.get(self.url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
    
    def parse_data(self, data):
        """Parse the HTML data from WSJ."""
        print("Normalizing WSJ gainers")
        gainers = []
        if not data:
            return gainers
            
        soup = BeautifulSoup(data, 'html.parser')
        # Implement parsing logic similar to original WSJ class
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
    
    def save_data(self, gainers):
        """Save the WSJ gainers to a file."""
        print("Saving WSJ gainers")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wsj_gainers_{timestamp}.csv"
        
        try:
            with open(filename, 'w') as f:
                f.write("symbol,name,price,change\n")
                for gainer in gainers:
                    f.write(f"{gainer['symbol']},{gainer['name']},{gainer['price']},{gainer['change']}\n")
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
