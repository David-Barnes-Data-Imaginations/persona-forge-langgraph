#!/usr/bin/env python3
"""
Flatten CSV: Read with proper CSV parser, then write with all newlines as spaces.
This preserves the QA pair structure while flattening multi-line text.
"""

import csv
import sys

def flatten_csv(input_file, output_file):
    """Read CSV properly and flatten all text to single lines"""

    print(f"📖 Reading: {input_file}")

    rows = []
    errors = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            # Use csv.reader to properly handle quoted multi-line fields
            reader = csv.reader(f, skipinitialspace=True)

            for i, row in enumerate(reader):
                if len(row) == 0:
                    continue  # Skip empty rows

                if len(row) != 3:
                    errors.append(f"Line {i+1}: Expected 3 fields, got {len(row)}: {row}")
                    continue

                # Flatten each field: remove newlines, compress whitespace
                cleaned_row = [
                    ' '.join(field.replace('\n', ' ').replace('\r', ' ').split()).strip()
                    for field in row
                ]
                rows.append(cleaned_row)

    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    print(f"✓ Successfully parsed {len(rows)} rows (including header)")

    if errors:
        print(f"\n⚠️  Skipped {len(errors)} malformed rows:")
        for err in errors[:5]:  # Show first 5 errors
            print(f"  {err}")

    # Validate we have QA pairs (rows with header)
    if len(rows) < 2:
        print("❌ No valid QA pairs found")
        sys.exit(1)

    qa_count = len(rows) - 1  # Exclude header
    print(f"✓ Found {qa_count} QA pairs")

    # Write cleaned CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

    print(f"✅ Saved to: {output_file}")
    print(f"\n💡 Upload {output_file.split('/')[-1]} to your app!")

if __name__ == "__main__":
    input_path = "data/therapy_csvs/therapy-fin.csv"
    output_path = "data/therapy_csvs/therapy-fin_FLAT.csv"

    flatten_csv(input_path, output_path)
