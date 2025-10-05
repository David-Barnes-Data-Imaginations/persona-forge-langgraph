#!/usr/bin/env python3
"""
Convert broken CSV format to correct format

Converts:
    Therapist,Client,message_id
    "question",

    "answer",1

To:
    Therapist,Client,message_id
    "question","answer",1
"""

import sys
import re
from pathlib import Path


def convert_csv_format(input_file: str) -> str:
    """
    Convert broken CSV format to proper format

    Args:
        input_file: Path to broken CSV file

    Returns:
        Path to fixed file
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    output_file = input_path.parent / f"{input_path.stem}_converted{input_path.suffix}"

    print(f"📄 Reading: {input_file}")

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"📏 Original file size: {len(content)} chars")

    # Split into lines
    lines = content.split('\n')

    # New format lines
    output_lines = []

    # Keep header
    output_lines.append(lines[0])  # Therapist,Client,message_id

    # Process remaining lines
    i = 1
    qa_pair_num = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Check if this looks like a question (starts with quote, ends with comma)
        if line.startswith('"') and (line.endswith(',') or line.endswith('","')):
            # This is a question line
            question = line.rstrip(',').strip()

            # Look for the answer in following lines
            answer_lines = []
            i += 1

            # Skip empty lines after question
            while i < len(lines) and not lines[i].strip():
                i += 1

            # Collect answer lines until we hit a line with message_id
            while i < len(lines):
                answer_line = lines[i].rstrip('\n')

                # Check if this line has the message_id (ends with ,N)
                if re.search(r',\s*\d+\s*$', answer_line):
                    # Extract the answer and message_id
                    # The line should be like: "answer text...",1
                    match = re.match(r'^(.+),(\d+)\s*$', answer_line)
                    if match:
                        answer_lines.append(match.group(1))
                        message_id = match.group(2)

                        # Combine everything into one row
                        # Join answer lines preserving internal newlines
                        answer = '\n'.join(answer_lines) if answer_lines else '""'

                        # Create proper CSV row
                        # Format: "question","answer",message_id
                        output_row = f'{question},{answer},{message_id}'
                        output_lines.append(output_row)

                        qa_pair_num += 1
                        print(f"✓ Converted QA pair {qa_pair_num}")

                        i += 1
                        break
                    else:
                        # Malformed line
                        print(f"⚠️  Warning: Malformed answer ending at line {i+1}: {answer_line[:60]}")
                        answer_lines.append(answer_line)
                        i += 1
                        break
                else:
                    # Part of the answer
                    answer_lines.append(answer_line)
                    i += 1
        else:
            # Unexpected format
            print(f"⚠️  Skipping unexpected line {i+1}: {line[:60]}")
            i += 1

    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(output_lines))

    print(f"\n✅ Converted CSV saved to: {output_file}")
    print(f"   Converted {qa_pair_num} QA pairs")

    return str(output_file)


def preview_csv(file_path: str, num_rows: int = 3):
    """Show first few rows of CSV"""
    print(f"\n📋 Preview of {file_path}:")
    print("=" * 80)

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:num_rows + 1]):  # +1 for header
            if i == 0:
                print(f"Header: {line.strip()}")
            else:
                # Show first 100 chars of each field
                parts = line.split('","')
                print(f"\nRow {i}:")
                if len(parts) >= 1:
                    q = parts[0].strip('"')
                    print(f"  Question: {q[:80]}{'...' if len(q) > 80 else ''}")
                if len(parts) >= 2:
                    # Handle the answer + message_id
                    rest = '","'.join(parts[1:])
                    # Split on the last comma to separate answer from message_id
                    last_comma = rest.rfind(',')
                    if last_comma > 0:
                        a = rest[:last_comma].strip('"')
                        mid = rest[last_comma+1:].strip()
                        print(f"  Answer: {a[:80]}{'...' if len(a) > 80 else ''}")
                        print(f"  Message ID: {mid}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert_csv_format.py <your_csv_file.csv>")
        print("\nThis will create: your_csv_file_converted.csv")
        print("\nConverts broken format:")
        print('  "question",')
        print('  ')
        print('  "answer",1')
        print("\nTo proper format:")
        print('  "question","answer",1')
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Convert the CSV
        converted_file = convert_csv_format(input_file)

        # Show preview
        preview_csv(converted_file, num_rows=2)

        print("\n💡 Next steps:")
        print(f"   1. Review: {converted_file}")
        print(f"   2. Upload to sentiment suite")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
