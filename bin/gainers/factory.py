"""Factory class for creating gainers"""
from .wsj import WSJGainer
from .yahoo import YahooGainer
from .mock import MockGainer
from .cnbc import CNBCGainer


class GainerFactory:
    """factory class for creating gainers"""

    @staticmethod
    def create_gainer(source_type):
        """
        create a gainer based on the source type

        Args:
            source_type (str): type of gainer to create (wsj, yahoo, mock, cnbc)

        Returns:
            BaseGainer: instance of the specified gainer

        Raises:
            ValueError: If the source type isnt supported
        """
        if source_type.lower() == 'wsj':
            return WSJGainer()
        elif source_type.lower() == 'yahoo':
            return YahooGainer()
        elif source_type.lower() == 'mock':
            return MockGainer()
        elif source_type.lower() == 'cnbc':
            return CNBCGainer()
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
