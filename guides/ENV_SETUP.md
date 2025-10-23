# Environment Variables Setup Guide

## Overview

This project uses environment variables to keep sensitive credentials secure and out of version control.

## Setup

### 1. Create Your .env File

If you don't have a `.env` file yet, copy the example:

```bash
cp .env.example .env
```

Then edit `.env` with your actual credentials.

### 2. Required Variables

#### Neo4j Database
```bash
NEO4J_URI="bolt://localhost:7687"     # Your Neo4j connection URI
NEO4J_USER="neo4j"                    # Your Neo4j username
NEO4JP="your_password_here"           # Your Neo4j password
```

**Note**: The password variable is named `NEO4JP` (not `NEO4J_PASSWORD`) to match your existing setup.

#### API Keys
```bash
TAVILY_API_KEY="your-tavily-key"      # For web search (research agent)
OPENAI_API_KEY="your-openai-key"      # If using OpenAI models
HUGGINGFACE_TOKEN="your-hf-token"     # For embeddings/models
```

#### Optional - LangSmith Tracing
```bash
LANGSMITH_API_KEY="your-key"
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT="your-project"
```

### 3. Verify Configuration

Test that your environment variables are loading correctly:

```bash
python3 test_env.py
```

You should see:
```
✅ Environment variables loaded successfully!
   Your Neo4j password is properly configured from .env file
```

## How It Works

### In Code

The project uses `python-dotenv` to automatically load variables from `.env`:

```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
password = os.getenv("NEO4JP")
```

### In hybrid_rag_tools.py

The Neo4j connection is configured like this:

```python
def get_rag_instance():
    global _rag_instance
    if _rag_instance is None:
        # Load from environment with fallbacks
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4JP")  # Your existing var name

        if not neo4j_password:
            raise ValueError("NEO4JP not set in .env file!")

        _rag_instance = PersonaForgeRAGTool(
            neo4j_uri=neo4j_uri,
            neo4j_user=neo4j_user,
            neo4j_password=neo4j_password
        )
    return _rag_instance
```

## Security Best Practices

### ✅ DO:
- Keep `.env` in `.gitignore` (already configured)
- Use `.env.example` for documentation (no secrets)
- Rotate credentials regularly
- Use strong passwords

### ❌ DON'T:
- Commit `.env` to version control
- Share your `.env` file
- Hard-code credentials in source files
- Use default/weak passwords

## Troubleshooting

### "NEO4JP environment variable not set"

**Problem**: The app can't find your Neo4j password.

**Solutions**:
1. Check `.env` file exists in project root
2. Verify the variable is named `NEO4JP` (not `NEO4J_PASSWORD`)
3. Make sure password is in quotes: `NEO4JP="your_password"`
4. Run `python3 test_env.py` to diagnose

### "Connection refused" or "Authentication failed"

**Problem**: Can't connect to Neo4j.

**Solutions**:
1. Verify Neo4j is running: `sudo systemctl status neo4j`
2. Check the URI is correct (default: `bolt://localhost:7687`)
3. Verify username/password are correct
4. Try connecting with Neo4j Browser to confirm credentials

### Environment variables not loading

**Problem**: Variables are `None` even though they're in `.env`.

**Solutions**:
1. Make sure you're running from the project root directory
2. Check `.env` file has no syntax errors
3. Verify `python-dotenv` is installed: `pip list | grep dotenv`
4. Make sure `load_dotenv()` is called before accessing variables

## Changing Neo4j Credentials

If you need to change your Neo4j password:

1. Update Neo4j password in Neo4j Browser or CLI
2. Update `.env` file:
   ```bash
   NEO4JP="your_new_password"
   ```
3. Restart your application
4. Verify with: `python3 test_env.py`

## Example .env File

Your `.env` should look like this:

```bash
# API Keys
OPENAI_API_KEY="sk-proj-..."
TAVILY_API_KEY="tvly-dev-..."
HUGGINGFACE_TOKEN="hf_..."

# Neo4j Database
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4JP="W00dpidge0n!"

# Ollama Configuration
OLLAMA_HOST="http://localhost:11434/api/embeddings"
OLLAMA_EMBED_MODEL="all-MiniLM-L6-v2"

# Optional: LangSmith
LANGSMITH_API_KEY="lsv2_..."
LANGSMITH_TRACING_V2=true
LANGSMITH_PROJECT="sentiment-suite"
```

## Files

- `.env` - Your actual credentials (NOT in git)
- `.env.example` - Template with no secrets (in git)
- `test_env.py` - Script to verify variables load correctly

## For Demo/Portfolio

When sharing this project:

1. ✅ Include `.env.example` (template)
2. ✅ Include this `ENV_SETUP.md` guide
3. ❌ Never include `.env` (actual secrets)
4. ✅ Mention in README: "Configure `.env` file (see ENV_SETUP.md)"

---

**Questions?** Just ask! This setup keeps your credentials secure while making the app easy to configure.