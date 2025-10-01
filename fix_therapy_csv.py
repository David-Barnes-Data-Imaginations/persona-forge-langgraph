#!/usr/bin/env python3
"""
Fix the therapy CSV by merging question and answer onto same row
"""

import re

# Read the broken file
with open('data/therapy_csvs/therapy-fin.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Output lines
output = []

# Keep header
output.append(lines[0].strip())

# Process the rest
i = 1
qa_count = 0

while i < len(lines):
    line = lines[i].rstrip('\n')

    # Skip empty lines at the top level
    if not line.strip():
        i += 1
        continue

    # Check if this is a question line (ends with comma, no number)
    if line.strip().endswith(',') and not re.search(r',\d+\s*$', line):
        question = line.rstrip(',').strip()
        i += 1

        # Skip blank line after question
        while i < len(lines) and not lines[i].strip():
            i += 1

        # Collect answer lines until we hit one ending with ,N
        answer_parts = []
        while i < len(lines):
            answer_line = lines[i].rstrip('\n')

            # Check if this has message_id at the end (pattern: ,number)
            if re.search(r',\d+\s*$', answer_line):
                # This is the last line of the answer
                # Extract message_id
                match = re.match(r'^(.*),(\d+)\s*$', answer_line)
                if match:
                    answer_parts.append(match.group(1))
                    message_id = match.group(2).strip()

                    # Combine into one row
                    answer = '\n'.join(answer_parts)
                    combined = f'{question},{answer},{message_id}'
                    output.append(combined)
                    qa_count += 1
                    print(f"✓ Fixed QA pair {qa_count}")
                    i += 1
                    break
                else:
                    answer_parts.append(answer_line)
                    i += 1
            else:
                answer_parts.append(answer_line)
                i += 1
    else:
        # This might be a standalone question-answer line already
        i += 1

# Write fixed file
with open('data/therapy_csvs/therapy-fin_FIXED.csv', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"\n✅ Fixed {qa_count} QA pairs")
print(f"📄 Saved to: data/therapy_csvs/therapy-fin_FIXED.csv")
print(f"\n💡 Upload therapy-fin_FIXED.csv to your app!")
