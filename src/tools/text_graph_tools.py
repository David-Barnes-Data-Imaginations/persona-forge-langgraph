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
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"ANALYSIS ENTRY - {timestamp}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(str(analysis_data))
            f.write(f"\n\n{'=' * 80}\n")

        # Count entries by counting separators
        with open(filepath, "r", encoding="utf-8") as f:
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
        output_dir = os.path.join(
            os.getcwd(), "output", "psychological_analysis", "graph_output"
        )
        os.makedirs(output_dir, exist_ok=True)

        # Single master Cypher file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = (
            f"psychological_graph_{timestamp[:8]}.cypher"  # Use date only for filename
        )
        filepath = os.path.join(output_dir, filename)

        # Get current timestamp for entry
        entry_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append to the master Cypher file with separator
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(
                f"\n// ============================================================================\n"
            )
            f.write(f"// CYPHER ENTRY - {entry_timestamp}\n")
            f.write(
                f"// ============================================================================\n\n"
            )
            f.write(str(cypher_data))
            f.write(
                f"\n\n// ============================================================================\n"
            )

        # Count entries by counting separators
        with open(filepath, "r", encoding="utf-8") as f:
            entry_count = f.read().count("CYPHER ENTRY")

        return f"Cypher query #{entry_count} successfully appended to: {filepath}"

    except Exception as e:
        return f"Error saving Cypher query: {str(e)}"


@tool
def submit_chunk(analysis_data: str) -> str:
    """
    Submit chunk data in TSV format to be processed and embedded.

    Expected format:
    ```MANIFEST-TSV
    chunk_id	session_id	qa_id	timestamp	text
    s001.q001.c1	session_001	qa_pair_001 2025-09-13T15:52:46Z	If I'm with someone who's happy, I feel happy...
    ```
    Args:
        analysis_data: The TSV-formatted chunk data within MANIFEST-TSV blocks

    Returns:
        String confirmation with processing results
    """
    try:
        # Create output directories
        today_str = datetime.now().strftime("%Y%m%d")
        base_output_dir = os.path.join(os.getcwd(), "output", "chunks_for_embedding")
        dated_output_dir = os.path.join(base_output_dir, today_str)
        os.makedirs(dated_output_dir, exist_ok=True)

        # Parse the TSV data from the LLM output
        good_rows, bad_rows = parse_manifest_tsv(analysis_data)

        if bad_rows:
            error_details = "; ".join(
                [str(row.get("error", "Unknown error")) for row in bad_rows]
            )
            return f"Error parsing TSV data: {error_details}"

        if not good_rows:
            return "No valid chunk data found in the analysis"

        # Save raw TSV data first (for debugging/inspection)
        tsv_filepath = os.path.join(
            dated_output_dir, f"chunks_tsv_{datetime.now().strftime('%H%M%S')}.tsv"
        )
        with open(tsv_filepath, "w", encoding="utf-8", newline="") as f:
            if good_rows:
                writer = csv.DictWriter(f, fieldnames=REQUIRED_FIELDS, delimiter="\t")
                writer.writeheader()
                writer.writerows(good_rows)

        # Convert to JSONL format
        jsonl_filepath = os.path.join(
            dated_output_dir, f"chunks_jsonl_{datetime.now().strftime('%H%M%S')}.jsonl"
        )
        save_jsonl(jsonl_filepath, good_rows)

        # Create embeddings for the chunks
        from .embeddings import embed_texts

        # Extract text for embedding
        texts_to_embed = [row["text"] for row in good_rows]
        chunk_ids = [row["chunk_id"] for row in good_rows]

        # Generate embeddings
        embeddings = embed_texts(texts_to_embed)

        # Save embeddings with metadata
        embeddings_filepath = os.path.join(
            dated_output_dir, f"embeddings_{datetime.now().strftime('%H%M%S')}.jsonl"
        )
        embedding_records = []
        with open(embeddings_filepath, "w", encoding="utf-8") as f:
            for i, (chunk_data, embedding) in enumerate(zip(good_rows, embeddings)):
                embedding_record = {
                    **chunk_data,  # Include all original chunk metadata
                    "embedding": embedding,
                    "embedding_model": "embeddinggemma",  # Updated model name
                    "created_at": datetime.now().isoformat(),
                }
                embedding_records.append(embedding_record)
                f.write(json.dumps(embedding_record, ensure_ascii=False) + "\n")

        # Generate parameterized Cypher for TextChunk graph
        chunk_cypher, chunk_params = generate_chunk_cypher(good_rows)

        # Save Cypher query and parameters separately
        time_suffix = datetime.now().strftime("%H%M%S")
        chunk_cypher_filepath = os.path.join(
            dated_output_dir, f"chunk_graph_{time_suffix}.cypher"
        )
        chunk_params_filepath = os.path.join(
            dated_output_dir, f"chunk_params_{time_suffix}.json"
        )

        with open(chunk_cypher_filepath, "w", encoding="utf-8") as f:
            f.write(chunk_cypher)

        with open(chunk_params_filepath, "w", encoding="utf-8") as f:
            f.write(chunk_params)

        # Generate parameterized Cypher for embeddings
        embedding_cypher_data = [
            {"chunk_id": rec["chunk_id"], "embedding": rec["embedding"]}
            for rec in embedding_records
        ]
        embedding_cypher, embedding_params = generate_embedding_cypher(
            embedding_cypher_data
        )

        embedding_cypher_filepath = os.path.join(
            dated_output_dir, f"embedding_vectors_{time_suffix}.cypher"
        )
        embedding_params_filepath = os.path.join(
            dated_output_dir, f"embedding_params_{time_suffix}.json"
        )

        with open(embedding_cypher_filepath, "w", encoding="utf-8") as f:
            f.write(embedding_cypher)

        with open(embedding_params_filepath, "w", encoding="utf-8") as f:
            f.write(embedding_params)

        return f"Successfully processed {len(good_rows)} chunks. Files saved: TSV({tsv_filepath}), JSONL({jsonl_filepath}), Embeddings({embeddings_filepath}), ChunkCypher+Params({chunk_cypher_filepath}, {chunk_params_filepath}), EmbeddingCypher+Params({embedding_cypher_filepath}, {embedding_params_filepath})"

    except Exception as e:
        return f"Error processing chunks: {str(e)}"


# ! Below here is for converting the TSV into JSONL or whichever is best for embedding chunks
TSV_BLOCK_PATTERN = re.compile(
    r"```MANIFEST-TSV\s+(?P<body>.+?)\s+```",
    flags=re.DOTALL | re.IGNORECASE,
)

REQUIRED_FIELDS = ["chunk_id", "session_id", "qa_id", "timestamp", "text"]


def parse_manifest_tsv(
    llm_output: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
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
            for k in ("valence", "arousal", "confidence"):
                row[k] = float(row[k]) if row[k] != "" else None

            # Split tags
            row["framework_tags"] = [t for t in row["framework_tags"].split("|") if t]

            # Auto-fill chunk_id if blank (optional)
            if not row["chunk_id"]:
                base = f'{row["session_id"]}:{row["qa_id"]}:{row["text"][:64]}'
                row["chunk_id"] = (
                    "auto_" + hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
                )

            # Minimal validations
            if not row["text"]:
                raise ValueError("empty text")

            good.append(row)
        except Exception as e:
            bad.append({"row_index": i, "error": str(e), "row": row})

    return good, bad


def save_jsonl(path: str, rows: List[Dict[str, Any]]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def generate_chunk_cypher(rows: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Generate optimized, parameterized Cypher queries for TextChunk nodes and relationships.

    Args:
        rows: List of validated chunk dictionaries

    Returns:
        Tuple of (cypher_query, json_params) for parameterized execution
    """

    if not rows:
        return "// No chunk data to process", "{}"

    # Optimized, parameterized Cypher query - build without .format() to avoid brace conflicts
    cypher_query = f"""
// ============================================================================
// TEXT CHUNK NODES AND RELATIONSHIPS (Parameterized)
// ============================================================================

// -- TextChunk upsert + properties
UNWIND $rows AS c
MERGE (t:TextChunk {{id: c.chunk_id}})
SET t.text = c.text,
    t.timestamp = datetime(c.timestamp);

// -- Link to QA and Session (if present)
UNWIND $rows AS c
OPTIONAL MATCH (q:QA_Pair {{id: c.qa_id}})
OPTIONAL MATCH (s:Session {{session_id: c.session_id}})
WITH c, q, s
MATCH (t:TextChunk {{id: c.chunk_id}})
FOREACH (_ IN CASE WHEN q IS NULL THEN [] ELSE [1] END |
  MERGE (q)-[:HAS_CHUNK]->(t)
)
FOREACH (_ IN CASE WHEN s IS NULL THEN [] ELSE [1] END |
  MERGE (s)-[:INCLUDES_CHUNK]->(t)
);

// -- Expand tags to evidence edges
UNWIND $rows AS c
UNWIND c.framework_tags AS tag
WITH c, split(tag, ':') AS parts
WITH c, toLower(parts[0]) AS kind, toLower(parts[1]) AS name
MATCH (t:TextChunk {{id: c.chunk_id}})
"""

    return cypher_query.strip(), json.dumps(params, ensure_ascii=False, indent=2)


def generate_embedding_cypher(embeddings_data: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Generate parameterized Cypher to add embedding vectors to existing TextChunk nodes.

    Args:
        embeddings_data: List of dictionaries with chunk_id and embedding

    Returns:
        Tuple of (cypher_query, json_params) for parameterized execution
    """
    if not embeddings_data:
        return "// No embeddings to process", "{}"

    # Prepare embedding data with just chunk_id and embedding vector
    embed_rows = [
        {"chunk_id": item["chunk_id"], "embedding": item["embedding"]}
        for item in embeddings_data
    ]

    # Parameterized Cypher query
    cypher_query = f"""
// ============================================================================
// ADD EMBEDDING VECTORS TO TEXT CHUNKS (Parameterized)
// ============================================================================

UNWIND $embeddings AS e
MATCH (t:TextChunk {{id: e.chunk_id}})
SET t.embedding = e.embedding;

// ============================================================================
// Added embeddings to {len(embeddings_data)} TextChunk nodes
// ============================================================================
"""

    # Generate JSON parameters
    params = {"embeddings": embed_rows}

    return cypher_query.strip(), json.dumps(params, ensure_ascii=False, indent=2)
