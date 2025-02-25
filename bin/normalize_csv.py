"""
normalize_csv.py

This script normalizes a stock market CSV file into a standardized format.
It reads a raw CSV file, renames columns, ensures required fields exist, and
saves the cleaned file with a "_norm.csv" suffix.

Usage:
    python bin/normalize_csv.py <path_to_csv>
"""

import sys
import os
import pandas as pd

def normalize_csv(input_csv):
    """
    Normalizes a given stock market CSV file into a standard format.

    Parameters:
    input_csv (str): Path to the raw CSV file

    Returns:
    str: Path to the normalized CSV file
    """
    if not isinstance(input_csv, str):
        raise ValueError(f"Expected a string file path, got {type(input_csv)}")
    if not os.path.exists(input_csv):
        raise FileNotFoundError(f"File not found: {input_csv}")

    try:
        df = pd.read_csv(input_csv)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("CSV file is empty or improperly formatted.") from exc
    except pd.errors.ParserError as exc:
        raise ValueError("File is not a valid CSV format.") from exc

    # normalize column names
    df.columns = df.columns.str.strip().str.lower()

    expected_columns = ['symbol', 'price', 'price_change', 'price_percent_change']
    column_mappings = {
        'symbol': 'symbol',
        'price': 'price',
        'change': 'price_change',
        '% change': 'price_percent_change',
        'ticker': 'symbol',
        'last price': 'price',
        'change amount': 'price_change',
        'change %': 'price_percent_change'
    }

    df.rename(columns=column_mappings, inplace=True)

    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")

    df = df[expected_columns]
    output_csv = input_csv.replace(".csv", "_norm.csv")
    df.to_csv(output_csv, index=False)

    print(f"Normalized CSV saved as: {output_csv}")
    return output_csv

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bin/normalize_csv.py <path_to_csv>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        normalize_csv(input_file)
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
