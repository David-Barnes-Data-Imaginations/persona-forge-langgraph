#!/usr/bin/env python3
"""
Quick script to fix CSV quoting issues

This script:
1. Reads your CSV
2. Properly escapes double quotes inside quoted fields
3. Saves a fixed version

Usage:
    python3 fix_csv_quotes.py your_therapy_file.csv
"""

import sys
import csv
from pathlib import Path


def fix_csv_quotes(input_file: str) -> str:
    """
    Fix CSV file by properly handling quotes

    Args:
        input_file: Path to CSV file to fix

    Returns:
        Path to fixed file
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    # Create output filename
    output_file = input_path.parent / f"{input_path.stem}_fixed{input_path.suffix}"

    print(f"📄 Reading: {input_file}")

    # Read the CSV
    with open(input_path, 'r', encoding='utf-8') as f:
        # Read all lines
        lines = f.readlines()

    print(f"📏 Total lines: {len(lines)}")

    # Write properly formatted CSV
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)  # Quote all fields

        # Parse the input more carefully
        reader = csv.reader(lines, quotechar='"', doublequote=True, skipinitialspace=True)

        rows_written = 0
        for row_num, row in enumerate(reader, 1):
            try:
                # Clean up the row
                cleaned_row = []
                for field in row:
                    # Strip whitespace
                    field = field.strip()
                    cleaned_row.append(field)

                # Write the row
                writer.writerow(cleaned_row)
                rows_written += 1

                if rows_written <= 3:
                    print(f"✓ Row {row_num}: {len(cleaned_row)} fields")

            except Exception as e:
                print(f"⚠️  Error on row {row_num}: {e}")
                print(f"    Raw row: {row}")

    print(f"\n✅ Fixed CSV saved to: {output_file}")
    print(f"   Wrote {rows_written} rows")
    return str(output_file)


def preview_csv(file_path: str, num_rows: int = 5):
    """Show first few rows of CSV"""
    print(f"\n📋 Preview of {file_path}:")
    print("=" * 80)

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i >= num_rows:
                break
            print(f"Row {i+1}: {len(row)} fields")
            for j, field in enumerate(row):
                preview = field[:60] + "..." if len(field) > 60 else field
                print(f"  [{j+1}] {preview}")
            print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fix_csv_quotes.py <your_csv_file.csv>")
        print("\nThis will create a new file: your_csv_file_fixed.csv")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Fix the CSV
        fixed_file = fix_csv_quotes(input_file)

        # Show preview
        preview_csv(fixed_file, num_rows=3)

        print("\n💡 Next steps:")
        print(f"   1. Review the fixed file: {fixed_file}")
        print(f"   2. Upload {Path(fixed_file).name} to your sentiment suite")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
