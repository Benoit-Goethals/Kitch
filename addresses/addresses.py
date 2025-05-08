import csv
import os

# Change the working directory to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Input and output file paths
input_file = "openaddress-bevlg.csv"
output_file = "addresses.csv"

# Filter and write only the required columns to the output file
required_columns = [
    "streetname_nl",
    "house_number",
    "postcode",
    "municipality_name_nl",
    "EPSG:4326_lat",
    "EPSG:4326_lon",
]

# Check if the output file exists, if not, create it with a header
if not os.path.exists(output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=required_columns)
        writer.writeheader()

# Read the input file and write filtered columns to the output file
with open(input_file, "r", newline="", encoding="utf-8") as infile:
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=required_columns)

        # Write the new header
        writer.writeheader()

        # Write only the required columns for the first 100 rows
        row_count = 0
        for row in reader:
            if row_count >= 200:
                break
            filtered_row = {col: row[col] for col in required_columns if col in row}
            writer.writerow(filtered_row)
            row_count += 1
