#!/usr/bin/env python3
"""
Quick test script for the updated get_personality_summary tool
"""

from src.tools.hybrid_rag_tools import get_personality_summary

print("Testing get_personality_summary with different focus areas:\n")
print("=" * 80)

# Test 1: Overall summary
print("\n1. OVERALL SUMMARY:")
print("-" * 80)
result = get_personality_summary.invoke({"focus_area": "overall", "session_id": "session_001"})
print(result)

# Test 2: Emotions only
print("\n\n2. EMOTIONS FOCUS:")
print("-" * 80)
result = get_personality_summary.invoke({"focus_area": "emotions", "session_id": "session_001"})
print(result)

# Test 3: Personality/Big Five
print("\n\n3. PERSONALITY (BIG FIVE) FOCUS:")
print("-" * 80)
result = get_personality_summary.invoke({"focus_area": "personality", "session_id": "session_001"})
print(result)

# Test 4: Attachment styles
print("\n\n4. ATTACHMENT FOCUS:")
print("-" * 80)
result = get_personality_summary.invoke({"focus_area": "attachment", "session_id": "session_001"})
print(result)

# Test 5: Cognition
print("\n\n5. COGNITION FOCUS:")
print("-" * 80)
result = get_personality_summary.invoke({"focus_area": "cognition", "session_id": "session_001"})
print(result)

print("\n\n" + "=" * 80)
print("Tests complete!")
