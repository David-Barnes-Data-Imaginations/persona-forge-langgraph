# Deep Agent Workflow Guide

## Overview

The Deep Agent workflow is a terminal-based psychological analysis system that uses an orchestrated multi-agent architecture to generate comprehensive progress notes from therapy session data stored in a Neo4j knowledge graph.

## Architecture

### The Architect (Main Agent)
- **Model**: `gpt-oss:20b` (14GB VRAM)
- **Role**: Oversees the entire workflow, delegates tasks to sub-agents, and produces the final report
- **Tools**: File operations, todo management, task delegation

### Sub-Agents

#### 1. Graph Agent (Overseer)
- **Model**: `gpt-oss:20b` (14GB VRAM)
- **Role**: Analyzes psychological patterns in the knowledge graph
- **Tools**:
  - `get_graph_statistics` - Get overall statistics (top emotions, distortions, schemas, etc.)
  - `get_extreme_values` - Find QA pairs with highest/lowest psychological property values
  - `get_qa_pair_details` - Retrieve complete analysis for a specific QA pair
  - `search_psychological_insights` - Semantic search through therapy session chunks

#### 2. Graph Assistant (Scribe)
- **Model**: `qwen3:4b`
- **Role**: Executes individual graph queries and extractions
- **Tools**: Same as Graph Agent

#### 3. Graph Assistant 2 (Peon)
- **Model**: `qwen3:4b`
- **Role**: Executes individual graph queries and extractions
- **Tools**: Same as Graph Agent

#### 4. Research Agent (Overseer)
- **Model**: `gpt-oss:20b` (14GB VRAM)
- **Role**: Conducts research on psychological topics and recent studies
- **Tools**:
  - `pubmed_search` - Search academic literature for peer-reviewed research
  - `tavily_search` - General web search for current information
  - File operations

#### 5. Research Assistant (Peon)
- **Model**: `qwen34b`
- **Role**: Handles individual research queries
- **Tools**: PubMed search, Tavily web search

#### 6. Research Assistant 2 (Scribe)
- **Model**: `granite3.3:8b`
- **Role**: Handles individual research queries
- **Tools**: PubMed search, Tavily web search

#### 7. Report Writer (Scribe)
- **Model**: `granite3.3:8b`
- **Role**: Generates progress notes in SOAP format
- **Tools**: File operations, todo management

## Workflow Steps

### 1. Graph Analysis Phase
The Architect delegates to the Graph Agent to:

1. Query total number of QA pairs in the session
2. Get statistical overview:
   - Top 5 most common emotions (with avg valence/arousal)
   - Top 5 cognitive distortions
   - Top 5 core schemas
   - Attachment style distribution
   - Top 5 defense mechanisms
   - Big Five personality averages

3. Identify extreme values for key metrics:
   - Highest emotion valence (most positive moments)
   - Lowest emotion valence (most negative moments)
   - Highest arousal (most intense moments)
   - Extreme Big Five traits (high neuroticism, low extraversion, etc.)

4. Retrieve full details for clinically significant QA pairs

### 2. Report Writing Phase
The Report Writer uses the analyzed data to create progress notes following the SOAP format:

- **Subjective**: Client's emotional state, key concerns expressed
- **Objective**: Observable patterns from psychological analysis
- **Assessment**: Clinical interpretation of patterns and themes
- **Plan**: Recommendations for treatment and interventions

### 3. Research Enhancement Phase
The Research Agent supplements the report with:

- Recent studies relevant to identified patterns
- Evidence-based interventions for the client's presentation
- Clinical guidelines for observed schemas/distortions

### 4. Final Review
The Architect reviews and edits the complete report before presenting to the user.

## New Graph RAG Tools

### `get_graph_statistics(session_id: str)`
Returns aggregated statistics across all QA pairs in a session:
- Total QA pairs count
- Emotion frequency and average valence/arousal
- Most common cognitive distortions
- Core schemas frequency
- Attachment style distribution
- Defense mechanism usage
- Big Five personality profile

**Use Case**: Get a bird's-eye view of the client's psychological patterns before diving into specifics.

### `get_extreme_values(property_type: str, session_id: str, limit: int)`
Finds QA pairs with the most extreme values for a property:

**Property Types**:
- `emotion_valence` - Most positive/negative emotional moments
- `emotion_arousal` - Most/least intense moments
- `neuroticism`, `openness`, `conscientiousness`, `extraversion`, `agreeableness` - Big Five extremes

**Returns**: QA pair IDs, property values, confidence scores, and text samples

**Use Case**: Identify clinically significant moments that warrant deeper analysis.

### `get_qa_pair_details(qa_pair_id: str)`
Retrieves complete psychological analysis for a specific QA pair:
- All detected emotions with valence/arousal/confidence
- All cognitive distortions
- Schemas, attachment styles, defense mechanisms
- Big Five personality scores
- Full text of the client's response

**Use Case**: Deep dive into a specific moment identified as significant.

### `search_psychological_insights(query: str, max_results: int)`
Semantic search through text chunks with psychological context:
- Searches embeddings for relevant content
- Returns text chunks with their psychological annotations
- Includes session and QA pair context

**Use Case**: Find moments related to specific themes ("abandonment", "anger", "relationship conflict")

## Research Tools

### `pubmed_search(query: str, max_results: int, recent_only: bool)`
Search PubMed's academic database for peer-reviewed research articles:
- Queries the PubMed E-utilities API
- Retrieves full article metadata (title, authors, abstract, journal, DOI, publication date)
- Saves articles as markdown files with proper citations
- Default filters to 2020+ for recent studies (can be disabled)
- Returns summaries with filenames for agent to read full details

**Arguments**:
- `query` - Search terms (e.g., "schema therapy emotional inhibition")
- `max_results` - Number of articles to retrieve (default: 5)
- `recent_only` - If True, only returns studies from 2020 onwards (default: True)

**Perfect for**:
- Finding evidence-based interventions
- Recent meta-analyses and systematic reviews
- Clinical research on specific psychological conditions
- Treatment effectiveness studies

**Example Usage by Agent**:
```
Research Agent: "I'll search PubMed for recent studies on emotional inhibition schema"
[Calls pubmed_search("schema therapy emotional inhibition", max_results=5, recent_only=True)]
[Returns]: 📚 Found 5 articles (2020-present)
1. Schema Therapy for Emotional Inhibition: A Meta-Analysis (2023)
2. Effectiveness of Schema-Focused Interventions... (2022)
...
Files saved: pubmed_Schema_Therapy_for_abc123.md, ...

Research Agent: "Let me read the first article for details"
[Calls read_file("pubmed_Schema_Therapy_for_abc123.md")]
[Incorporates findings into research summary]
```

**Use Case**: Supplement clinical reports with current peer-reviewed research and evidence-based recommendations.

### `tavily_search(query: str, max_results: int, topic: str)`
General web search for current information:
- Searches the web for recent articles and information
- Converts HTML to markdown for easier reading
- Summarizes webpage content using AI
- Best for non-academic, current information

**Use Case**: Find clinical guidelines, treatment resources, or general mental health information not in academic journals.

## Terminal UI Features

### Launch
```bash
python run_deep_agent.py
```

### Commands

| Command | Description |
|---------|-------------|
| `/help` | Show comprehensive help |
| `/stats` | Display graph statistics for current session |
| `/session <id>` | Change active session (default: session_001) |
| `/clear` | Clear conversation history |
| `/exit` | Exit the application |

### Natural Language Interactions

You can interact naturally with the Architect:

- "Start the psychological analysis workflow for session_001"
- "What are the most common emotions in this session?"
- "Show me the QA pairs with the highest neuroticism scores"
- "Generate the progress notes report"
- "Research recent studies on emotional inhibition schema"

### Human-in-the-Loop File Operations

When agents request file operations (creating reports, etc.), you'll see a confirmation panel:

```
┌─ File Operation Request ─────────────────────┐
│ Operation:      CREATE                        │
│ File Path:      output/progress_notes.md     │
│ Absolute Path:  /full/path/to/file           │
└───────────────────────────────────────────────┘
Do you want to proceed? [y/N]
```

## Example Workflow Session

```
You: Start the analysis for session_001

Agent: I'll begin the psychological analysis workflow.

[Agent calls get_graph_statistics]
[Displays statistics panel]

Agent: I've found 47 QA pairs in this session. The most common patterns are:
- Emotions: Anxiety (12), Shame (8), Anger (7)
- Schemas: Emotional Inhibition (9), Defectiveness/Shame (7)
- Attachment: Anxious Preoccupied (15)

I'll now identify the most clinically significant moments...

[Agent calls get_extreme_values for high neuroticism]
[Agent calls get_qa_pair_details for significant pairs]

Agent: I've identified 5 key moments. Now delegating to the Report Writer...

[Report Writer generates SOAP notes]

Agent: The progress notes are ready. Would you like me to save them to a file?

You: Yes

[Human-in-the-loop confirmation appears]
[File is created]

Agent: Report saved. Would you like me to research recent interventions for emotional inhibition?
```

## Improved Workflow Efficiency

### Before (Old Approach)
- Graph Agent read all QA pairs sequentially (47 reads for 47 pairs)
- Massive file I/O overhead
- Difficult to identify patterns
- No aggregation or statistical analysis

### After (New Approach)
- Single query for overall statistics
- Targeted queries for extreme values (3-5 QA pairs)
- Deep dive only on clinically significant moments
- Uses graph structure and embeddings efficiently

**Result**: ~90% reduction in queries, focused analysis on what matters clinically.

## VRAM Usage

The models are sized to fit on a single 4090 (24GB):
- Architect: 14GB (only runs when others are idle)
- Overseer: 2.4GB (can run concurrently)
- Peon: 2.4GB (can run concurrently)
- Scribe: Variable (based on available memory)

**Design Note**: The Architect and Overseer models never run concurrently, allowing the same 14GB allocation to be shared.

## Progress Notes Output Format

```markdown
# Progress Notes for Client_ID: client_001
Date: 2025-09-30

## Subjective
[1-3 paragraphs describing the client's emotional state,
key concerns expressed, and self-reported experiences]

## Objective
[1-3 paragraphs describing observable patterns from the
psychological analysis: dominant emotions, cognitive distortions,
schemas, and personality presentation]

## Assessment
[1-3 paragraphs providing clinical interpretation of the
patterns, themes, and their significance for treatment]

## Plan
[1-3 paragraphs outlining recommendations for interventions,
therapeutic approaches, and treatment goals]

## Research of Recent Studies
[1-3 paragraphs summarizing relevant recent research and
evidence-based practices for the client's presentation]
```

## Troubleshooting

### Agent Not Initializing
- Check that Neo4j is running (`bolt://localhost:7687`)
- Verify Ollama is running and models are pulled
- Check that required models are available: `ollama list`

### Graph Queries Failing
- Verify session_id exists in the graph
- Check Neo4j connection credentials in `hybrid_rag_tools.py`
- Ensure vector index exists: `CREATE VECTOR INDEX textchunk_embedding_index ...`

### Terminal UI Issues
- Ensure Rich is installed: `pip install rich>=2.0.0`
- Check terminal supports UTF-8 and colors
- Try running with `TERM=xterm-256color python run_deep_agent.py`

## Future Enhancements

- [ ] Add real-time progress indicators for long-running queries
- [ ] Implement session comparison ("compare session_001 with session_002")
- [ ] Add visualization of emotional patterns over time
- [ ] Export reports in multiple formats (PDF, HTML, JSON)
- [ ] Add configurable report templates
- [ ] Implement parallel sub-agent execution for faster analysis

## Contributing

This is a portfolio/demo project for the NHS mental health hospital. Feedback and suggestions are welcome!

---

**Created by**: David Barnes
**Purpose**: Mental health technology demonstration
**Stack**: Python, LangGraph, Neo4j, Ollama, Rich