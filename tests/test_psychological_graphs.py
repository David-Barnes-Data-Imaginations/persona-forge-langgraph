#!/usr/bin/env python3
"""
Test script for the /psychological_graphs endpoint (without HTTP server)
"""

import json
from src.tools.hybrid_rag_tools import get_objective_statistics, get_extreme_values
import re


def test_psychological_graphs(session_id="session_001"):
    """
    Test the psychological graphs data parsing logic
    """

    # Get the raw statistics
    stats_result = get_objective_statistics.invoke({"session_id": session_id})

    # Initialize response structure
    graph_data = {
        "emotions": [],
        "personality": {},
        "statistics": {
            "emotions": {"categories": [], "values": []},
            "distortions": {"categories": [], "values": []},
            "schemas": {"categories": [], "values": []},
            "attachments": {"categories": [], "values": []},
            "defenses": {"categories": [], "values": []}
        },
        "extreme_values": {},
        "session_id": session_id
    }

    # Parse the text output from get_objective_statistics
    lines = stats_result.split('\n')

    current_section = None

    for line in lines:
        line = line.strip()

        # Detect sections
        if line.startswith("Top 5 Emotions:"):
            current_section = "emotions"
            continue
        elif line.startswith("Top 5 Cognitive Distortions:"):
            current_section = "distortions"
            continue
        elif line.startswith("Top 5 Core Schemas:"):
            current_section = "schemas"
            continue
        elif line.startswith("Attachment Styles:"):
            current_section = "attachments"
            continue
        elif line.startswith("Top 5 Defense Mechanisms:"):
            current_section = "defenses"
            continue
        elif line.startswith("Big Five Personality Averages:"):
            current_section = "personality"
            continue

        # Parse emotion data (with valence and arousal)
        if current_section == "emotions" and line.startswith("-"):
            # Format: "- Sadness: 10 occurrences (avg valence: -0.54, avg arousal: 0.39)"
            match = re.search(r'-\s+([^:]+):\s+(\d+)\s+occurrences\s+\(avg valence:\s+([-\d.]+),\s+avg arousal:\s+([-\d.]+)\)', line)
            if match:
                emotion_name = match.group(1).strip()
                count = int(match.group(2))
                valence = float(match.group(3))
                arousal = float(match.group(4))

                graph_data["emotions"].append({
                    "name": emotion_name,
                    "valence": valence,
                    "arousal": arousal,
                    "confidence": min(count / 15.0, 1.0),
                    "count": count
                })

                graph_data["statistics"]["emotions"]["categories"].append(emotion_name)
                graph_data["statistics"]["emotions"]["values"].append(count)

        # Parse distortions
        elif current_section == "distortions" and line.startswith("-"):
            match = re.search(r'-\s+([^:]+):\s+(\d+)\s+occurrences', line)
            if match:
                name = match.group(1).strip()
                count = int(match.group(2))
                graph_data["statistics"]["distortions"]["categories"].append(name)
                graph_data["statistics"]["distortions"]["values"].append(count)

        # Parse schemas
        elif current_section == "schemas" and line.startswith("-"):
            match = re.search(r'-\s+([^:]+):\s+(\d+)\s+occurrences', line)
            if match:
                name = match.group(1).strip()
                count = int(match.group(2))
                graph_data["statistics"]["schemas"]["categories"].append(name)
                graph_data["statistics"]["schemas"]["values"].append(count)

        # Parse attachments
        elif current_section == "attachments" and line.startswith("-"):
            match = re.search(r'-\s+([^:]+):\s+(\d+)\s+occurrences', line)
            if match:
                name = match.group(1).strip()
                count = int(match.group(2))
                graph_data["statistics"]["attachments"]["categories"].append(name)
                graph_data["statistics"]["attachments"]["values"].append(count)

        # Parse defenses
        elif current_section == "defenses" and line.startswith("-"):
            match = re.search(r'-\s+([^:]+):\s+(\d+)\s+occurrences', line)
            if match:
                name = match.group(1).strip()
                count = int(match.group(2))
                graph_data["statistics"]["defenses"]["categories"].append(name)
                graph_data["statistics"]["defenses"]["values"].append(count)

        # Parse Big Five personality
        elif current_section == "personality" and line.startswith("-"):
            # Format: "- Openness: 0.73 (High)"
            match = re.search(r'-\s+([^:]+):\s+([\d.]+)\s+\(([^)]+)\)', line)
            if match:
                trait = match.group(1).strip().lower()
                value = float(match.group(2))
                graph_data["personality"][trait] = value

    # Get extreme values for neuroticism
    try:
        extreme_neuroticism = get_extreme_values.invoke({
            "property_type": "neuroticism",
            "session_id": session_id,
            "limit": 3
        })
        graph_data["extreme_values"]["neuroticism"] = extreme_neuroticism
    except Exception as e:
        print(f"Error getting extreme values: {e}")
        graph_data["extreme_values"]["neuroticism"] = "No extreme value data available"

    return graph_data


if __name__ == "__main__":
    print("Testing /psychological_graphs endpoint logic...")
    print("=" * 80)

    result = test_psychological_graphs()

    print("✅ Successfully parsed graph data!\n")

    print(f"Session: {result['session_id']}")
    print(f"\n📊 EMOTIONS DATA (for valence-arousal scatter plot):")
    print(f"   Count: {len(result['emotions'])} emotions")
    if result['emotions']:
        print(f"   Sample: {result['emotions'][0]}")

    print(f"\n🌟 PERSONALITY DATA (for Big Five radar chart):")
    print(f"   Traits: {list(result['personality'].keys())}")
    print(f"   Values: {result['personality']}")

    print(f"\n📈 STATISTICS DATA (for bar charts):")
    for category, data in result['statistics'].items():
        if data['categories']:
            print(f"   {category.title()}: {len(data['categories'])} items")

    print(f"\n🎯 EXTREME VALUES:")
    if isinstance(result['extreme_values'].get('neuroticism'), str):
        print(f"   {result['extreme_values']['neuroticism'][:100]}...")
    else:
        print(f"   Available")

    print("\n" + "=" * 80)
    print("FULL JSON OUTPUT (formatted):")
    print("=" * 80)
    # Pretty print the JSON
    print(json.dumps(result, indent=2, default=str)[:2000] + "...")

    print("\n" + "=" * 80)
    print("Test complete!")
