#!/usr/bin/env python3
"""
Script to get stock gainers using strategy pattern (extra credit)

Usage:
    python get_gainer_strategy.py
"""
import sys
from bin.gainers.strategy.gainer_context import GainerContext


def main():
    """main function to run script."""
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
