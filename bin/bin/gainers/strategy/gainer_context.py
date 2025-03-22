"""Context for Strategy pattern implementation."""
from .wsj_strategy import WSJStrategy
from .yahoo_strategy import YahooStrategy


class GainerContext:
    """Context class that uses a strategy to get gainers."""
    
    def __init__(self, strategy_type=None):
        """Initialize the gainer context with a strategy."""
        self.strategy = None
        self.gainers = []
        
        if strategy_type:
            self.set_strategy(strategy_type)
    
    def set_strategy(self, strategy_type):
        """Set the strategy based on the type."""
        if strategy_type.lower() == 'wsj':
            self.strategy = WSJStrategy()
        elif strategy_type.lower() == 'yahoo':
            self.strategy = YahooStrategy()
        else:
            raise ValueError(f"Unsupported strategy type: {strategy_type}")
    
    def execute(self):
        """Execute the strategy."""
        if not self.strategy:
            raise ValueError("No strategy set")
            
        data = self.strategy.fetch_data()
        self.gainers = self.strategy.parse_data(data)
        self.print_gainers()
        self.strategy.save_data(self.gainers)
        return self.gainers
    
    def print_gainers(self):
        """Print the gainers to the console."""
        for gainer in self.gainers:
            print(gainer)
