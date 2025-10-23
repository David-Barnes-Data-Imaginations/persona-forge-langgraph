#!/usr/bin/env python3
"""
Anonymize therapy CSV by rewriting client answers using Gemini.
This rewrites client responses to tell a different story while maintaining
the same psychological patterns, making it safe for GitHub/demos.

Usage:
    # Process single QA pair
    python3 anonymize_therapy_csv.py --message-id 1

    # Process all QA pairs
    python3 anonymize_therapy_csv.py --all

    # Process range of QA pairs
    python3 anonymize_therapy_csv.py --start 1 --end 10

The script will:
- Read from data/therapy_csvs/therapy_WORKING.csv
- Send client answers to Gemini for rewriting
- Save to data/therapy_csvs/therapy_anonymized.csv
- Keep therapist questions unchanged
- Shorten overly long responses
- Remove references to real people/places
"""

import sys
import os
import csv
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai


def get_gemini_model():
    """Initialize Gemini model using direct Google API."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)

    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config={
            "temperature": 0.7,
            "max_output_tokens": 2048,
        }
    )


def anonymize_client_answer(therapist_question: str, client_answer: str, model) -> str:
    """
    Use Gemini to rewrite the client answer with a different story
    while maintaining the same psychological patterns.
    """

    prompt = f"""You are helping to anonymize a therapy transcript for demo purposes.

THERAPIST QUESTION:
{therapist_question}

ORIGINAL CLIENT ANSWER:
{client_answer}

TASK:
Rewrite the client's answer to tell a DIFFERENT story while preserving the EXACT SAME psychological patterns, emotions, cognitive distortions, and attachment styles present in the original.

REQUIREMENTS:
1. Change all specific people, places, events, and personal details
2. Create a fictional but realistic scenario that demonstrates the same psychological issues
3. Keep the same emotional tone and intensity
4. Maintain the same defense mechanisms, cognitive distortions, and coping strategies
5. If the original is overly long (>300 words), condense it to 150-250 words while keeping key psychological content
6. Make it sound natural and conversational, like a real therapy session
7. Remove any references to specific occupations, assessments, or identifiable details

IMPORTANT: The psychological profile should remain identical - only the surface story changes.

REWRITTEN CLIENT ANSWER (respond with ONLY the rewritten answer, no preamble):"""

    response = model.generate_content(prompt)
    return response.text.strip()


def read_therapy_csv(csv_path: str) -> list:
    """Read therapy CSV and return list of rows."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV file is empty")

    return rows


def write_therapy_csv(csv_path: str, rows: list, headers: list):
    """Write therapy CSV."""
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Saved anonymized CSV to: {csv_path}")


def load_existing_anonymized_csv(output_path: str) -> dict:
    """Load existing anonymized CSV to resume from where we left off."""
    if not os.path.exists(output_path):
        return {}

    with open(output_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing = {row["message_id"]: row for row in reader}

    return existing


def anonymize_therapy_csv(
    input_csv: str = "data/therapy_csvs/therapy_WORKING.csv",
    output_csv: str = "data/therapy_csvs/therapy_anonymized.csv",
    message_id: str = None,
    process_all: bool = False,
    start_id: int = None,
    end_id: int = None,
):
    """
    Anonymize therapy CSV by rewriting client answers.

    Args:
        input_csv: Path to input CSV
        output_csv: Path to output CSV
        message_id: Single message ID to process
        process_all: Process all rows
        start_id: Start message ID for range
        end_id: End message ID for range
    """

    print(f"📂 Reading input CSV: {input_csv}")
    rows = read_therapy_csv(input_csv)
    headers = ["Therapist", "Client", "message_id"]

    # Load existing anonymized data (to resume if interrupted)
    existing_anonymized = load_existing_anonymized_csv(output_csv)

    # Initialize Gemini
    print("🤖 Initializing Gemini model...")
    model = get_gemini_model()

    # Determine which rows to process
    if message_id:
        # Single message
        target_id = str(int(message_id)).zfill(3)
        rows_to_process = [r for r in rows if r["message_id"] == target_id]
        if not rows_to_process:
            print(f"❌ Message ID {message_id} not found")
            return
    elif start_id and end_id:
        # Range of messages
        start = str(int(start_id)).zfill(3)
        end = str(int(end_id)).zfill(3)
        rows_to_process = [r for r in rows if start <= r["message_id"] <= end]
    elif process_all:
        # All messages
        rows_to_process = rows
    else:
        print("❌ Must specify --message-id, --all, or --start/--end")
        return

    print(f"\n📝 Processing {len(rows_to_process)} QA pairs...\n")

    # Create output rows (start with existing or empty)
    output_rows = []
    processed_ids = set()

    # Add existing anonymized rows first
    for row in rows:
        msg_id = row["message_id"]
        if msg_id in existing_anonymized:
            output_rows.append(existing_anonymized[msg_id])
            processed_ids.add(msg_id)

    # Process new rows
    for i, row in enumerate(rows_to_process, 1):
        msg_id = row["message_id"]

        # Skip if already processed
        if msg_id in processed_ids:
            print(f"⏭️  Skipping {msg_id} (already anonymized)")
            continue

        therapist_q = row["Therapist"]
        client_a = row["Client"]

        print(f"🔄 Processing {msg_id} ({i}/{len(rows_to_process)})")
        print(f"   Original length: {len(client_a)} chars")

        try:
            # Anonymize the client answer
            anonymized_answer = anonymize_client_answer(therapist_q, client_a, model)

            print(f"   Anonymized length: {len(anonymized_answer)} chars")
            print(f"   ✅ Anonymized successfully")

            # Create new row
            new_row = {
                "Therapist": therapist_q,  # Keep question unchanged
                "Client": anonymized_answer,  # Rewritten answer
                "message_id": msg_id,
            }

            # Update output rows
            output_rows.append(new_row)
            processed_ids.add(msg_id)

            # Save after each successful anonymization (in case of interruption)
            write_therapy_csv(output_csv, output_rows, headers)

        except Exception as e:
            print(f"   ❌ Error: {e}")
            print(f"   Skipping {msg_id}")
            continue

        print()

    print(f"\n🎉 Anonymization complete!")
    print(f"   Processed: {len(processed_ids)} QA pairs")
    print(f"   Output: {output_csv}")


def main():
    parser = argparse.ArgumentParser(
        description="Anonymize therapy CSV using Gemini to rewrite client answers"
    )
    parser.add_argument(
        "--message-id",
        type=str,
        help="Single message ID to process (e.g., 1 or 001)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all QA pairs in the CSV",
    )
    parser.add_argument(
        "--start",
        type=int,
        help="Start message ID for range processing",
    )
    parser.add_argument(
        "--end",
        type=int,
        help="End message ID for range processing",
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/therapy_csvs/therapy_WORKING.csv",
        help="Input CSV path (default: data/therapy_csvs/therapy_WORKING.csv)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/therapy_csvs/therapy_anonymized.csv",
        help="Output CSV path (default: data/therapy_csvs/therapy_anonymized.csv)",
    )

    args = parser.parse_args()

    # Validate arguments
    if not (args.message_id or args.all or (args.start and args.end)):
        parser.print_help()
        print("\n❌ Error: Must specify --message-id, --all, or --start/--end")
        sys.exit(1)

    anonymize_therapy_csv(
        input_csv=args.input,
        output_csv=args.output,
        message_id=args.message_id,
        process_all=args.all,
        start_id=args.start,
        end_id=args.end,
    )


if __name__ == "__main__":
    main()
