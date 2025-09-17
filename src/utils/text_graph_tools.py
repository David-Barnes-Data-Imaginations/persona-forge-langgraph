
import json
import os
from datetime import datetime
from langchain_core.tools import tool
import io, json, re, csv, hashlib
from typing import Dict, Any, List, Tuple

@tool
def submit_analysis(analysis_data: str) -> str:
    """
    Submit psychological analysis data. This tool appends the analysis to a single master file.

    Args:
        analysis_data: The psychological analysis as a text string

    Returns:
        String confirmation with entry number and filename
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output", "psychological_analysis")
        os.makedirs(output_dir, exist_ok=True)

        # Single master file
        filepath = os.path.join(output_dir, "psychological_analysis_master.txt")

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append to the master file with separator
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"ANALYSIS ENTRY - {timestamp}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(str(analysis_data))
            f.write(f"\n\n{'=' * 80}\n")

        # Count entries by counting separators
        with open(filepath, 'r', encoding='utf-8') as f:
            entry_count = f.read().count("ANALYSIS ENTRY")

        return f"Analysis #{entry_count} successfully appended to: {filepath}"

    except Exception as e:
        return f"Error saving analysis: {str(e)}"

@tool 
def submit_cypher(cypher_data: str) -> str:
    """
    Submit Cypher query data for graph database import.
    
    Args:
        cypher_data: The Cypher query string.
        filename: Optional filename. If not provided, uses timestamp-based name
    
    Returns:
        String confirmation with the filename where data was saved
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output", "psychological_analysis", "graph_output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Single master Cypher file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"psychological_graph_{timestamp[:8]}.cypher"  # Use date only for filename
        filepath = os.path.join(output_dir, filename)
        
        # Get current timestamp for entry
        entry_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append to the master Cypher file with separator
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n// ============================================================================\n")
            f.write(f"// CYPHER ENTRY - {entry_timestamp}\n")
            f.write(f"// ============================================================================\n\n")
            f.write(str(cypher_data))
            f.write(f"\n\n// ============================================================================\n")
        
        # Count entries by counting separators
        with open(filepath, 'r', encoding='utf-8') as f:
            entry_count = f.read().count("CYPHER ENTRY")
        
        return f"Cypher query #{entry_count} successfully appended to: {filepath}"
    
    except Exception as e:
        return f"Error saving Cypher query: {str(e)}"

@tool
def submit_chunk(analysis_data: str) -> str:
    """
    ! Notes for Claude:
    ---
    Submit chunk to be embedded later.
    Output format like this i 'think':
    ```MANIFEST-TSV
    chunk_id	session_id	qa_id	source	framework_tags	valence	arousal	confidence	timestamp	text
    s001.q001.v1	session_001	qa_pair_001	therapy.md	Emotion:Empathy|Attachment:Anxious_preoccupied	0.2	0.3	0.8	2025-09-13T15:52:46Z	If I’m with someone who’s happy, I feel happy...
    ... other rows
    ```
    The rows should be:
    chunk_id (deterministic, e.g., session.qaid.v1 or hash)

    session_id

    qa_id

    source (e.g., therapy.md)

    framework_tags (pipe-delimited list, e.g., Emotion:Empathy|Attachment:Anxious_preoccupied)

    valence (float)

    arousal (float)

    confidence (float)

    timestamp (ISO 8601)

    text (free text; TSV handles tabs/quotes better than CSV)

    An example of the output from the 'submit_analysis tool (which is the human-readable equivalent of the chunk)':
    Analysis:

        Valence and Arousal:
        Empathy: valence 0.2, arousal 0.3, confidence 0.8
        Evidence: "If I’m with someone who’s happy, I feel happy. If I’m with someone sad, I feel sad."
        Anger visualization: valence 0.5, arousal 0.7, confidence 0.7
        Evidence: "I will typically visualise something that would make me angry, as it ‘feels’ like it gives me extra strength."
        Sadness when others sad: valence -0.4, arousal 0.4, confidence 0.7
        Evidence: "If I’m with someone sad, I feel sad."

        Cognitive Distortions:
        Rationalization, confidence 0.7
        Evidence: "I do often use ‘creative visualisation’ to simulate emotions if it's going to serve a purpose."

        Erikson Developmental Stage:
        Identity vs role confusion, confidence 0.7
        Evidence: "I don’t remember ever sitting around feeling sorry for myself, likewise I don’t sit around feeling joy about myself."

        Attachment Style:
        Anxious preoccupied, confidence 0.7
        Evidence: "I feel emotions through others, reflecting their feelings, or my perception of their feelings."

        Defense Mechanisms:
        Denial, confidence 0.6
        Evidence: "I literally never remember even seeing them."
        Intellectualization, confidence 0.6
        Evidence: "I do often use ‘creative visualisation’ to simulate emotions if it's going to serve a purpose."

        Schema Therapy:
        Emotional deprivation, confidence 0.7
        Evidence: "I don’t remember ever sitting around feeling sorry for myself, likewise I don’t sit around feeling joy about myself."

        Big Five Personality Traits:
        Openness 0.8, Conscientiousness 0.6, Extraversion 0.4, Agreeableness 0.5, Neuroticism 0.5
        Overall confidence 0.7

        Summary: The client reports a predominantly other‑oriented emotional experience with minimal self‑directed affect. They employ creative visualization to generate emotions for functional purposes, suggesting a rationalization defense. The pattern indicates possible identity confusion and emotional deprivation schemas, with an anxious preoccupied attachment style. Personality assessment shows high openness and moderate conscientiousness, low extraversion, and moderate neuroticism, aligning with a reflective, internally focused individual who may benefit from interventions targeting self‑affect awareness and emotional integration.

    ---

    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output", "chunks_for_embedding") # i need it to add a directory with the date as its title
        os.makedirs(output_dir, exist_ok=True)

        # Single master file
        filepath = os.path.join(output_dir, "psychological_analysis_master.txt")

        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append to the master file with separator
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"ANALYSIS ENTRY - {timestamp}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(str(analysis_data))
            f.write(f"\n\n{'=' * 80}\n")

        # Count entries by counting separators
        with open(filepath, 'r', encoding='utf-8') as f:
            entry_count = f.read().count("ANALYSIS ENTRY")

        return f"Analysis #{entry_count} successfully appended to: {filepath}"

    except Exception as e:
        return f"Error saving analysis: {str(e)}"



# ! Below here is for converting the TSV into JSONL or whichever is best for embedding chunks
TSV_BLOCK_PATTERN = re.compile(
    r"```MANIFEST-TSV\s+(?P<body>.+?)\s+```",
    flags=re.DOTALL | re.IGNORECASE,
)

REQUIRED_FIELDS = [
    "chunk_id","session_id","qa_id","source",
    "framework_tags","valence","arousal","confidence","timestamp","text"
]

def parse_manifest_tsv(llm_output: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Extracts the MANIFEST-TSV fenced block, parses rows, validates per-row,
    and returns (good_rows, bad_rows). Never raises on content errors.
    """
    m = TSV_BLOCK_PATTERN.search(llm_output)
    if not m:
        # No block found -> treat as single fatal row for logging, but don't loop the LLM
        return [], [{"error": "No MANIFEST-TSV block found"}]

    tsv = m.group("body").strip("\n\r\t ")
    # Normalize BOM and newlines
    tsv = tsv.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")

    reader = csv.DictReader(io.StringIO(tsv), delimiter="\t")
    good, bad = [], []

    # quick header check
    header = reader.fieldnames or []
    missing = [f for f in REQUIRED_FIELDS if f not in header]
    if missing:
        bad.append({"error": f"Missing required columns: {missing}", "header": header})
        return [], bad

    for i, row in enumerate(reader, 1):
        try:
            # Trim whitespace
            for k, v in list(row.items()):
                if isinstance(v, str):
                    row[k] = v.strip()

            # Coerce numeric fields
            for k in ("valence","arousal","confidence"):
                row[k] = float(row[k]) if row[k] != "" else None

            # Split tags
            row["framework_tags"] = [t for t in row["framework_tags"].split("|") if t]

            # Auto-fill chunk_id if blank (optional)
            if not row["chunk_id"]:
                base = f'{row["session_id"]}:{row["qa_id"]}:{row["text"][:64]}'
                row["chunk_id"] = "auto_" + hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]

            # Minimal validations
            if not row["text"]:
                raise ValueError("empty text")
            if row["valence"] is not None and not (-1.0 <= row["valence"] <= 1.0):
                raise ValueError("valence out of range [-1,1]")
            if row["arousal"] is not None and not (0.0 <= row["arousal"] <= 1.0):
                raise ValueError("arousal out of range [0,1]")

            good.append(row)
        except Exception as e:
            bad.append({"row_index": i, "error": str(e), "row": row})

    return good, bad

def save_jsonl(path: str, rows: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")