#!/usr/bin/env python3
"""
Script to get stock gainers using Strategy pattern.

Usage:
    python get_gainer_strategy.py <source>
"""
import sys
from bin.gainers.strategy.gainer_context import GainerContext


def main():
    """Main function to run the gainer script."""
    if len(sys.argv) < 2:
        print("Usage: python get_gainer_strategy.py <source>")
        print("Available sources: wsj, yahoo")
        sys.exit(1)

    source = sys.argv[1]
    try:
        context = GainerContext()
        context.set_strategy(source)
        gainers = context.execute()
        return gainers
    except ValueError as e:
        print(f"Error: {e}")
        print("Available sources: wsj, yahoo")
        sys.exit(1)


if __name__ == "__main__":
    main()
