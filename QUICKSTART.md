# Quick Start Guide - Deep Agent Workflow

## Prerequisites

1. **Neo4j Running**
   ```bash
   # Check if Neo4j is running
   sudo systemctl status neo4j
   # Or start it
   sudo systemctl start neo4j
   ```

2. **Ollama Running with Required Models**
   ```bash
   # Check Ollama is running
   ollama list

   # Pull required models if not already present
   ollama pull qwen2.5:3b        # For peon tasks
   ollama pull granite3.1:8b     # For scribe tasks
   ollama pull llama3.2:latest   # For overseer/architect tasks (or use your preferred 20B model)
   ```

3. **Python Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   ```

## Run the Deep Agent Terminal

```bash
python run_deep_agent.py
```

## Your First Analysis

Once the terminal loads, try these commands:

### 1. Check Session Statistics
```
/stats
```
This shows you the overall psychological patterns in the default session (session_001).

### 2. Start a Full Workflow
```
Start the psychological analysis and generate progress notes for session_001
```

The agent will:
1. Analyze the graph statistics
2. Identify extreme values (clinically significant moments)
3. Query details for those moments
4. Generate a SOAP format progress notes report
5. Ask if you want to research recent studies

### 3. Custom Queries

```
Show me the 3 QA pairs with the highest neuroticism scores

What are the most common cognitive distortions?

Find moments related to abandonment

Generate a report focusing on attachment patterns
```

## Common Commands

| What You Want | Command |
|---------------|---------|
| See statistics | `/stats` |
| Change session | `/session session_002` |
| Get help | `/help` |
| Clear history | `/clear` |
| Exit | `/exit` or Ctrl+D |

## Tips

- The terminal supports **markdown** in agent responses
- Use **Ctrl+C** to interrupt long-running operations
- File operations require **confirmation** (human-in-the-loop)
- The agent uses **streaming** responses for real-time feedback

## What You'll See

```
╔═══════════════════════════════════════════════╗
║  SENTIMENT SUITE - DEEP AGENT TERMINAL        ║
║  Psychological Analysis & Report Generation   ║
╚═══════════════════════════════════════════════╝

┌─ Quick Commands ──────────────────────────────┐
│ /help          Show available commands        │
│ /stats         Show graph statistics          │
│ /session <id>  Change session ID             │
│ /clear         Clear conversation history     │
│ /exit          Exit the application          │
└───────────────────────────────────────────────┘

Type your message or use /help for commands

You: /stats

┌─ Statistics for session_001 ──────────────────┐
│ === GRAPH STATISTICS FOR session_001 ===      │
│                                               │
│ Total QA Pairs: 47                           │
│                                               │
│ Top 5 Emotions:                              │
│   - Anxiety: 12 occurrences                  │
│   - Shame: 8 occurrences                     │
│   ...                                        │
└───────────────────────────────────────────────┘
```

## Workflow in Action

### Analysis Phase (~2-3 minutes)
- Architect queries graph statistics
- Identifies top patterns (emotions, distortions, schemas)
- Finds extreme values (most clinically significant moments)
- Delegates to Graph Agent for detailed extraction

### Report Generation (~1-2 minutes)
- Report Writer creates SOAP notes
- Subjective, Objective, Assessment, Plan sections
- Includes evidence from the graph

### Research Phase (Optional, ~2-3 minutes)
- Research Agent searches for recent studies
- Finds evidence-based interventions
- Supplements the report with current research

### Total Time: ~5-8 minutes for complete analysis

## Example Output

The final report will be structured as:

```markdown
# Progress Notes for Client_ID: client_001

## Subjective
The client presented with significant anxiety and shame...

## Objective
Analysis revealed consistent patterns of emotional inhibition
(9 occurrences) and defectiveness/shame schema (7 occurrences)...

## Assessment
The predominance of anxious-preoccupied attachment style
combined with emotional inhibition suggests...

## Plan
Recommend schema-focused therapy targeting emotional
inhibition and defectiveness/shame schemas...

## Research of Recent Studies
Recent meta-analyses support the effectiveness of schema
therapy for...
```

## Troubleshooting

**Issue**: "Agent not initialized"
- **Fix**: Check Neo4j and Ollama are running

**Issue**: "No data found for session"
- **Fix**: Use `/session session_001` to verify session ID

**Issue**: Terminal looks weird/broken
- **Fix**: `export TERM=xterm-256color` before running

**Issue**: Models running out of memory
- **Fix**: Close other applications, check `nvidia-smi`

## Need Help?

See [DEEP_AGENT_WORKFLOW.md](DEEP_AGENT_WORKFLOW.md) for the complete guide.

---

Happy analyzing! 🧠💙