#!/usr/bin/env python3
"""
Test script for the updated deep_agent_endpoint
"""

import requests
import json

print("Testing the deep_agent endpoint...")
print("=" * 80)

# Test the endpoint
try:
    response = requests.post("http://localhost:8001/deep_agent")

    if response.status_code == 200:
        data = response.json()

        print("✅ Endpoint is working!\n")
        print(f"Status: {data.get('status')}")
        print(f"Current Task: {data.get('current_task')}")
        print(f"Progress: {data.get('progress')}%")
        print(f"\nNumber of Todos: {len(data.get('todos', []))}")
        print(f"Number of Thoughts: {len(data.get('thoughts', []))}")

        print("\n" + "=" * 80)
        print("TODOS:")
        print("-" * 80)
        for todo in data.get('todos', []):
            print(f"  [{todo['status']}] {todo['task']} (Priority: {todo['priority']})")

        print("\n" + "=" * 80)
        print("THOUGHTS:")
        print("-" * 80)
        for thought in data.get('thoughts', [])[:5]:  # Show first 5
            print(f"  [{thought['type']}] {thought['content'][:100]}...")

        if len(data.get('thoughts', [])) > 5:
            print(f"  ... and {len(data.get('thoughts', [])) - 5} more thoughts")

        print("\n" + "=" * 80)
        print("RAW ANALYSIS (first 300 chars):")
        print("-" * 80)
        raw = data.get('raw_analysis', '')
        print(raw[:300] + "..." if len(raw) > 300 else raw)

    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Error: Could not connect to the backend server.")
    print("Make sure the FastAPI server is running on http://localhost:8001")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("Test complete!")
