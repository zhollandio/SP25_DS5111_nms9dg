"""Strategy pattern for gainers."""
from abc import ABC, abstractmethod


class GainerStrategy(ABC):
    """Strategy interface for fetching gainers data."""

    @abstractmethod
    def fetch_data(self):
        """Fetch data from source."""
        pass

    @abstractmethod
    def parse_data(self, data):
        """Parse data from source."""
        pass

    @abstractmethod
    def save_data(self, gainers):
        """Save data to file."""
        pass
