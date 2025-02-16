import sys
import os
import pytest
import pandas as pd
# project's root directory to sys.path so Python can find `bin/`
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from bin.merge_csvs import merge_csvs

# check for test_data, create if = false
TEST_DIR = "tests/test_data"
os.makedirs(TEST_DIR, exist_ok=True)

CSV_CONTENT_1 = """symbol,price,price_change,price_percent_change
AAPL,150,2,1.5
GOOGL,2800,50,1.8
"""
CSV_CONTENT_2 = """symbol,price,price_change,price_percent_change
TSLA,900,20,2.3
MSFT,310,5,1.6
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

# 1 - test successful merging of 2 valid csvs
def test_merge_valid_csvs(create_csv_file):
    csv1 = create_csv_file("valid1.csv", CSV_CONTENT_1)
    csv2 = create_csv_file("valid2.csv", CSV_CONTENT_2)
    output_file = os.path.join(TEST_DIR, "merged_output.csv")

    merge_csvs(csv1, csv2, output_dir=TEST_DIR, output_file="merged_output.csv")

    assert os.path.exists(output_file), "Merged CSV file was not created"

    df = pd.read_csv(output_file)
    assert len(df) == 4, "Merged file should contain 4 rows"

# 2 - test handling of missing input files
def test_merge_missing_file(create_csv_file):
    csv1 = create_csv_file("valid1.csv", CSV_CONTENT_1)
    missing_csv = os.path.join(TEST_DIR, "missing.csv")

    with pytest.raises(AssertionError, match="File not found"):
        merge_csvs(csv1, missing_csv)

# 3 - test output file naming
def test_merge_output_filename(create_csv_file):
    csv1 = create_csv_file("valid1.csv", CSV_CONTENT_1)
    csv2 = create_csv_file("valid2.csv", CSV_CONTENT_2)
    expected_output = os.path.join(TEST_DIR, "custom_output.csv")

    merge_csvs(csv1, csv2, output_dir=TEST_DIR, output_file="custom_output.csv")

    assert os.path.exists(expected_output), "Output file name mismatch"

# 4 - test empty csv handling
def test_merge_empty_csv(create_csv_file):
    csv1 = create_csv_file("valid1.csv", CSV_CONTENT_1)
    empty_csv = create_csv_file("empty.csv", "")

    with pytest.raises(pd.errors.EmptyDataError):
        merge_csvs(csv1, empty_csv)
