#!/usr/bin/env python3
"""
Regenerate framework analysis for a specific message_id from the CSV file.
This allows fixing individual entries that had errors in the framework_analysis workflow.

Usage:
    python3 regenerate_framework_analysis.py <message_id>

Example:
    python3 regenerate_framework_analysis.py 3
"""

import sys
import os
import csv
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.graphs.framework_analysis import process_qa_pair


def find_qa_pair_by_message_id(message_id: str) -> dict:
    """Find the QA pair from the CSV file by message_id."""
    # Find the CSV file (look for therapy_WORKING.csv or similar)
    csv_candidates = [
        # "data/therapy_csvs/therapy_WORKING.csv",
        "data/therapy_csvs/therapy_WORKING.csv",
    ]

    csv_path = None
    for candidate in csv_candidates:
        if os.path.exists(candidate):
            csv_path = candidate
            break

    if not csv_path:
        raise FileNotFoundError(
            "Could not find therapy CSV file. Checked: " + ", ".join(csv_candidates)
        )

    print(f"📂 Reading CSV: {csv_path}")

    # Read CSV using standard library
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV file is empty")

    # Check columns
    headers = rows[0].keys()
    if "message_id" in headers:
        id_col = "message_id"
    elif "qa_id" in headers:
        id_col = "qa_id"
    else:
        raise ValueError("CSV must have either 'message_id' or 'qa_id' column")

    # Convert message_id to zero-padded format (001, 002, etc.)
    try:
        target_id_padded = str(int(message_id)).zfill(3)
    except ValueError:
        # Maybe it's already in format like "001"
        target_id_padded = message_id

    # Find the row - CSV has format like "001", "002"
    matching_row = None
    for row in rows:
        if row[id_col] == target_id_padded:
            matching_row = row
            break

    if not matching_row:
        available_ids = [row[id_col] for row in rows[:10]]  # Show first 10
        raise ValueError(
            f"Message ID '{message_id}' not found in CSV. Available IDs (first 10): {available_ids}"
        )

    # Extract question and answer
    # Check column names (might be Therapist/Client or Question/Answer)
    if "Therapist" in headers and "Client" in headers:
        question = matching_row["Therapist"]
        answer = matching_row["Client"]
    elif "Question" in headers and "Answer" in headers:
        question = matching_row["Question"]
        answer = matching_row["Answer"]
    else:
        raise ValueError(
            "CSV must have either Therapist/Client or Question/Answer columns"
        )

    return {"message_id": target_id_padded, "question": question, "answer": answer}


def regenerate_framework_analysis(message_id: str):
    """Regenerate framework analysis for a specific message_id."""
    print(f"\n🔍 Searching for message_id {message_id} in CSV...\n")

    # Find the QA pair
    try:
        qa_data = find_qa_pair_by_message_id(message_id)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    print(f"✅ Found QA pair:")
    print(f"   Message ID: {qa_data['message_id']}")
    print(f"   Question: {qa_data['question'][:100]}...")
    print(f"   Answer: {qa_data['answer'][:100]}...")
    print()

    # Run framework analysis workflow
    print(f"🤖 Running framework analysis workflow...\n")

    try:
        # Use the process_qa_pair function directly
        result = process_qa_pair(qa_data)

        if result.get("status") == "success":
            print(f"\n✅ Framework analysis completed!")
            print(f"   QA ID: {result.get('qa_id')}")
            print(
                f"   Check the master file at: output/psychological_analysis/psychological_analysis_master.txt"
            )
            print(f"   The new analysis has been appended to the file.")
        else:
            print(f"\n⚠️  Analysis completed with warnings:")
            print(f"   {result.get('error', 'Unknown issue')}")

    except Exception as e:
        print(f"❌ Error running framework analysis: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 regenerate_framework_analysis.py <message_id>")
        print("Example: python3 regenerate_framework_analysis.py 3")
        sys.exit(1)

    message_id = sys.argv[1]
    regenerate_framework_analysis(message_id)
