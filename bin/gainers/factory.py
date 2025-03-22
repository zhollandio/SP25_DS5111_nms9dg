"""Factory class for creating gainers."""
from .wsj import WSJGainer
from .yahoo import YahooGainer
from .mock import MockGainer
from .cnbc import CNBCGainer


class GainerFactory:
    """Factory class for creating gainers."""

    @staticmethod
    def create_gainer(source_type):
        """
        Create a gainer based on the source type.
        
        Args:
            source_type (str): Type of gainer to create (wsj, yahoo, mock, cnbc)
            
        Returns:
            BaseGainer: An instance of the specified gainer
            
        Raises:
            ValueError: If the source type is not supported
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
