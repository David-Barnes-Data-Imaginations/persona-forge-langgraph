#!/usr/bin/env python3
"""
Persona-Forge RAG Tool for Chat Agent Integration
Provides psychological context retrieval as a tool for LLM conversations
"""

from langchain_core.tools import tool
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
from src.utils.embeddings import embed_texts
import json


# Global RAG instance (initialize once, use many times)
_rag_instance = None


def get_rag_instance():
    """Get or create the global RAG instance"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = PersonaForgeRAGTool(
            neo4j_uri="bolt://localhost:7687",
            neo4j_user="neo4j",
            neo4j_password="!"  # You might want to use env vars for this
        )
    return _rag_instance


class PersonaForgeRAGTool:
    """Core RAG functionality for tool integration"""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        if self.driver:
            self.driver.close()

    def search_psychological_context(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for psychological context using hybrid vector + graph search
        """
        # Generate query embedding using your Ollama setup
        query_embedding = embed_texts([query])[0]

        cypher = """
        CALL db.index.vector.queryNodes('textchunk_embedding_index', $k, $query_embedding)
        YIELD node, score

        // Get comprehensive psychological context
        MATCH (node:TextChunk)
        OPTIONAL MATCH (node)-[:REVEALS_EMOTION]->(e:Emotion)
        OPTIONAL MATCH (node)-[:EXHIBITS_DISTORTION]->(d:Cognitive_Distortion)
        OPTIONAL MATCH (node)-[:REVEALS_ATTACHMENT_STYLE]->(a:Attachment_Style)
        OPTIONAL MATCH (node)-[:REVEALS_SCHEMA]->(s:Schema)
        OPTIONAL MATCH (node)-[:USES_DEFENSE_MECHANISM]->(m:Defense_Mechanism)
        OPTIONAL MATCH (node)-[:EXHIBITS_STAGE]->(es:Erikson_Stage)

        // Get parent QA and session context
        OPTIONAL MATCH (qa:QA_Pair)-[:HAS_CHUNK]->(node)
        OPTIONAL MATCH (session:Session)-[:INCLUDES_CHUNK]->(node)

        // Get QA-level psychological analysis
        OPTIONAL MATCH (qa)-[:REVEALS_EMOTION]->(qa_emotion:Emotion)
        OPTIONAL MATCH (qa)-[:EXHIBITS_DISTORTION]->(qa_distortion:Cognitive_Distortion)
        OPTIONAL MATCH (qa)-[:REVEALS_ATTACHMENT_STYLE]->(qa_attachment:Attachment_Style)
        OPTIONAL MATCH (qa)-[:SHOWS_BIG_FIVE]->(big5:Big_Five)

        RETURN 
            node.id as chunk_id,
            node.text as text,
            score,
            node.valence as valence,
            node.arousal as arousal,
            node.confidence as confidence,

            // Chunk-level psychology
            collect(DISTINCT e.name) as chunk_emotions,
            collect(DISTINCT d.type) as chunk_distortions,
            collect(DISTINCT a.name) as chunk_attachment_styles,
            collect(DISTINCT s.name) as chunk_schemas,
            collect(DISTINCT m.name) as chunk_defense_mechanisms,
            collect(DISTINCT es.name) as chunk_erikson_stages,

            // QA-level psychology  
            qa.id as qa_pair_id,
            session.session_id as session_id,
            collect(DISTINCT qa_emotion.name) as qa_emotions,
            collect(DISTINCT qa_distortion.type) as qa_distortions,
            collect(DISTINCT qa_attachment.name) as qa_attachment_styles,

            // Big Five personality
            big5.openness as openness,
            big5.conscientiousness as conscientiousness,
            big5.extraversion as extraversion,
            big5.agreeableness as agreeableness,
            big5.neuroticism as neuroticism

        ORDER BY score DESC
        """

        with self.driver.session() as session:
            try:
                results = session.run(cypher, k=k, query_embedding=query_embedding)
                return [dict(record) for record in results]
            except Exception as e:
                print(f"❌ RAG search error: {e}")
                return []


@tool
def search_psychological_insights(query: str, max_results: int = 3) -> str:
    """
    Search the psychological knowledge graph for insights related to the user's query.

    This tool searches through analyzed therapy session text chunks using both semantic similarity
    and psychological framework connections (emotions, cognitive distortions, attachment styles, etc.).

    Args:
        query: The search query to find relevant psychological context
        max_results: Maximum number of results to return (default: 3)

    Returns:
        Formatted psychological context including text chunks, emotional states,
        cognitive patterns, and personality insights
    """
    rag = get_rag_instance()

    try:
        # Perform the hybrid search
        search_results = rag.search_psychological_context(query, k=max_results)

        if not search_results:
            return f"No psychological insights found for query: '{query}'"

        # Format the results for the LLM
        context_parts = [f"=== PSYCHOLOGICAL INSIGHTS FOR: '{query}' ===\n"]

        for i, result in enumerate(search_results, 1):
            # Build psychological profile summary
            chunk_psychology = []
            if result['chunk_emotions']:
                chunk_psychology.append(f"Emotions: {', '.join(result['chunk_emotions'])}")
            if result['chunk_distortions']:
                chunk_psychology.append(f"Cognitive Distortions: {', '.join(result['chunk_distortions'])}")
            if result['chunk_attachment_styles']:
                chunk_psychology.append(f"Attachment: {', '.join(result['chunk_attachment_styles'])}")
            if result['chunk_schemas']:
                chunk_psychology.append(f"Core Schemas: {', '.join(result['chunk_schemas'])}")
            if result['chunk_defense_mechanisms']:
                chunk_psychology.append(f"Defense Mechanisms: {', '.join(result['chunk_defense_mechanisms'])}")

            # QA-level context
            qa_psychology = []
            if result['qa_emotions']:
                qa_psychology.append(f"QA Emotions: {', '.join(result['qa_emotions'])}")
            if result['qa_distortions']:
                qa_psychology.append(f"QA Distortions: {', '.join(result['qa_distortions'])}")

            # Big Five if available
            big_five = []
            if result['openness'] is not None:
                big_five.append(f"Openness: {result['openness']:.1f}")
            if result['conscientiousness'] is not None:
                big_five.append(f"Conscientiousness: {result['conscientiousness']:.1f}")
            if result['extraversion'] is not None:
                big_five.append(f"Extraversion: {result['extraversion']:.1f}")
            if result['neuroticism'] is not None:
                big_five.append(f"Neuroticism: {result['neuroticism']:.1f}")

            context_part = f"""
INSIGHT {i} (Relevance: {result['score']:.3f}):
Text: "{result['text']}"

Chunk Psychology: {' | '.join(chunk_psychology) if chunk_psychology else 'None detected'}
QA Psychology: {' | '.join(qa_psychology) if qa_psychology else 'None detected'}
Big Five Traits: {' | '.join(big_five) if big_five else 'Not available'}
Emotional State: Valence={result['valence']}, Arousal={result['arousal']}
Source: {result['session_id']} → {result['qa_pair_id']}

{'-' * 60}"""

            context_parts.append(context_part)

        return "\n".join(context_parts)

    except Exception as e:
        return f"Error searching psychological insights: {str(e)}"


@tool
def get_personality_summary(focus_area: str = "overall") -> str:
    """
    Get a summary of personality traits and psychological patterns.

    Args:
        focus_area: Area to focus on - 'overall', 'emotions', 'cognition', 'attachment', or 'personality'

    Returns:
        Summary of psychological patterns and personality insights
    """
    rag = get_rag_instance()

    # Use a broad search to get general personality patterns
    if focus_area == "overall":
        query = "personality emotions attachment cognitive patterns"
    elif focus_area == "emotions":
        query = "emotional patterns feelings empathy mood"
    elif focus_area == "cognition":
        query = "thinking patterns cognitive distortions mental processing"
    elif focus_area == "attachment":
        query = "relationships attachment style interpersonal"
    elif focus_area == "personality":
        query = "personality traits big five characteristics"
    else:
        query = focus_area

    try:
        results = rag.search_psychological_context(query, k=5)

        if not results:
            return f"No personality data available for focus area: {focus_area}"

        # Aggregate patterns across results
        all_emotions = []
        all_distortions = []
        all_attachments = []
        all_schemas = []
        big_five_data = {}

        for result in results:
            all_emotions.extend(result['chunk_emotions'] or [])
            all_distortions.extend(result['chunk_distortions'] or [])
            all_attachments.extend(result['chunk_attachment_styles'] or [])
            all_schemas.extend(result['chunk_schemas'] or [])

            # Collect Big Five data
            if result['openness'] is not None:
                big_five_data['openness'] = result['openness']
            if result['conscientiousness'] is not None:
                big_five_data['conscientiousness'] = result['conscientiousness']
            if result['extraversion'] is not None:
                big_five_data['extraversion'] = result['extraversion']
            if result['neuroticism'] is not None:
                big_five_data['neuroticism'] = result['neuroticism']

        # Create summary
        summary_parts = [f"=== PERSONALITY SUMMARY: {focus_area.upper()} ===\n"]

        if all_emotions:
            dominant_emotions = list(set(all_emotions))
            summary_parts.append(f"Dominant Emotions: {', '.join(dominant_emotions)}")

        if all_distortions:
            key_distortions = list(set(all_distortions))
            summary_parts.append(f"Cognitive Patterns: {', '.join(key_distortions)}")

        if all_attachments:
            attachment_styles = list(set(all_attachments))
            summary_parts.append(f"Attachment Style: {', '.join(attachment_styles)}")

        if all_schemas:
            core_schemas = list(set(all_schemas))
            summary_parts.append(f"Core Schemas: {', '.join(core_schemas)}")

        if big_five_data:
            big_five_summary = []
            for trait, score in big_five_data.items():
                level = "High" if score > 0.7 else "Moderate" if score > 0.4 else "Low"
                big_five_summary.append(f"{trait.title()}: {level} ({score:.1f})")
            summary_parts.append(f"Big Five Profile: {' | '.join(big_five_summary)}")

        return "\n".join(summary_parts)

    except Exception as e:
        return f"Error generating personality summary: {str(e)}"


# Tool list for import to chat_agents tools
PERSONA_FORGE_TOOLS = [
    search_psychological_insights,
    get_personality_summary
]


# Cleanup function
def cleanup_rag_connection():
    """Call this when shutting down your application"""
    global _rag_instance
    if _rag_instance:
        _rag_instance.close()
        _rag_instance = None