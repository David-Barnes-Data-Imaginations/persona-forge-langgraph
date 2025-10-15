#!/usr/bin/env python3
"""
Final CSV cleaner: removes blank lines and newlines within fields.
"""

import csv
import sys

def clean_csv(input_file, output_file):
    """Clean CSV by removing blank lines and newlines within fields"""

    print(f"📖 Reading: {input_file}")

    # First, remove blank lines from the file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]  # Remove blank lines

    print(f"✓ Removed blank lines")

    # Write to temporary file
    temp_file = input_file + ".temp"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    # Now use csv module to properly parse and clean
    with open(temp_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = []

        for row in reader:
            # Replace newlines and extra spaces in each field
            cleaned_row = [
                ' '.join(field.replace('\n', ' ').replace('\r', ' ').split())
                for field in row
            ]
            rows.append(cleaned_row)

    print(f"✓ Processed {len(rows)} rows (including header)")

    # Write cleaned CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

    # Clean up temp file
    import os
    os.remove(temp_file)

    print(f"✅ Saved to: {output_file}")
    print(f"✓ {len(rows) - 1} QA pairs ready")
    print(f"\n💡 Upload {output_file.split('/')[-1]} to your app!")

if __name__ == "__main__":
    input_path = "data/therapy_csvs/therapy-fin.csv"
    output_path = "data/therapy_csvs/therapy-fin_CLEAN.csv"

    try:
        clean_csv(input_path, output_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
