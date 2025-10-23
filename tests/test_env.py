#!/usr/bin/env python3
"""
Quick test to verify environment variables are loading correctly
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

print("=" * 70)
print("Environment Variables Test")
print("=" * 70)

# Test Neo4j variables
neo4j_vars = {
    "NEO4J_URI": os.getenv("NEO4J_URI"),
    "NEO4J_USER": os.getenv("NEO4J_USER"),
    "NEO4JP": os.getenv("NEO4JP"),
}

print("\n📊 Neo4j Configuration:")
for key, value in neo4j_vars.items():
    if value:
        # Mask password for display
        if "password" in key.lower() or key == "NEO4JP":
            masked = value[:2] + "*" * (len(value) - 4) + value[-2:] if len(value) > 4 else "****"
            print(f"  ✅ {key}: {masked}")
        else:
            print(f"  ✅ {key}: {value}")
    else:
        print(f"  ❌ {key}: NOT SET")

# Test other important variables
other_vars = {
    "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
    "OLLAMA_HOST": os.getenv("OLLAMA_HOST"),
    "OLLAMA_EMBED_MODEL": os.getenv("OLLAMA_EMBED_MODEL"),
}

print("\n🔧 Other Configuration:")
for key, value in other_vars.items():
    if value:
        # Mask API keys
        if "key" in key.lower() or "token" in key.lower():
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "****"
            print(f"  ✅ {key}: {masked}")
        else:
            print(f"  ✅ {key}: {value}")
    else:
        print(f"  ❌ {key}: NOT SET")

# Check if Neo4j password is set
print("\n" + "=" * 70)
if neo4j_vars["NEO4JP"]:
    print("✅ Environment variables loaded successfully!")
    print("   Your Neo4j password is properly configured from .env file")
else:
    print("❌ NEO4JP not found in environment!")
    print("   Make sure your .env file contains: NEO4JP=\"your_password\"")

print("=" * 70)