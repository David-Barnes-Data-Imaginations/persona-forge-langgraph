#!/usr/bin/env python3
"""
Fix newline escape sequences in Cypher files that break Neo4j syntax.
Replaces \\n with semicolons in plan/assessment text fields.
"""

import re
import sys

def fix_cypher_file(input_file, output_file):
    """Fix newline escape sequences in Cypher file"""

    print(f"📖 Reading: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace \n with semicolon+space in text fields
    # This regex finds strings containing \n and replaces them
    def replace_newlines(match):
        text = match.group(0)
        # Replace \n with ; (semicolon)
        fixed = text.replace('\\n', '; ')
        return fixed

    # Fix newlines in string literals (between single quotes)
    fixed_content = re.sub(r"'[^']*\\n[^']*'", replace_newlines, content)

    print(f"✅ Fixed newline escape sequences")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

    print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    import glob

    # Find the most recent Cypher file
    cypher_files = glob.glob("output/psychological_analysis/graph_output/psychological_graph_*.cypher")

    if not cypher_files:
        print("❌ No Cypher files found!")
        sys.exit(1)

    # Get the most recent
    latest = max(cypher_files, key=lambda x: x)

    output = latest.replace('.cypher', '_FIXED.cypher')

    fix_cypher_file(latest, output)

    print(f"\n💡 Use {output} for Neo4j import!")
