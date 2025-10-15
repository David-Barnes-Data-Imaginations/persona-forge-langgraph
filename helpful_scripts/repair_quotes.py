#!/usr/bin/env python3
"""
Repair CSV quotes by detecting QA pair patterns and fixing quote mismatches.
"""

import re

def repair_csv_quotes(input_file, output_file):
    """Repair quote issues in CSV file"""

    print(f"📖 Reading: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into lines but keep the content
    lines = content.split('\n')

    print(f"✓ Read {len(lines)} lines")

    # Strategy: Find patterns like `",\d+` (end of answer) and work backwards
    # to find the start of each QA pair

    repaired_lines = []
    current_qa = []
    in_qa_pair = False

    for i, line in enumerate(lines):
        if i == 0:  # Header
            repaired_lines.append(line)
            continue

        # Check if this line ends a QA pair (pattern: something",NUMBER or something",)
        if re.search(r'",\s*\d+\s*$', line) or (line.strip() == '' and current_qa):
            # This is the end of a QA pair
            current_qa.append(line)

            # Join all lines of this QA pair
            if current_qa:
                qa_text = '\n'.join(current_qa)

                # Only keep if it looks like a valid QA pair
                if re.search(r'",\s*\d+\s*$', qa_text):
                    # Flatten newlines to spaces
                    qa_flat = ' '.join(qa_text.replace('\n', ' ').split())
                    repaired_lines.append(qa_flat)

            current_qa = []
            continue

        # Start of new QA pair (starts with quote)
        if line.strip().startswith('"'):
            current_qa = [line]
        elif current_qa:  # Continuation of current QA pair
            current_qa.append(line)

    print(f"✓ Extracted {len(repaired_lines) - 1} QA pairs")

    # Write repaired CSV
    output_content = '\n'.join(repaired_lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)

    print(f"✅ Saved to: {output_file}")
    print(f"\n💡 Try uploading {output_file.split('/')[-1]} to your app!")

if __name__ == "__main__":
    input_path = "data/therapy_csvs/therapy-fin.csv"
    output_path = "data/therapy_csvs/therapy-fin_REPAIRED.csv"

    repair_csv_quotes(input_path, output_path)
