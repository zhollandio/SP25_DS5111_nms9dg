import sys
import os
import pytest
import pandas as pd
# project's root directory to sys.path so Python can find `bin/`
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from bin.normalize_csv import normalize_csv

# creating test dir and data
TEST_DIR = "tests/test_data"
os.makedirs(TEST_DIR, exist_ok=True)

VALID_CSV_CONTENT = """symbol,price,change,change %
AAPL,150,2,1.5
GOOGL,2800,50,1.8
"""
MISSING_COLUMN_CSV = """symbol,price
AAPL,150
GOOGL,2800
"""
INVALID_CSV_CONTENT = """random_text
This is not a CSV
"""

@pytest.fixture
def create_csv_file():
    """Helper fixture to create a test CSV file"""
    def _create(filename, content):
        file_path = os.path.join(TEST_DIR, filename)
        with open(file_path, "w") as f:
            f.write(content)
        return file_path
    return _create

# 1- test normalization of a valid csv
def test_normalize_valid_csv(create_csv_file):
    input_csv = create_csv_file("valid.csv", VALID_CSV_CONTENT)
    output_csv = normalize_csv(input_csv)

    assert os.path.exists(output_csv), "Output CSV was not created"

    df = pd.read_csv(output_csv)
    assert set(df.columns) == {'symbol', 'price', 'price_change', 'price_percent_change'}, "Column names mismatch"

# 2 - test missing file handling
def test_missing_file():
    with pytest.raises(FileNotFoundError, match="File not found"):
        normalize_csv("non_existent.csv")

#  3 - test incorrect input type
def test_invalid_input_type():
    with pytest.raises(ValueError, match="Expected a string file path"):
        normalize_csv(12345)

# 4 - test csv with missing expected cols
def test_missing_columns(create_csv_file):
    input_csv = create_csv_file("missing_columns.csv", MISSING_COLUMN_CSV)

    with pytest.raises(ValueError, match="Missing expected columns"):
        normalize_csv(input_csv)

# 5 - test output file naming
def test_output_filename(create_csv_file):
    input_csv = create_csv_file("stocks.csv", VALID_CSV_CONTENT)
    output_csv = normalize_csv(input_csv)

    expected_output = input_csv.replace(".csv", "_norm.csv")
    assert output_csv == expected_output, "Output file name mismatch"

# 6 - test empty csv file
def test_empty_csv(create_csv_file):
    input_csv = create_csv_file("empty.csv", "")

    with pytest.raises(ValueError, match="CSV file is empty or improperly formatted."):
        normalize_csv(input_csv)

# 7 - test trimming column names
def test_trimmed_column_names(create_csv_file):
    trimmed_csv_content = """ Symbol , Price , Change , Change %
AAPL,150,2,1.5
GOOGL,2800,50,1.8
"""
    input_csv = create_csv_file("trimmed_columns.csv", trimmed_csv_content)
    output_csv = normalize_csv(input_csv)

    df = pd.read_csv(output_csv)
    assert set(df.columns) == {'symbol', 'price', 'price_change', 'price_percent_change'}, "Column names were not correctly trimmed"

# 8 - test normalization w/o change cols
def test_normalization_without_change_columns(create_csv_file):
    csv_without_change_columns = """symbol,price
AAPL,150
GOOGL,2800
"""
    input_csv = create_csv_file("no_change_cols.csv", csv_without_change_columns)

    with pytest.raises(ValueError, match="Missing expected columns"):
        normalize_csv(input_csv)
