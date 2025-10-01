#!/usr/bin/env python3
"""
Convert therapy.md to clean CSV format.
Extracts Q&A pairs from markdown structure.
"""

import csv
import re

def parse_therapy_md(md_file, output_csv):
    """Parse therapy.md and create clean CSV"""

    print(f"📖 Reading: {md_file}")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by --- separator
    sections = content.split('---')

    qa_pairs = []
    current_question = None
    message_id = 1

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Check if this is a therapist question
        if section.startswith('**Therapist'):
            # Extract question text
            question = re.sub(r'\*\*Therapist\s*', '', section)
            question = question.replace('**', '').strip()
            current_question = question

        # Check if this is David's answer
        elif section.startswith('David'):
            if current_question:
                # Extract answer text
                answer = re.sub(r'^David\s*', '', section, flags=re.MULTILINE)
                answer = answer.strip()

                # Clean up: remove extra whitespace, keep single spaces
                answer = ' '.join(answer.split())
                question_clean = ' '.join(current_question.split())

                qa_pairs.append({
                    'Therapist': question_clean,
                    'Client': answer,
                    'message_id': message_id
                })

                message_id += 1
                current_question = None

    print(f"✓ Extracted {len(qa_pairs)} QA pairs")

    # Write to CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Therapist', 'Client', 'message_id'])
        writer.writeheader()
        writer.writerows(qa_pairs)

    print(f"✅ Saved to: {output_csv}")
    print(f"📊 {len(qa_pairs)} complete QA pairs ready to use")
    print(f"\n💡 Upload {output_csv.split('/')[-1]} to your app!")

if __name__ == "__main__":
    input_md = "data/therapy_csvs/therapy.md"
    output_csv = "data/therapy_csvs/therapy_WORKING.csv"

    parse_therapy_md(input_md, output_csv)
