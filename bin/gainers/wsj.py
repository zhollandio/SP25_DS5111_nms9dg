"""WSJ Gainer implem using requests-html for JS rendering"""
import os
import csv
import re
import json
import time
import random
from datetime import datetime

from bs4 import BeautifulSoup
from requests_html import HTMLSession

from .base import BaseGainer

# having problems with wsj, moving to rendering js with requests-htlm
class WSJGainer(BaseGainer):
    """get gainers from  WSJ by rendering JS with requests-html"""

    def __init__(self):
        """init"""
        super().__init__()
        # updating url, last was 404
        self.url = "https://www.wsj.com/market-data/stocks/us/movers"

    def fetch_gainers(self):
        """
        use requests-html to fetch + render the WSJ page, parse
        """
        print("Downloading WSJ gainers (with JS rendering)...")
        session = HTMLSession()

        # user-agent to mimic a real browser (I was getting denied originally)
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/122.0.0.0 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                       'q=0.9,image/avif,image/webp,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive'
        }

        try:
            time.sleep(random.uniform(1, 3))

            # get the page
            response = session.get(self.url, headers=headers, timeout=20)
            if response.status_code != 200:
                print(f"Initial request failed with status code {response.status_code}")
                self.gainers = []
                return self.gainers

            # render JS (chromium)
            print("Rendering JavaScript...")
            response.html.render(timeout=30, sleep=3)

            # final HTML after JS loads
            rendered_html = response.html.html

            # parse the rendered HTML
            self.gainers = self.parse_data(rendered_html)
            return self.gainers

        except Exception as e:
            print(f"Error fetching data from WSJ: {e}")
            self.gainers = []
            return self.gainers

    def parse_data(self, html_data):
        """
        parse the rendered HTML:

        From the URL, we know the table structure (5 columns) is:
        1) Name (Ticker)
        2) Volume
        3) Last (Price)
        4) Change
        5) % Change
        """
        print("Normalizing WSJ gainers")
        gainers = []
        soup = BeautifulSoup(html_data, 'html.parser')

        # creating debug folder to check
        debug_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'debug'
        )
        os.makedirs(debug_dir, exist_ok=True)

        debug_file = os.path.join(debug_dir, 'wsj_debug_rendered.html')
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(html_data)

        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables on the rendered page.")

        # parse each table
        for table_idx, table in enumerate(tables, start=1):
            rows = table.find_all('tr')
            if len(rows) <= 1:
                continue  # skip tables without data rows

            for i, row in enumerate(rows[1:], start=1):
                cells = row.find_all('td')
                # we want at least 5 columns: Name(Ticker), Volume, Last, Change, %Change
                if len(cells) < 5:
                    continue

                raw_symbol = cells[0].get_text(strip=True)
                volume = cells[1].get_text(strip=True)
                last_price = cells[2].get_text(strip=True)
                change = cells[3].get_text(strip=True)
                pct_change = cells[4].get_text(strip=True)

                # separate the name from the ticker, e.g. "MicroAlgo Inc. (MLGO)"
                match = re.match(r'(.*?)\s*\((.*?)\)', raw_symbol)
                if match:
                    name = match.group(1).strip()
                    symbol = match.group(2).strip()
                else:
                    # fallback if no parentheses
                    name = raw_symbol
                    symbol = raw_symbol

                gainers.append({
                    'Symbol': symbol,
                    'Company': name,
                    'Volume': volume,
                    'Price': last_price,
                    'Change': change,
                    '%Change': pct_change
                })

        # if no gainers found - trying JSON
        if not gainers:
            print("No table data found. Attempting to find embedded JSON data...")
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'marketModules' in script.string:
                    try:
                        start_idx = script.string.find('{')
                        if start_idx != -1:
                            json_str = script.string[start_idx:]
                            parsed_json = json.loads(json_str)
                            if 'marketModules' in parsed_json:
                                for item in parsed_json.get('gainers', []):
                                    gainers.append({
                                        'Symbol': item.get('ticker', ''),
                                        'Company': item.get('name', ''),
                                        'Price': str(item.get('price', '')),
                                        'Change': f"{item.get('change', '')} ({item.get('percentChange', '')}%)",
                                        'Volume': str(item.get('volume', 'N/A'))
                                    })
                    except Exception:
                        pass

        print(f"Extracted {len(gainers)} gainers from WSJ")
        return gainers

    def save_with_timestamp(self):
        """
        save the gainer list to a CSV
        """
        print("Saving WSJ gainers")
        if not self.gainers:
            print("No gainers to save.")
            return

        # data directory
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            'data'
        )
        wsj_dir = os.path.join(data_dir, 'wsj')
        os.makedirs(wsj_dir, exist_ok=True)

        # timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M")
        time_of_day = os.environ.get("TIME_OF_DAY", "unknown")

        # filename
        filename = os.path.join(wsj_dir, f'wsj_gainers_{timestamp}_{time_of_day}.csv')

        # to csv
        fieldnames = list(self.gainers[0].keys())
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for gainer in self.gainers:
                writer.writerow(gainer)

        print(f"Successfully saved WSJ gainers to {filename}")
