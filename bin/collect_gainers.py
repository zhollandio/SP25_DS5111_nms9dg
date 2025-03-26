#!/usr/bin/env python3
"""
Script to collect stock gainer data from Yahoo and WSJ based on time of day
"""
import argparse
import os
import sys
import traceback

# define project_root before imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from bin.gainers.factory import GainerFactory

def main():
    """main function to parse arguments +  process stock gainer sources"""
    parser = argparse.ArgumentParser(description='Collect stock gainers data')
    parser.add_argument('time_of_day', choices=['morning', 'noon', 'afternoon'],
                        help='Time of day for data collection')
    args = parser.parse_args()

    # prep data directories
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(os.path.join(data_dir, 'yahoo'), exist_ok=True)
    os.makedirs(os.path.join(data_dir, 'wsj'), exist_ok=True)

    factory = GainerFactory()
    sources = ['yahoo', 'wsj']
    for source in sources:
        try:
            print(f"Processing {source} gainers for {args.time_of_day}...")
            gainer = factory.create_gainer(source)
            gainer.process()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Error collecting {source.upper()} gainers: {e}", file=sys.stderr)
            traceback.print_exc()

if __name__ == "__main__":
    main()
