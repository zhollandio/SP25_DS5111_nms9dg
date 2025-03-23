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
        # we need to make sure these lines actually print to stdout
        # and don't just call the internal functions
        self.fetch_gainers()
        # print
        for gainer in self.gainers:
            print(gainer)
        # save
        self.save_with_timestamp()
