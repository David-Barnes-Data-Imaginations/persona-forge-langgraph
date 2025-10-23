#!/usr/bin/env python3
"""
Simple script to remove all newlines from CSV fields while keeping proper CSV structure.
This converts multi-line quoted fields into single-line fields.
"""

import csv
import sys

def remove_newlines_from_csv(input_file, output_file):
    """Remove all newlines from CSV fields"""

    print(f"📖 Reading: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = []

        for row in reader:
            # Replace newlines with spaces in each field
            cleaned_row = [field.replace('\n', ' ').replace('\r', ' ').strip() for field in row]
            rows.append(cleaned_row)

    print(f"✓ Read {len(rows)} rows (including header)")

    # Write cleaned CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

    print(f"✅ Saved to: {output_file}")
    print(f"✓ All newlines removed from fields")
    print(f"\n💡 Upload {output_file.split('/')[-1]} to your app!")

if __name__ == "__main__":
    input_path = "data/therapy_csvs/therapy-fin.csv"
    output_path = "data/therapy_csvs/therapy-fin_NO_NEWLINES.csv"

    try:
        remove_newlines_from_csv(input_path, output_path)
    except FileNotFoundError:
        print(f"❌ File not found: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
