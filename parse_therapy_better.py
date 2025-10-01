#!/usr/bin/env python3
"""
Better parser for therapy.md that handles all edge cases
"""

import csv
import re

def parse_therapy_md_better(md_file, output_csv):
    """Parse therapy.md by splitting on --- and pairing Q&A"""

    print(f"📖 Reading: {md_file}")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace David with Client
    content = content.replace('David', 'Client')

    # Split by ---
    sections = [s.strip() for s in content.split('---') if s.strip()]

    qa_pairs = []
    i = 0
    message_id = 1

    while i < len(sections):
        section = sections[i]

        # Check if this is a therapist question
        if '**Therapist' in section or section.startswith('**Therapist'):
            # Extract question
            question = re.sub(r'\*\*Therapist:?\s*', '', section, flags=re.IGNORECASE)
            question = question.replace('**', '').strip()

            # Next section should be the answer
            if i + 1 < len(sections):
                answer_section = sections[i + 1]

                # Remove "Client" prefix if present
                answer = re.sub(r'^Client\s*', '', answer_section, flags=re.MULTILINE)
                answer = answer.strip()

                # Clean whitespace
                question_clean = ' '.join(question.split())
                answer_clean = ' '.join(answer.split())

                if question_clean and answer_clean:
                    qa_pairs.append({
                        'Therapist': question_clean,
                        'Client': answer_clean,
                        'message_id': message_id
                    })
                    message_id += 1

                i += 2  # Skip both question and answer
            else:
                i += 1
        else:
            i += 1

    print(f"✓ Extracted {len(qa_pairs)} QA pairs")

    # Write CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Therapist', 'Client', 'message_id'])
        writer.writeheader()
        writer.writerows(qa_pairs)

    print(f"✅ Saved to: {output_csv}")
    print(f"📊 {len(qa_pairs)} complete QA pairs ready")
    print(f"\n💡 Upload {output_csv.split('/')[-1]} to your app!")

    return len(qa_pairs)

if __name__ == "__main__":
    count = parse_therapy_md_better(
        "data/therapy_csvs/therapy.md",
        "data/therapy_csvs/therapy_WORKING.csv"
    )

    if count < 30:
        print(f"\n⚠️  Expected ~34 pairs but got {count}")
        print("Some Q&A pairs may be malformed in the markdown")
