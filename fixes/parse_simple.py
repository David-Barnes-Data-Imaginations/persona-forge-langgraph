#!/usr/bin/env python3
"""
Simple parser for cleaned therapy.md format:
Therapist
Question

---

Client
Answer

---
"""

import csv

def parse_simple_format(md_file, output_csv):
    """Parse simple markdown format"""

    print(f"📖 Reading: {md_file}")

    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by ---
    sections = [s.strip() for s in content.split('---') if s.strip()]

    qa_pairs = []
    i = 0
    message_id = 1

    while i < len(sections):
        section = sections[i]

        # Check if this section starts with "Therapist"
        if section.startswith('Therapist'):
            # Extract question (everything after "Therapist")
            lines = section.split('\n', 1)
            if len(lines) > 1:
                question = lines[1].strip()
            else:
                question = ""

            # Next section should be the answer starting with "Client"
            if i + 1 < len(sections):
                answer_section = sections[i + 1]

                if answer_section.startswith('Client'):
                    # Extract answer (everything after "Client")
                    lines = answer_section.split('\n', 1)
                    if len(lines) > 1:
                        answer = lines[1].strip()
                    else:
                        answer = ""

                    # Clean whitespace (collapse multiple spaces/newlines to single space)
                    question_clean = ' '.join(question.split())
                    answer_clean = ' '.join(answer.split())

                    if question_clean and answer_clean:
                        qa_pairs.append({
                            'Therapist': question_clean,
                            'Client': answer_clean,
                            'message_id': message_id
                        })
                        message_id += 1

                    i += 2  # Skip both Q and A
                else:
                    i += 1
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
    print(f"📊 {len(qa_pairs)} QA pairs ready")
    print(f"\n💡 Upload {output_csv.split('/')[-1]}")

if __name__ == "__main__":
    parse_simple_format(
        "data/therapy_csvs/therapy.md",
        "data/therapy_csvs/therapy_WORKING.csv"
    )
