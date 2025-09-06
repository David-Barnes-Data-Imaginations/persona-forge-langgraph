
import json
import os
from datetime import datetime
from langchain_core.tools import tool

@tool
def submit_analysis(analysis_data: str, filename: str = None) -> str:
    """
    Submit psychological analysis data. This tool writes the analysis to a file as text.
    
    Args:
        analysis_data: The psychological analysis as a text string
        filename: Optional filename. If not provided, uses timestamp-based name
    
    Returns:
        String confirmation with the filename where data was saved
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output", "psychological_analysis")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"psychological_analysis_{timestamp}.txt"
        
        # Ensure .txt extension for text analysis
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Full path
        filepath = os.path.join(output_dir, filename)
        
        # Write the analysis as plain text
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(analysis_data))
        
        return f"Analysis successfully saved to: {filepath}"
    
    except Exception as e:
        return f"Error saving analysis: {str(e)}"

@tool 
def submit_cypher(cypher_data: str, filename: str = None) -> str:
    """
    Submit Cypher query data for graph database import.
    
    Args:
        cypher_data: The Cypher query string
        filename: Optional filename. If not provided, uses timestamp-based name
    
    Returns:
        String confirmation with the filename where data was saved
    """
    try:
        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output", "cypher_queries")
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename if not provided
        if filename is None:
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