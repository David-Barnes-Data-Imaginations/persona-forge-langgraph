#!/usr/bin/env python3
"""
Parse therapy.md using ^ as the end-of-QA-pair marker
"""

import csv

def parse_with_caret(md_file, output_csv):
    """Parse markdown with ^ markers"""

    print(f"📖 Reading: {md_file}")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by ^ character (each QA pair ends with ^)
    qa_blocks = [block.strip() for block in content.split('^') if block.strip()]

    qa_pairs = []

    for i, block in enumerate(qa_blocks):
        # Split by --- to separate Therapist and Client sections
        sections = [s.strip() for s in block.split('---') if s.strip()]

        question = None
        answer = None

        for section in sections:
            if section.startswith('Therapist'):
                # Extract question (everything after "Therapist")
                lines = section.split('\n', 1)
                if len(lines) > 1:
                    question = lines[1].strip()
                else:
                    question = ""

            elif section.startswith('Client'):
                # Extract answer (everything after "Client")
                lines = section.split('\n', 1)
                if len(lines) > 1:
                    answer = lines[1].strip()
                else:
                    answer = ""

        # Clean whitespace
        if question and answer:
            question_clean = ' '.join(question.split())
            answer_clean = ' '.join(answer.split())

            qa_id = f"{i+1:03d}"  # Format as 001, 002, etc.

            qa_pairs.append({
                'Therapist': question_clean,
                'Client': answer_clean,
                'qa_id': qa_id
            })

    print(f"✓ Extracted {len(qa_pairs)} QA pairs")

    # Write CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Therapist', 'Client', 'qa_id'])
        writer.writeheader()
        writer.writerows(qa_pairs)

    print(f"✅ Saved to: {output_csv}")
    print(f"📊 {len(qa_pairs)} QA pairs ready")
    print(f"\n💡 Upload {output_csv.split('/')[-1]}")

if __name__ == "__main__":
    parse_with_caret(
        "data/therapy_csvs/therapy.md",
        "data/therapy_csvs/therapy_WORKING.csv"
    )
