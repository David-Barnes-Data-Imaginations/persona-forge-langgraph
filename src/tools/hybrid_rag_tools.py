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
            neo4j_password="W00dpidge0n!"  # You might want to use env vars for this
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

        // Get the TextChunk and its basic properties
        WITH node, score
        WHERE node:TextChunk

        // Get parent QA and session context
        OPTIONAL MATCH (qa:QA_Pair)-[:HAS_CHUNK]->(node)
        OPTIONAL MATCH (session:Session)-[:INCLUDES]->(qa)

        // Get QA-level psychological analysis (this is where the psychology lives)
        OPTIONAL MATCH (qa)-[:REVEALS_EMOTION]->(qa_emotion:Emotion)
        OPTIONAL MATCH (qa)-[:EXHIBITS_DISTORTION]->(qa_distortion:Cognitive_Distortion)  
        OPTIONAL MATCH (qa)-[:REVEALS_ATTACHMENT_STYLE]->(qa_attachment:Attachment_Style)
        OPTIONAL MATCH (qa)-[:REVEALS_SCHEMA]->(qa_schema:Schema)
        OPTIONAL MATCH (qa)-[:USES_DEFENSE_MECHANISM]->(qa_defense:Defense_Mechanism)
        OPTIONAL MATCH (qa)-[:EXHIBITS_STAGE]->(qa_stage:Erikson_Stage)
        OPTIONAL MATCH (qa)-[:SHOWS_BIG_FIVE]->(big5:Big_Five)

        // Get relationship properties for emotions (valence, arousal, confidence)
        OPTIONAL MATCH (qa)-[emo_rel:REVEALS_EMOTION]->(qa_emotion)
        OPTIONAL MATCH (qa)-[dist_rel:EXHIBITS_DISTORTION]->(qa_distortion)
        OPTIONAL MATCH (qa)-[att_rel:REVEALS_ATTACHMENT_STYLE]->(qa_attachment)
        OPTIONAL MATCH (qa)-[sch_rel:REVEALS_SCHEMA]->(qa_schema)
        OPTIONAL MATCH (qa)-[def_rel:USES_DEFENSE_MECHANISM]->(qa_defense)
        OPTIONAL MATCH (qa)-[stage_rel:EXHIBITS_STAGE]->(qa_stage)
        OPTIONAL MATCH (qa)-[big5_rel:SHOWS_BIG_FIVE]->(big5)

        RETURN 
            node.id as chunk_id,
            node.text as text,
            score,

            // QA and session context
            qa.id as qa_pair_id,
            session.session_id as session_id,

            // QA-level psychology with confidence scores
            collect(DISTINCT {
                name: qa_emotion.name, 
                valence: emo_rel.valence, 
                arousal: emo_rel.arousal, 
                confidence: emo_rel.confidence
            }) as emotions,

            collect(DISTINCT {
                type: qa_distortion.type, 
                confidence: dist_rel.confidence
            }) as distortions,

            collect(DISTINCT {
                name: qa_attachment.name, 
                confidence: att_rel.confidence
            }) as attachment_styles,

            collect(DISTINCT {
                name: qa_schema.name, 
                confidence: sch_rel.confidence
            }) as schemas,

            collect(DISTINCT {
                name: qa_defense.name, 
                confidence: def_rel.confidence
            }) as defense_mechanisms,

            collect(DISTINCT {
                name: qa_stage.name, 
                confidence: stage_rel.confidence
            }) as erikson_stages,

            // Big Five personality (single values)
            big5_rel.openness as openness,
            big5_rel.conscientiousness as conscientiousness,
            big5_rel.extraversion as extraversion,
            big5_rel.agreeableness as agreeableness,
            big5_rel.neuroticism as neuroticism,
            big5_rel.confidence as big5_confidence

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
            # Extract psychology data (filter out empty entries)
            emotions = [e for e in result['emotions'] if e['name']]
            distortions = [d for d in result['distortions'] if d['type']]
            attachments = [a for a in result['attachment_styles'] if a['name']]
            schemas = [s for s in result['schemas'] if s['name']]
            defenses = [d for d in result['defense_mechanisms'] if d['name']]
            stages = [s for s in result['erikson_stages'] if s['name']]

            # Build psychological profile summary
            psychology_parts = []

            if emotions:
                emotion_strs = [f"{e['name']} (v:{e['valence']:.1f}, a:{e['arousal']:.1f}, conf:{e['confidence']:.1f})"
                                for e in emotions]
                psychology_parts.append(f"Emotions: {', '.join(emotion_strs)}")

            if distortions:
                distortion_strs = [f"{d['type']} (conf:{d['confidence']:.1f})" for d in distortions]
                psychology_parts.append(f"Cognitive Distortions: {', '.join(distortion_strs)}")

            if attachments:
                attachment_strs = [f"{a['name']} (conf:{a['confidence']:.1f})" for a in attachments]
                psychology_parts.append(f"Attachment: {', '.join(attachment_strs)}")

            if schemas:
                schema_strs = [f"{s['name']} (conf:{s['confidence']:.1f})" for s in schemas]
                psychology_parts.append(f"Core Schemas: {', '.join(schema_strs)}")

            if defenses:
                defense_strs = [f"{d['name']} (conf:{d['confidence']:.1f})" for d in defenses]
                psychology_parts.append(f"Defense Mechanisms: {', '.join(defense_strs)}")

            if stages:
                stage_strs = [f"{s['name']} (conf:{s['confidence']:.1f})" for s in stages]
                psychology_parts.append(f"Erikson Stage: {', '.join(stage_strs)}")

            # Big Five if available
            big_five = []
            if result['openness'] is not None:
                big_five.append(f"Openness: {result['openness']:.1f}")
            if result['conscientiousness'] is not None:
                big_five.append(f"Conscientiousness: {result['conscientiousness']:.1f}")
            if result['extraversion'] is not None:
                big_five.append(f"Extraversion: {result['extraversion']:.1f}")
            if result['agreeableness'] is not None:
                big_five.append(f"Agreeableness: {result['agreeableness']:.1f}")
            if result['neuroticism'] is not None:
                big_five.append(f"Neuroticism: {result['neuroticism']:.1f}")

            context_part = f"""
INSIGHT {i} (Relevance: {result['score']:.3f}):
Text: "{result['text']}"

Psychology: {' | '.join(psychology_parts) if psychology_parts else 'None detected'}
Big Five: {' | '.join(big_five) if big_five else 'Not available'}
Source: {result['session_id']} → {result['qa_pair_id']} → {result['chunk_id']}

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
        all_defenses = []
        big_five_data = {}

        for result in results:
            # Extract names from the structured data
            all_emotions.extend([e['name'] for e in result['emotions'] if e['name']])
            all_distortions.extend([d['type'] for d in result['distortions'] if d['type']])
            all_attachments.extend([a['name'] for a in result['attachment_styles'] if a['name']])
            all_schemas.extend([s['name'] for s in result['schemas'] if s['name']])
            all_defenses.extend([d['name'] for d in result['defense_mechanisms'] if d['name']])

            # Collect Big Five data
            if result['openness'] is not None:
                big_five_data['openness'] = result['openness']
            if result['conscientiousness'] is not None:
                big_five_data['conscientiousness'] = result['conscientiousness']
            if result['extraversion'] is not None:
                big_five_data['extraversion'] = result['extraversion']
            if result['agreeableness'] is not None:
                big_five_data['agreeableness'] = result['agreeableness']
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

        if all_defenses:
            defense_mechanisms = list(set(all_defenses))
            summary_parts.append(f"Defense Mechanisms: {', '.join(defense_mechanisms)}")

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