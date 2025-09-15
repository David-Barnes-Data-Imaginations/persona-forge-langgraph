
import json
import os
from datetime import datetime
from langchain_core.tools import tool

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