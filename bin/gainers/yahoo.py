"""Yahoo Gainer implem"""
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import os
import csv
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
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
        }

        # add slight delay (avoid rate limiting)
        time.sleep(random.uniform(1, 3))

        response = requests.get(self.url, headers=headers, timeout=15)
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
        if not gainer_table:
            tables = soup.find_all('table')
            for table in tables:
                if table.find('tr'):  # make sure it has rows
                    gainer_table = table
                    break

        if gainer_table:
            tbody = gainer_table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
            else:
                rows = gainer_table.find_all('tr')[1:]  # skip header row

            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 5:
                    symbol = cells[0].text.strip()
                    name = cells[1].text.strip()
                    price = cells[2].text.strip()
                    change = cells[3].text.strip()

                    if symbol and name:
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
        if not self.gainers:
            print("No gainers to save")
            return

        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
        yahoo_dir = os.path.join(data_dir, 'yahoo')
        os.makedirs(yahoo_dir, exist_ok=True)

        # timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M")
        time_of_day = os.environ.get("TIME_OF_DAY", "unknown")

        # Create filename
        filename = os.path.join(yahoo_dir, f'yahoo_gainers_{timestamp}_{time_of_day}.csv')

        # save to csv
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = self.gainers[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for gainer in self.gainers:
                writer.writerow(gainer)

        print(f"Successfully saved Yahoo gainers to {filename}")
