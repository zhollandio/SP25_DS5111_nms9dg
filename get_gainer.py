#!/usr/bin/env python3
"""
Script to get stock gainers from different sources.

Usage:
    python get_gainer.py
"""
import sys
from bin.gainers.factory import GainerFactory


def main():
    """main function to run script"""
    if len(sys.argv) < 2:
        print("Usage: python get_gainer.py <source>")
        print("Available sources: wsj, yahoo")
        sys.exit(1)

    source = sys.argv[1]
    try:
        gainer = GainerFactory.create_gainer(source)
        gainers = gainer.get_gainers()
        gainer.print_gainers()
        return gainers
    except ValueError as e:
        print(f"Error: {e}")
        print("Available sources: wsj, yahoo")
        sys.exit(1)


if __name__ == "__main__":
    main()
