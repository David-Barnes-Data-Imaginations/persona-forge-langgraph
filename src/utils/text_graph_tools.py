
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
        output_dir = os.path.join(os.getcwd(), "output", "cypher_queries")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graph_import_{timestamp}.cypher"
        
        # Ensure .cypher extension
        if not filename.endswith('.cypher'):
            filename += '.cypher'
        
        # Full path
        filepath = os.path.join(output_dir, filename)
        
        # Write the cypher file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cypher_data)
        
        return f"Cypher query successfully saved to: {filepath}"
    
    except Exception as e:
        return f"Error saving Cypher query: {str(e)}"