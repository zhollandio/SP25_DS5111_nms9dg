"""Base Gainer class to be inherited by all gainer implementations."""
from abc import ABC, abstractmethod


class BaseGainer(ABC):
    """Abstract base class for all gainer implementations."""

    def __init__(self):
        """Initialize the gainer."""
        self.gainers = []
        self.url = None

    @abstractmethod
    def fetch_gainers(self):
        """Fetch gainers from the source."""
        pass

    @abstractmethod
    def parse_data(self, data):
        """Parse the data from the source."""
        pass

    def get_gainers(self):
        """Get the gainers list."""
        self.fetch_gainers()
        return self.gainers

    def print_gainers(self):
        """Print the gainers to the console."""
        for gainer in self.gainers:
            print(gainer)

    @abstractmethod
    def save_with_timestamp(self):
        """Save gainers with timestamp (from original design)."""
        pass

    def process(self):
        """Process the gainers (template method from original design)."""
        # We need to make sure these lines actually print to stdout
        # and don't just call the internal functions
        self.fetch_gainers()  # This function has print statements inside
        # Print the gainers
        for gainer in self.gainers:
            print(gainer)
        # Save with timestamp
        self.save_with_timestamp()
