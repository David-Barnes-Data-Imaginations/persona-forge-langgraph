#!/usr/bin/env python3
"""Quick test to verify master file parsing"""

from src.graphs.create_kg import extract_analyses_from_master_file

print("Testing master file parsing...\n")

analyses = extract_analyses_from_master_file()

print(f"\n✅ Successfully extracted {len(analyses)} analyses")

if analyses:
    print(f"\nFirst analysis preview:")
    first = analyses[0]
    print(f"  Entry number: {first['entry_number']}")
    print(f"  Question: {first['original_question'][:100]}...")
    print(f"  Answer: {first['original_answer'][:100]}...")
    print(f"  Subjective: {first.get('subjective_analysis', '')[:100]}...")
    print(f"  Has assessment: {bool(first.get('assessment'))}")
    print(f"  Has plan: {bool(first.get('plan'))}")
