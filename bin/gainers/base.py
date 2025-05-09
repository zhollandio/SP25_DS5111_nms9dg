"""base gainer class -  inherited by all gainer implems"""
from abc import ABC, abstractmethod


class BaseGainer(ABC):
    """abstract base class for all gainer implems"""

    def __init__(self):
        """init the gainer"""
        self.gainers = []
        self.url = None

    @abstractmethod
    def fetch_gainers(self):
        """fetch gainers from source"""
        pass

    @abstractmethod
    def parse_data(self, data):
        """parse the data from source"""
        pass

    def get_gainers(self):
        """gainers list"""
        self.fetch_gainers()
        return self.gainers

    def print_gainers(self):
        """gainers to the console"""
        for gainer in self.gainers:
            print(gainer)

    @abstractmethod
    def save_with_timestamp(self):
        """save w timestamp"""
        pass

    def process(self):
        """process"""
        self.fetch_gainers()
        for gainer in self.gainers:
            print(gainer)
        self.save_with_timestamp()
