## E2B Migration Guide for Deep Agent

### Overview

This guide explains how to migrate your deep agent workflow from a virtual filesystem to E2B sandboxes.

### Benefits of E2B

**Before (Virtual Filesystem):**
- ❌ Complex custom file tools (ls, read_file, write_file)
- ❌ Large prompts explaining virtual filesystem
- ❌ Limited to predefined file operations
- ❌ Hard to debug file state

**After (E2B Sandbox):**
- ✅ Agents use real Linux commands (they already know these!)
- ✅ Much simpler prompts
- ✅ Full bash/python execution capabilities
- ✅ Easy to inspect /workspace/ directory
- ✅ Persistent file storage

### Architecture

```
┌─────────────────────────────────────────┐
│  Your Host Machine                      │
│  - Neo4j running on localhost:7687      │
│  - Ollama models                        │
│  - Deep agent orchestration             │
└─────────────────────────────────────────┘
                   │
                   ├─> Controls
                   ↓
┌─────────────────────────────────────────┐
│  E2B Sandbox (Linux Container)          │
│  - /workspace/ directory                │
│  - Bash execution                       │
│  - Python execution                     │
│  - Connects to Neo4j on host           │
└─────────────────────────────────────────┘
```

### Neo4j Connection from E2B

**Yes, agents CAN query Neo4j from inside E2B!**

The Neo4j connection works because:
1. Neo4j runs on your HOST machine (localhost:7687)
2. E2B sandbox can connect to host network
3. RAG tools connect using the Neo4j Python driver

**Setup:**
```python
# In sandbox, set environment variables
sandbox.commands.run("export NEO4J_URI=bolt://host.docker.internal:7687")
sandbox.commands.run("export NEO4J_USER=neo4j")
sandbox.commands.run("export NEO4JP=your_password")

# Install neo4j driver in sandbox
sandbox.commands.run("pip install neo4j")
```

**Note:** You may need to use `host.docker.internal` instead of `localhost` for the Neo4j URI when connecting from inside the sandbox.

### File Structure

Created files:
- **run_deep_agent_e2b.py** - E2B-enabled entry point
- **src/tools/e2b_tools.py** - Bash/Python execution tools
- **src/prompts/e2b_prompts.py** - Simplified prompts

### Tool Comparison

| Virtual Filesystem | E2B Sandbox |
|-------------------|-------------|
| `ls()` | `execute_bash("ls -la /workspace/")` |
| `read_file("file.txt")` | `execute_bash("cat /workspace/file.txt")` |
| `write_file("file.txt", content)` | `execute_bash("echo 'content' > /workspace/file.txt")` |
| `save_to_disk("file.txt")` | Files already persisted in /workspace/ |

### Agent Tool List (E2B Version)

**Architect:**
- Delegation tools (3)
- E2B execution (execute_bash, execute_python)
- File operations (read_sandbox_file, write_sandbox_file, list_workspace_files)
- TODO management (write_todos, read_todos)
- Think tool

**Assistants:**
- All RAG tools (9) - these query Neo4j from HOST
- Research tools (tavily_search, pubmed_search)
- E2B execution (execute_bash, execute_python)
- File operations
- TODO management

### Implementation Steps

#### 1. Install E2B

```bash
pip install e2b-code-interpreter
```

#### 2. Get E2B API Key

```bash
# Visit https://e2b.dev/
# Create account and get API key
export E2B_API_KEY="your_key_here"
```

#### 3. Update deep_agent.py for E2B

Replace virtual filesystem tools with E2B tools:

```python
from ..tools.e2b_tools import E2B_TOOLS

# OLD:
# built_in_tools = [ls, read_file, write_file, save_to_disk, ...]

# NEW:
built_in_tools = E2B_TOOLS + [write_todos, read_todos, think_tool]
```

#### 4. Modify Agent Initialization

Pass sandbox to agent state:

```python
def get_new_deep_agent_e2b(
    config,
    short_term_memory,
    long_term_memory,
    sandbox  # Add sandbox parameter
):
    # ... existing code ...

    # Add sandbox to initial state
    deep_agent = create_react_agent(
        model,
        tools,
        prompt=E2B_ARCHITECT_INSTRUCTIONS,  # Use E2B prompts
        checkpointer=short_term_memory,
        store=long_term_memory,
        state_schema=DeepAgentState,
    )

    return deep_agent
```

#### 5. Run E2B Version

```bash
python run_deep_agent_e2b.py
```

### Simplified Prompts

E2B prompts are **much shorter** because agents already know Linux:

**Before:**
```
FILE_USAGE_INSTRUCTIONS = """Virtual Filesystem Management...
[200 lines explaining how to use custom file tools]
"""
```

**After:**
```
E2B_INSTRUCTIONS = """You have a Linux sandbox.
Use execute_bash for file operations.
Files in /workspace/ persist between calls.
"""
```

### Debugging

**Check sandbox state:**
```python
# In your code:
result = sandbox.commands.run("ls -la /workspace/")
print(result.stdout)
```

**View files:**
```python
content = sandbox.files.read("/workspace/report.txt")
print(content)
```

**Check Neo4j connection:**
```python
result = sandbox.commands.run("echo $NEO4J_URI")
print(result.stdout)
```

### Cost Considerations

E2B has usage costs:
- Free tier: 100 sandbox hours/month
- Paid: ~$0.20/hour per sandbox

For your workflow with 3 sub-agents, each workflow run might use:
- 1 shared sandbox
- ~5-10 minutes per workflow
- Cost: ~$0.02-0.03 per workflow

**Recommendation:** Use a single shared sandbox for all agents rather than one sandbox per agent.

### Migration Checklist

- [ ] Install e2b-code-interpreter
- [ ] Get E2B API key
- [ ] Update deep_agent.py to use E2B_TOOLS
- [ ] Replace prompts with E2B versions
- [ ] Update Neo4j URI to use host.docker.internal
- [ ] Test Neo4j connection from sandbox
- [ ] Test file operations in /workspace/
- [ ] Run workflow end-to-end
- [ ] Monitor E2B usage/costs

### Next Steps

1. Test the e2b setup with: `python run_deep_agent_e2b.py`
2. Monitor the first workflow run to ensure:
   - Neo4j queries work
   - Files save correctly to /workspace/
   - Agents can read each other's files
3. Adjust Neo4j URI if needed (may need host IP instead of host.docker.internal)
4. Celebrate simpler prompts! 🎉
