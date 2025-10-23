#!/usr/bin/env python3
"""
Direct test of the plan.txt parsing logic (without HTTP server)
"""

import os
from datetime import datetime

def parse_plan_file():
    """Parse the plan.txt file - same logic as in ag_ui_backend.py"""

    # Path to the plan file
    plan_file = os.path.join(os.path.dirname(__file__), "output", "plan.txt")

    if not os.path.exists(plan_file):
        return {"error": "Plan file not found"}

    # Read the plan file
    with open(plan_file, "r", encoding="utf-8") as f:
        plan_content = f.read()

    # Parse the content into structured data
    sections = plan_content.split("\n\n")

    subjective_text = ""
    statistics_text = ""

    # Extract sections
    for i, section in enumerate(sections):
        if section.strip().startswith("Subjective"):
            # Get the next section as subjective content
            if i + 1 < len(sections):
                subjective_text = sections[i + 1].strip()
        elif section.strip().startswith("Statistics Summary"):
            # Get remaining text as statistics
            if i + 1 < len(sections):
                statistics_text = "\n".join(sections[i + 1:]).strip()

    # Parse statistics into structured thoughts
    thoughts = []
    thought_id = 1

    # Add subjective analysis as first thought
    if subjective_text:
        thoughts.append({
            "id": str(thought_id),
            "content": f"Subjective Analysis: {subjective_text}",
            "type": "observation",
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.9,
        })
        thought_id += 1

    # Parse statistics lines into thoughts
    if statistics_text:
        stat_lines = statistics_text.split("\n")
        i = 0
        while i < len(stat_lines):
            line = stat_lines[i]
            if line.strip() and ":" in line:
                # Parse each statistic line
                parts = line.split(":", 1)
                if len(parts) == 2:
                    category = parts[0].strip()
                    data = parts[1].strip()

                    # Check if this is "Personality" and the next line contains the actual data
                    if category == "Personality" and not data and i + 1 < len(stat_lines):
                        # Get the next line which has the personality data
                        data = stat_lines[i + 1].strip()
                        i += 1  # Skip the next line since we've already used it

                    if data:  # Only add if we have actual data
                        thoughts.append({
                            "id": str(thought_id),
                            "content": f"{category}: {data}",
                            "type": "analysis",
                            "timestamp": datetime.now().isoformat(),
                            "confidence": 0.85,
                        })
                        thought_id += 1
            i += 1

    # Create todos based on the analysis
    todos = [
        {
            "id": "1",
            "task": "Analyze emotional patterns from session data",
            "status": "completed",
            "priority": "high",
            "created_at": datetime.now().isoformat(),
        },
        {
            "id": "2",
            "task": "Identify cognitive distortions and schemas",
            "status": "completed",
            "priority": "high",
            "created_at": datetime.now().isoformat(),
        },
        {
            "id": "3",
            "task": "Assess personality traits and attachment styles",
            "status": "completed",
            "priority": "medium",
            "created_at": datetime.now().isoformat(),
        },
        {
            "id": "4",
            "task": "Generate comprehensive treatment plan",
            "status": "completed",
            "priority": "high",
            "created_at": datetime.now().isoformat(),
        },
    ]

    # Build the response
    state = {
        "current_task": "Deep psychological analysis completed",
        "status": "completed",
        "progress": 100,
        "todos": todos,
        "thoughts": thoughts,
        "raw_analysis": plan_content,
    }

    return state


if __name__ == "__main__":
    print("Testing plan.txt parser...")
    print("=" * 80)

    result = parse_plan_file()

    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print("✅ Successfully parsed plan.txt!\n")
        print(f"Status: {result['status']}")
        print(f"Current Task: {result['current_task']}")
        print(f"Progress: {result['progress']}%")
        print(f"\nNumber of Todos: {len(result['todos'])}")
        print(f"Number of Thoughts: {len(result['thoughts'])}")

        print("\n" + "=" * 80)
        print("TODOS:")
        print("-" * 80)
        for todo in result['todos']:
            print(f"  [{todo['status']}] {todo['task']} (Priority: {todo['priority']})")

        print("\n" + "=" * 80)
        print("THOUGHTS:")
        print("-" * 80)
        for thought in result['thoughts']:
            content_preview = thought['content'][:100] + "..." if len(thought['content']) > 100 else thought['content']
            print(f"  [{thought['type']}] {content_preview}")

        print("\n" + "=" * 80)
        print("RAW ANALYSIS:")
        print("-" * 80)
        print(result['raw_analysis'])

    print("\n" + "=" * 80)
    print("Test complete!")
