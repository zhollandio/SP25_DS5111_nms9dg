import sys
import os
import pandas as pd

def merge_csvs(csv1, csv2, output_dir="sample_data", output_file="merged_gainers.csv"):
    """
    Merges two normalized CSV files into one and saves it in the specified output directory.

    Parameters:
    csv1 (str): Path to the first normalized CSV file.
    csv2 (str): Path to the second normalized CSV file.
    output_dir (str): Directory where the merged file should be saved.
    output_file (str): Name of the merged CSV output file (default: merged_gainers.csv).

    Returns:
    None
    """
    assert os.path.exists(csv1), f"File not found: {csv1}"
    assert os.path.exists(csv2), f"File not found: {csv2}"

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_file)

    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    merged_df = pd.concat([df1, df2], ignore_index=True)
    merged_df.to_csv(output_path, index=False)

    print(f"Merged CSV saved as: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python bin/merge_csvs.py <normalized_csv1> <normalized_csv2>")
        sys.exit(1)

    csv1 = sys.argv[1]
    csv2 = sys.argv[2]

    merge_csvs(csv1, csv2)
