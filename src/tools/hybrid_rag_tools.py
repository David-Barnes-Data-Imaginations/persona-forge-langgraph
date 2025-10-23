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
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global RAG instance (initialize once, use many times)
_rag_instance = None


def get_rag_instance():
    """Get or create the global RAG instance"""
    global _rag_instance
    if _rag_instance is None:
        # Get Neo4j credentials from environment variables with fallbacks
        neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        neo4j_password = os.getenv("NEO4JP")  # Using your existing env var name

        if not neo4j_password:
            raise ValueError(
                "NEO4JP environment variable not set. "
                "Please add 'NEO4JP=your_password' to your .env file"
            )

        _rag_instance = PersonaForgeRAGTool(
            neo4j_uri=neo4j_uri, neo4j_user=neo4j_user, neo4j_password=neo4j_password
        )
    return _rag_instance


class PersonaForgeRAGTool:
    """Core RAG functionality for tool integration"""

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        if self.driver:
            self.driver.close()

    def search_psychological_context(
        self, query: str, k: int = 3
    ) -> List[Dict[str, Any]]:
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

            // Clinical analysis fields (SOAP format)
            qa.subjective_analysis as subjective_analysis,
            qa.objective_analysis as objective_analysis,
            qa.assessment as assessment,
            qa.plan as plan,

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

    This tool searches through analyzed therapy session text chunks using both semantic similarity (keywords like "sleep patterns" etc)
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
            emotions = [e for e in result["emotions"] if e["name"]]
            distortions = [d for d in result["distortions"] if d["type"]]
            attachments = [a for a in result["attachment_styles"] if a["name"]]
            schemas = [s for s in result["schemas"] if s["name"]]
            defenses = [d for d in result["defense_mechanisms"] if d["name"]]
            stages = [s for s in result["erikson_stages"] if s["name"]]

            # Build psychological profile summary
            psychology_parts = []

            if emotions:
                emotion_strs = [
                    f"{e['name']} (v:{e['valence']:.1f}, a:{e['arousal']:.1f}, conf:{e['confidence']:.1f})"
                    for e in emotions
                ]
                psychology_parts.append(f"Emotions: {', '.join(emotion_strs)}")

            if distortions:
                distortion_strs = [
                    f"{d['type']} (conf:{d['confidence']:.1f})" for d in distortions
                ]
                psychology_parts.append(
                    f"Cognitive Distortions: {', '.join(distortion_strs)}"
                )

            if attachments:
                attachment_strs = [
                    f"{a['name']} (conf:{a['confidence']:.1f})" for a in attachments
                ]
                psychology_parts.append(f"Attachment: {', '.join(attachment_strs)}")

            if schemas:
                schema_strs = [
                    f"{s['name']} (conf:{s['confidence']:.1f})" for s in schemas
                ]
                psychology_parts.append(f"Core Schemas: {', '.join(schema_strs)}")

            if defenses:
                defense_strs = [
                    f"{d['name']} (conf:{d['confidence']:.1f})" for d in defenses
                ]
                psychology_parts.append(
                    f"Defense Mechanisms: {', '.join(defense_strs)}"
                )

            if stages:
                stage_strs = [
                    f"{s['name']} (conf:{s['confidence']:.1f})" for s in stages
                ]
                psychology_parts.append(f"Erikson Stage: {', '.join(stage_strs)}")

            # Big Five if available
            big_five = []
            if result["openness"] is not None:
                big_five.append(f"Openness: {result['openness']:.1f}")
            if result["conscientiousness"] is not None:
                big_five.append(f"Conscientiousness: {result['conscientiousness']:.1f}")
            if result["extraversion"] is not None:
                big_five.append(f"Extraversion: {result['extraversion']:.1f}")
            if result["agreeableness"] is not None:
                big_five.append(f"Agreeableness: {result['agreeableness']:.1f}")
            if result["neuroticism"] is not None:
                big_five.append(f"Neuroticism: {result['neuroticism']:.1f}")

            # Add clinical analysis if available
            clinical_parts = []
            if result.get("subjective_analysis"):
                clinical_parts.append(f"Subjective: {result['subjective_analysis']}")
            if result.get("objective_analysis"):
                clinical_parts.append(f"Objective: {result['objective_analysis']}")
            if result.get("assessment"):
                clinical_parts.append(f"Assessment: {result['assessment']}")
            if result.get("plan"):
                clinical_parts.append(f"Plan: {result['plan']}")

            context_part = f"""
INSIGHT {i} (Relevance: {result['score']:.3f}):
Text: "{result['text']}"

Clinical Analysis:
{chr(10).join(clinical_parts) if clinical_parts else 'Not available'}

Psychology: {' | '.join(psychology_parts) if psychology_parts else 'None detected'}
Big Five: {' | '.join(big_five) if big_five else 'Not available'}
Source: {result['session_id']} → {result['qa_pair_id']} → {result['chunk_id']}

{'-' * 60}"""

            context_parts.append(context_part)

        return "\n".join(context_parts)

    except Exception as e:
        return f"Error searching psychological insights: {str(e)}"


@tool
def get_objective_statistics(session_id: str = "session_001") -> str:
    """
    Get 'objective' statistical analysis of psychological patterns across all QA pairs in a session.

    Returns counts, distributions, and aggregated metrics for emotions, distortions,
    schemas, attachment styles, defense mechanisms, and Big Five traits.

    Args:
        session_id: The session to analyze (default: 'session_001')

    Returns:
        Statistical summary of psychological patterns in the session
    """
    rag = get_rag_instance()

    cypher = """
    MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)

    // Count total QA pairs
    WITH s, count(qa) as total_qa_pairs, collect(qa) as qa_list

    // Aggregate emotions with statistics
    UNWIND qa_list as qa
    OPTIONAL MATCH (qa)-[emo_rel:REVEALS_EMOTION]->(e:Emotion)
    WITH s, total_qa_pairs, qa_list,
         collect({
             name: e.name,
             valence: emo_rel.valence,
             arousal: emo_rel.arousal,
             confidence: emo_rel.confidence
         }) as all_emotions

    // Aggregate distortions
    UNWIND qa_list as qa
    OPTIONAL MATCH (qa)-[dist_rel:EXHIBITS_DISTORTION]->(d:Cognitive_Distortion)
    WITH s, total_qa_pairs, qa_list, all_emotions,
         collect({type: d.type, confidence: dist_rel.confidence}) as all_distortions

    // Aggregate schemas
    UNWIND qa_list as qa
    OPTIONAL MATCH (qa)-[sch_rel:REVEALS_SCHEMA]->(sch:Schema)
    WITH s, total_qa_pairs, qa_list, all_emotions, all_distortions,
         collect({name: sch.name, confidence: sch_rel.confidence}) as all_schemas

    // Aggregate attachments
    UNWIND qa_list as qa
    OPTIONAL MATCH (qa)-[att_rel:REVEALS_ATTACHMENT_STYLE]->(a:Attachment_Style)
    WITH s, total_qa_pairs, qa_list, all_emotions, all_distortions, all_schemas,
         collect({name: a.name, confidence: att_rel.confidence}) as all_attachments

    // Aggregate defense mechanisms
    UNWIND qa_list as qa
    OPTIONAL MATCH (qa)-[def_rel:USES_DEFENSE_MECHANISM]->(dm:Defense_Mechanism)
    WITH s, total_qa_pairs, qa_list, all_emotions, all_distortions, all_schemas, all_attachments,
         collect({name: dm.name, confidence: def_rel.confidence}) as all_defenses

    // Aggregate Big Five traits
    UNWIND qa_list as qa
    OPTIONAL MATCH (qa)-[bf_rel:SHOWS_BIG_FIVE]->(bf:Big_Five)
    WITH s, total_qa_pairs, all_emotions, all_distortions, all_schemas, all_attachments, all_defenses,
         collect({
             openness: bf_rel.openness,
             conscientiousness: bf_rel.conscientiousness,
             extraversion: bf_rel.extraversion,
             agreeableness: bf_rel.agreeableness,
             neuroticism: bf_rel.neuroticism,
             confidence: bf_rel.confidence
         }) as all_big_five

    RETURN
        total_qa_pairs,
        all_emotions,
        all_distortions,
        all_schemas,
        all_attachments,
        all_defenses,
        all_big_five
    """

    with rag.driver.session() as session:
        try:
            result = session.run(cypher, session_id=session_id)
            record = result.single()

            if not record:
                return f"No data found for session: {session_id}"

            # Process statistics
            total_qa = record["total_qa_pairs"]

            # Emotion statistics
            emotions = [e for e in record["all_emotions"] if e["name"]]
            emotion_counts = {}
            emotion_valences = {}
            emotion_arousals = {}

            for e in emotions:
                name = e["name"]
                emotion_counts[name] = emotion_counts.get(name, 0) + 1
                if name not in emotion_valences:
                    emotion_valences[name] = []
                    emotion_arousals[name] = []
                emotion_valences[name].append(e["valence"])
                emotion_arousals[name].append(e["arousal"])

            # Distortion statistics
            distortions = [d for d in record["all_distortions"] if d["type"]]
            distortion_counts = {}
            for d in distortions:
                distortion_counts[d["type"]] = distortion_counts.get(d["type"], 0) + 1

            # Schema statistics
            schemas = [s for s in record["all_schemas"] if s["name"]]
            schema_counts = {}
            for s in schemas:
                schema_counts[s["name"]] = schema_counts.get(s["name"], 0) + 1

            # Attachment statistics
            attachments = [a for a in record["all_attachments"] if a["name"]]
            attachment_counts = {}
            for a in attachments:
                attachment_counts[a["name"]] = attachment_counts.get(a["name"], 0) + 1

            # Defense statistics
            defenses = [d for d in record["all_defenses"] if d["name"]]
            defense_counts = {}
            for d in defenses:
                defense_counts[d["name"]] = defense_counts.get(d["name"], 0) + 1

            # Big Five averages
            big_five_traits = [
                bf for bf in record["all_big_five"] if bf.get("openness") is not None
            ]
            big_five_avg = {}
            if big_five_traits:
                traits = [
                    "openness",
                    "conscientiousness",
                    "extraversion",
                    "agreeableness",
                    "neuroticism",
                ]
                for trait in traits:
                    values = [
                        bf[trait] for bf in big_five_traits if bf.get(trait) is not None
                    ]
                    if values:
                        big_five_avg[trait] = sum(values) / len(values)

            # Format output
            output_parts = [f"=== GRAPH STATISTICS FOR {session_id} ===\n"]
            output_parts.append(f"Total QA Pairs: {total_qa}\n")

            # Top 5 emotions
            if emotion_counts:
                sorted_emotions = sorted(
                    emotion_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]
                output_parts.append("Top 5 Emotions:")
                for emotion, count in sorted_emotions:
                    avg_valence = sum(emotion_valences[emotion]) / len(
                        emotion_valences[emotion]
                    )
                    avg_arousal = sum(emotion_arousals[emotion]) / len(
                        emotion_arousals[emotion]
                    )
                    output_parts.append(
                        f"  - {emotion}: {count} occurrences (avg valence: {avg_valence:.2f}, avg arousal: {avg_arousal:.2f})"
                    )

            # Top 5 distortions
            if distortion_counts:
                sorted_distortions = sorted(
                    distortion_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]
                output_parts.append("\nTop 5 Cognitive Distortions:")
                for distortion, count in sorted_distortions:
                    output_parts.append(f"  - {distortion}: {count} occurrences")

            # Top 5 schemas
            if schema_counts:
                sorted_schemas = sorted(
                    schema_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]
                output_parts.append("\nTop 5 Core Schemas:")
                for schema, count in sorted_schemas:
                    output_parts.append(f"  - {schema}: {count} occurrences")

            # Attachment styles
            if attachment_counts:
                output_parts.append("\nAttachment Styles:")
                for attachment, count in attachment_counts.items():
                    output_parts.append(f"  - {attachment}: {count} occurrences")

            # Defense mechanisms
            if defense_counts:
                sorted_defenses = sorted(
                    defense_counts.items(), key=lambda x: x[1], reverse=True
                )[:5]
                output_parts.append("\nTop 5 Defense Mechanisms:")
                for defense, count in sorted_defenses:
                    output_parts.append(f"  - {defense}: {count} occurrences")

            # Big Five averages
            if big_five_avg:
                output_parts.append("\nBig Five Personality Averages:")
                for trait, avg in big_five_avg.items():
                    level = "High" if avg > 0.7 else "Moderate" if avg > 0.4 else "Low"
                    output_parts.append(f"  - {trait.title()}: {avg:.2f} ({level})")

            return "\n".join(output_parts)

        except Exception as e:
            return f"Error getting graph statistics: {str(e)}"


@tool
def get_extreme_values(
    property_type: str, session_id: str = "session_001", limit: int = 3
) -> str:
    """
    Get QA pairs with extreme (highest/lowest) values for a specific psychological property.

    Use this to find outliers or most significant instances of emotions, distortions, etc.

    Args:
        property_type: Type to analyze - 'emotion_valence', 'emotion_arousal', 'neuroticism',
                      'openness', 'conscientiousness', 'extraversion', 'agreeableness'
        session_id: The session to analyze (default: 'session_001')
        limit: Number of extreme values to return (default: 3)

    Returns:
        QA pairs with the most extreme values for the specified property
    """
    rag = get_rag_instance()

    # Map property types to appropriate Cypher queries
    if property_type == "emotion_valence":
        cypher = """
        MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
        MATCH (qa)-[r:REVEALS_EMOTION]->(e:Emotion)
        WITH qa, r, e
        ORDER BY r.valence DESC
        LIMIT $limit

        OPTIONAL MATCH (qa)-[:HAS_CHUNK]->(tc:TextChunk)

        RETURN qa.id as qa_id,
               e.name as emotion,
               r.valence as value,
               r.arousal as arousal,
               r.confidence as confidence,
               collect(tc.text)[0] as sample_text
        """
    elif property_type == "emotion_arousal":
        cypher = """
        MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
        MATCH (qa)-[r:REVEALS_EMOTION]->(e:Emotion)
        WITH qa, r, e
        ORDER BY r.arousal DESC
        LIMIT $limit

        OPTIONAL MATCH (qa)-[:HAS_CHUNK]->(tc:TextChunk)

        RETURN qa.id as qa_id,
               e.name as emotion,
               r.valence as valence,
               r.arousal as value,
               r.confidence as confidence,
               collect(tc.text)[0] as sample_text
        """
    elif property_type in [
        "neuroticism",
        "openness",
        "conscientiousness",
        "extraversion",
        "agreeableness",
    ]:
        cypher = f"""
        MATCH (s:Session {{session_id: $session_id}})-[:INCLUDES]->(qa:QA_Pair)
        MATCH (qa)-[r:SHOWS_BIG_FIVE]->(bf:Big_Five)
        WHERE r.{property_type} IS NOT NULL
        WITH qa, r.{property_type} as value, r.confidence as confidence
        ORDER BY value DESC
        LIMIT $limit

        OPTIONAL MATCH (qa)-[:HAS_CHUNK]->(tc:TextChunk)

        RETURN qa.id as qa_id,
               value,
               confidence,
               collect(tc.text)[0] as sample_text
        """
    else:
        return f"Unknown property type: {property_type}. Use 'emotion_valence', 'emotion_arousal', or Big Five traits."

    with rag.driver.session() as session:
        try:
            results = session.run(cypher, session_id=session_id, limit=limit)
            records = [dict(record) for record in results]

            if not records:
                return f"No data found for {property_type} in session {session_id}"

            # Format output
            output_parts = [f"=== EXTREME VALUES FOR {property_type.upper()} ===\n"]

            for i, record in enumerate(records, 1):
                output_parts.append(f"{i}. QA Pair: {record['qa_id']}")

                if "emotion" in record:
                    output_parts.append(f"   Emotion: {record['emotion']}")
                    if "valence" in record and record.get("valence") is not None:
                        output_parts.append(f"   Valence: {record['valence']:.2f}")
                    if "arousal" in record and record.get("arousal") is not None:
                        output_parts.append(f"   Arousal: {record['arousal']:.2f}")
                else:
                    output_parts.append(
                        f"   {property_type.title()}: {record['value']:.2f}"
                    )

                output_parts.append(f"   Confidence: {record['confidence']:.2f}")

                if record.get("sample_text"):
                    text_preview = (
                        record["sample_text"][:150] + "..."
                        if len(record["sample_text"]) > 150
                        else record["sample_text"]
                    )
                    output_parts.append(f'   Sample: "{text_preview}"')

                output_parts.append("")

            return "\n".join(output_parts)

        except Exception as e:
            return f"Error getting extreme values: {str(e)}"


@tool
def get_qa_pair_details(qa_pair_id: str) -> str:
    """
    Get complete details for a specific QA pair including all psychological analysis and full text.

    Use this after identifying interesting QA pairs from statistics or extreme values.

    Args:
        qa_pair_id: The ID of the QA pair to retrieve (e.g., 'qa_pair_001')

    Returns:
        Complete psychological analysis and text content for the QA pair
    """
    rag = get_rag_instance()

    cypher = """
    MATCH (qa:QA_Pair {id: $qa_pair_id})

    // Get all psychological relationships
    OPTIONAL MATCH (qa)-[emo_rel:REVEALS_EMOTION]->(e:Emotion)
    OPTIONAL MATCH (qa)-[dist_rel:EXHIBITS_DISTORTION]->(d:Cognitive_Distortion)
    OPTIONAL MATCH (qa)-[sch_rel:REVEALS_SCHEMA]->(s:Schema)
    OPTIONAL MATCH (qa)-[att_rel:REVEALS_ATTACHMENT_STYLE]->(a:Attachment_Style)
    OPTIONAL MATCH (qa)-[def_rel:USES_DEFENSE_MECHANISM]->(dm:Defense_Mechanism)
    OPTIONAL MATCH (qa)-[stage_rel:EXHIBITS_STAGE]->(es:Erikson_Stage)
    OPTIONAL MATCH (qa)-[bf_rel:SHOWS_BIG_FIVE]->(bf:Big_Five)

    // Get all text chunks
    OPTIONAL MATCH (qa)-[:HAS_CHUNK]->(tc:TextChunk)

    RETURN
        qa.id as qa_id,
        qa.question as question,
        qa.answer as answer,
        qa.subjective_analysis as subjective_analysis,
        qa.objective_analysis as objective_analysis,
        qa.assessment as assessment,
        qa.plan as plan,
        collect(DISTINCT {name: e.name, valence: emo_rel.valence, arousal: emo_rel.arousal, confidence: emo_rel.confidence}) as emotions,
        collect(DISTINCT {type: d.type, confidence: dist_rel.confidence}) as distortions,
        collect(DISTINCT {name: s.name, confidence: sch_rel.confidence}) as schemas,
        collect(DISTINCT {name: a.name, confidence: att_rel.confidence}) as attachments,
        collect(DISTINCT {name: dm.name, confidence: def_rel.confidence}) as defenses,
        collect(DISTINCT {name: es.name, confidence: stage_rel.confidence}) as stages,
        bf_rel.openness as openness,
        bf_rel.conscientiousness as conscientiousness,
        bf_rel.extraversion as extraversion,
        bf_rel.agreeableness as agreeableness,
        bf_rel.neuroticism as neuroticism,
        bf_rel.confidence as big_five_confidence,
        collect(tc.text) as text_chunks
    """

    with rag.driver.session() as session:
        try:
            result = session.run(cypher, qa_pair_id=qa_pair_id)
            record = result.single()

            if not record:
                return f"QA pair not found: {qa_pair_id}"

            # Format output
            output_parts = [f"=== COMPLETE ANALYSIS FOR {qa_pair_id} ===\n"]

            # Original Question & Answer
            if record.get("question"):
                output_parts.append("ORIGINAL QUESTION:")
                output_parts.append(f"{record['question']}\n")

            if record.get("answer"):
                output_parts.append("ORIGINAL ANSWER:")
                output_parts.append(f"{record['answer']}\n")

            # Analysis Sections
            if record.get("subjective_analysis"):
                output_parts.append("SUBJECTIVE ANALYSIS:")
                output_parts.append(f"{record['subjective_analysis']}\n")

            if record.get("objective_analysis"):
                output_parts.append("OBJECTIVE ANALYSIS:")
                output_parts.append(f"{record['objective_analysis']}\n")

            if record.get("assessment"):
                output_parts.append("ASSESSMENT:")
                output_parts.append(f"{record['assessment']}\n")

            if record.get("plan"):
                output_parts.append("PLAN:")
                output_parts.append(f"{record['plan']}\n")

            output_parts.append("=" * 60 + "\n")
            output_parts.append("DETAILED PSYCHOLOGY FRAMEWORKS:\n")

            # Emotions
            emotions = [e for e in record["emotions"] if e.get("name")]
            if emotions:
                output_parts.append("\nEMOTIONS:")
                for e in emotions:
                    output_parts.append(
                        f"  - {e['name']}: valence={e['valence']:.2f}, arousal={e['arousal']:.2f}, confidence={e['confidence']:.2f}"
                    )

            # Cognitive distortions
            distortions = [d for d in record["distortions"] if d.get("type")]
            if distortions:
                output_parts.append("\nCOGNITIVE DISTORTIONS:")
                for d in distortions:
                    output_parts.append(
                        f"  - {d['type']}: confidence={d['confidence']:.2f}"
                    )

            # Schemas
            schemas = [s for s in record["schemas"] if s.get("name")]
            if schemas:
                output_parts.append("\nCORE SCHEMAS:")
                for s in schemas:
                    output_parts.append(
                        f"  - {s['name']}: confidence={s['confidence']:.2f}"
                    )

            # Attachment styles
            attachments = [a for a in record["attachments"] if a.get("name")]
            if attachments:
                output_parts.append("\nATTACHMENT STYLES:")
                for a in attachments:
                    output_parts.append(
                        f"  - {a['name']}: confidence={a['confidence']:.2f}"
                    )

            # Defense mechanisms
            defenses = [d for d in record["defenses"] if d.get("name")]
            if defenses:
                output_parts.append("\nDEFENSE MECHANISMS:")
                for d in defenses:
                    output_parts.append(
                        f"  - {d['name']}: confidence={d['confidence']:.2f}"
                    )

            # Erikson stages
            stages = [s for s in record["stages"] if s.get("name")]
            if stages:
                output_parts.append("\nERIKSON STAGES:")
                for s in stages:
                    output_parts.append(
                        f"  - {s['name']}: confidence={s['confidence']:.2f}"
                    )

            # Big Five
            if record.get("openness") is not None:
                output_parts.append("\nBIG FIVE PERSONALITY:")
                output_parts.append(f"  - Openness: {record['openness']:.2f}")
                output_parts.append(
                    f"  - Conscientiousness: {record['conscientiousness']:.2f}"
                )
                output_parts.append(f"  - Extraversion: {record['extraversion']:.2f}")
                output_parts.append(f"  - Agreeableness: {record['agreeableness']:.2f}")
                output_parts.append(f"  - Neuroticism: {record['neuroticism']:.2f}")
                output_parts.append(
                    f"  - Confidence: {record['big_five_confidence']:.2f}"
                )

            # Full text
            text_chunks = record.get("text_chunks", [])
            if text_chunks:
                output_parts.append("\nFULL TEXT:")
                for i, chunk in enumerate(text_chunks, 1):
                    output_parts.append(f"  Chunk {i}: {chunk}")

            return "\n".join(output_parts)

        except Exception as e:
            return f"Error getting QA pair details: {str(e)}"


@tool
def get_personality_summary(focus_area: str = "overall", session_id: str = "session_001") -> str:
    """
    Get a summary of personality traits and psychological patterns across a session.

    This tool uses direct graph queries (not vector search) to aggregate psychological
    patterns and provide a comprehensive personality profile.

    Args:
        focus_area: Area to focus on - 'overall', 'emotions', 'cognition', 'attachment', or 'personality'
        session_id: The session to analyze (default: 'session_001')

    Returns:
        Summary of psychological patterns and personality insights
    """
    rag = get_rag_instance()

    try:
        # Build Cypher query based on focus area
        if focus_area == "overall":
            # Get everything
            cypher = """
            MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)

            // Get all psychological relationships
            OPTIONAL MATCH (qa)-[emo_rel:REVEALS_EMOTION]->(e:Emotion)
            OPTIONAL MATCH (qa)-[dist_rel:EXHIBITS_DISTORTION]->(d:Cognitive_Distortion)
            OPTIONAL MATCH (qa)-[att_rel:REVEALS_ATTACHMENT_STYLE]->(a:Attachment_Style)
            OPTIONAL MATCH (qa)-[sch_rel:REVEALS_SCHEMA]->(sch:Schema)
            OPTIONAL MATCH (qa)-[def_rel:USES_DEFENSE_MECHANISM]->(dm:Defense_Mechanism)
            OPTIONAL MATCH (qa)-[bf_rel:SHOWS_BIG_FIVE]->(bf:Big_Five)

            WITH
                collect(DISTINCT e.name) as emotions,
                collect(DISTINCT d.type) as distortions,
                collect(DISTINCT a.name) as attachments,
                collect(DISTINCT sch.name) as schemas,
                collect(DISTINCT dm.name) as defenses,
                collect(DISTINCT {
                    openness: bf_rel.openness,
                    conscientiousness: bf_rel.conscientiousness,
                    extraversion: bf_rel.extraversion,
                    agreeableness: bf_rel.agreeableness,
                    neuroticism: bf_rel.neuroticism
                }) as big_five_list

            RETURN emotions, distortions, attachments, schemas, defenses, big_five_list
            """
        elif focus_area == "emotions":
            cypher = """
            MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
            OPTIONAL MATCH (qa)-[emo_rel:REVEALS_EMOTION]->(e:Emotion)
            RETURN collect(DISTINCT e.name) as emotions
            """
        elif focus_area == "cognition":
            cypher = """
            MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
            OPTIONAL MATCH (qa)-[dist_rel:EXHIBITS_DISTORTION]->(d:Cognitive_Distortion)
            OPTIONAL MATCH (qa)-[sch_rel:REVEALS_SCHEMA]->(sch:Schema)
            RETURN collect(DISTINCT d.type) as distortions, collect(DISTINCT sch.name) as schemas
            """
        elif focus_area == "attachment":
            cypher = """
            MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
            OPTIONAL MATCH (qa)-[att_rel:REVEALS_ATTACHMENT_STYLE]->(a:Attachment_Style)
            RETURN collect(DISTINCT a.name) as attachments
            """
        elif focus_area == "personality":
            cypher = """
            MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
            OPTIONAL MATCH (qa)-[bf_rel:SHOWS_BIG_FIVE]->(bf:Big_Five)
            RETURN collect(DISTINCT {
                openness: bf_rel.openness,
                conscientiousness: bf_rel.conscientiousness,
                extraversion: bf_rel.extraversion,
                agreeableness: bf_rel.agreeableness,
                neuroticism: bf_rel.neuroticism
            }) as big_five_list
            """
        else:
            return f"Unknown focus area: {focus_area}. Use 'overall', 'emotions', 'cognition', 'attachment', or 'personality'."

        with rag.driver.session() as session:
            result = session.run(cypher, session_id=session_id)
            record = result.single()

            if not record:
                return f"No data found for session: {session_id}"

            # Build summary based on what we got
            summary_parts = [f"=== PERSONALITY SUMMARY: {focus_area.upper()} ({session_id}) ===\n"]

            # Process based on focus area
            if focus_area in ["overall", "emotions"]:
                emotions = [e for e in record.get("emotions", []) if e]
                if emotions:
                    unique_emotions = list(set(emotions))
                    summary_parts.append(f"Dominant Emotions ({len(unique_emotions)}): {', '.join(unique_emotions)}")

            if focus_area in ["overall", "cognition"]:
                distortions = [d for d in record.get("distortions", []) if d]
                if distortions:
                    unique_distortions = list(set(distortions))
                    summary_parts.append(f"Cognitive Patterns ({len(unique_distortions)}): {', '.join(unique_distortions)}")

                schemas = [s for s in record.get("schemas", []) if s]
                if schemas:
                    unique_schemas = list(set(schemas))
                    summary_parts.append(f"Core Schemas ({len(unique_schemas)}): {', '.join(unique_schemas)}")

            if focus_area in ["overall", "attachment"]:
                attachments = [a for a in record.get("attachments", []) if a]
                if attachments:
                    unique_attachments = list(set(attachments))
                    summary_parts.append(f"Attachment Styles ({len(unique_attachments)}): {', '.join(unique_attachments)}")

            if focus_area == "overall":
                defenses = [d for d in record.get("defenses", []) if d]
                if defenses:
                    unique_defenses = list(set(defenses))
                    summary_parts.append(f"Defense Mechanisms ({len(unique_defenses)}): {', '.join(unique_defenses)}")

            if focus_area in ["overall", "personality"]:
                big_five_list = record.get("big_five_list", [])
                # Filter out entries where all values are None
                valid_big_five = [bf for bf in big_five_list if bf.get("openness") is not None]

                if valid_big_five:
                    # Calculate averages
                    traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
                    trait_avgs = {}

                    for trait in traits:
                        values = [bf[trait] for bf in valid_big_five if bf.get(trait) is not None]
                        if values:
                            trait_avgs[trait] = sum(values) / len(values)

                    if trait_avgs:
                        big_five_summary = []
                        for trait, score in trait_avgs.items():
                            level = "High" if score > 0.7 else "Moderate" if score > 0.4 else "Low"
                            big_five_summary.append(f"{trait.title()}: {level} ({score:.2f})")
                        summary_parts.append(f"Big Five Profile: {' | '.join(big_five_summary)}")

            # If we have no data at all
            if len(summary_parts) == 1:
                summary_parts.append(f"No {focus_area} data found for this session.")

            return "\n".join(summary_parts)

    except Exception as e:
        return f"Error generating personality summary: {str(e)}"


@tool
def retrieve_diagnosis(client_id: str = "client_001") -> str:
    """
    Retrieve the complete diagnosis and medical history for a client.

    Returns the client's medical history, diagnoses, previous treatments,
    family history, and risk factors from the knowledge graph.

    Args:
        client_id: The client ID to retrieve diagnosis for (default: 'client_001')

    Returns:
        Complete medical history and diagnostic information
    """
    rag = get_rag_instance()

    cypher = """
    MATCH (c:Client {id: $client_id})-[:HAS_HISTORY]->(h:History)
    RETURN
        h.medical_history as medical_history,
        h.diagnoses as diagnoses,
        h.previous_treatments as previous_treatments,
        h.family_history as family_history,
        h.risk_factors as risk_factors,
        h.last_updated as last_updated
    """

    with rag.driver.session() as session:
        try:
            result = session.run(cypher, client_id=client_id)
            record = result.single()

            if not record:
                return f"No diagnosis/history found for client: {client_id}"

            # Format output
            output_parts = [
                f"=== DIAGNOSIS AND MEDICAL HISTORY FOR {client_id.upper()} ===\n"
            ]

            if record.get("medical_history"):
                output_parts.append("MEDICAL HISTORY:")
                output_parts.append(f"{record['medical_history']}\n")

            if record.get("diagnoses"):
                output_parts.append("CURRENT DIAGNOSES:")
                for diagnosis in record["diagnoses"]:
                    output_parts.append(f"  - {diagnosis}")
                output_parts.append("")

            if record.get("previous_treatments"):
                output_parts.append("PREVIOUS TREATMENTS:")
                for treatment in record["previous_treatments"]:
                    output_parts.append(f"  - {treatment}")
                output_parts.append("")

            if record.get("family_history"):
                output_parts.append("FAMILY HISTORY:")
                for item in record["family_history"]:
                    output_parts.append(f"  - {item}")
                output_parts.append("")

            if record.get("risk_factors"):
                output_parts.append("RISK ASSESSMENT:")
                for risk in record["risk_factors"]:
                    output_parts.append(f"  - {risk}")
                output_parts.append("")

            if record.get("last_updated"):
                output_parts.append(f"Last Updated: {record['last_updated']}")

            return "\n".join(output_parts)

        except Exception as e:
            return f"Error retrieving diagnosis: {str(e)}"


@tool
def get_subjective_analysis(session_id: str = "session_001") -> str:
    """
    Retrieve ALL subjective analysis sections from QA pairs in a session,
    then summarize them using Gemini to extract common themes.

    The subjective analysis contains client-reported experiences, feelings,
    and symptoms. This function retrieves all analyses and uses Gemini to
    create a condensed summary of common themes, making it easier for local
    models to process.

    Args:
        session_id: The session to retrieve subjective analyses from (default: 'session_001')

    Returns:
        Gemini-generated summary of common themes from all subjective analyses
    """
    rag = get_rag_instance()

    # Retrieve ALL QA pairs with subjective analysis
    cypher = """
    MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
    WHERE qa.subjective_analysis IS NOT NULL
    RETURN qa.id as qa_id,
           qa.question as question,
           qa.subjective_analysis as subjective_analysis
    ORDER BY qa.id
    """

    with rag.driver.session() as session:
        try:
            results = session.run(cypher, session_id=session_id)
            records = [dict(record) for record in results]

            if not records:
                return f"No subjective analyses found for session: {session_id}"

            # Collect all subjective analyses
            all_analyses = []
            for record in records:
                all_analyses.append(
                    f"QA Pair {record['qa_id']}:\n{record['subjective_analysis']}"
                )

            # Combine all analyses into one text block
            combined_text = "\n\n".join(all_analyses)

            from langchain_google_genai import ChatGoogleGenerativeAI

            # Import Gemini for summarization
            gemini_model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                temperature=0.3,
                api_key=os.environ.get("GEMINI_API_KEY"),
            )

            # Create summarization prompt
            summarization_prompt = f"""Review the subjective analysis from these QA pairs in a therapy script.
Extract the common themes to provide a summary of analysis. Leave out any quoted comments from the client.

Focus on:
1. Common emotional patterns
2. Recurring symptoms or experiences
3. Major psychological themes
4. Key concerns or issues raised

Subjective Analyses:
{combined_text}

Provide a concise thematic summary (300-500 words max):"""

            # Get summary from Gemini
            from langchain_core.messages import HumanMessage

            summary_response = gemini_model.invoke(
                [HumanMessage(content=summarization_prompt)]
            )
            summary = summary_response.content

            # Format final output
            output = f"""=== SUBJECTIVE ANALYSIS SUMMARY FOR {session_id.upper()} ===

Total QA Pairs Analyzed: {len(records)}

THEMATIC SUMMARY:
{summary}

---
Note: This is a Gemini-generated summary of {len(records)} subjective analyses.
Use get_qa_pair_details() to view individual analyses if needed.
"""

            return output

        except Exception as e:
            return f"Error retrieving and summarizing subjective analyses: {str(e)}"


@tool
def get_plan(session_id: str = "session_001") -> str:
    """
    Retrieve all treatment plan sections from QA pairs in a session.

    The plan contains recommended next steps, interventions, monitoring strategies,
    homework assignments, and follow-up actions for the client.

    Args:
        session_id: The session to retrieve plans from (default: 'session_001')

    Returns:
        All treatment plan sections organized by QA pair
    """
    rag = get_rag_instance()

    cypher = """
    MATCH (s:Session {session_id: $session_id})-[:INCLUDES]->(qa:QA_Pair)
    WHERE qa.plan IS NOT NULL
    RETURN qa.id as qa_id,
           qa.question as question,
           qa.plan as plan
    ORDER BY qa.id
    """

    with rag.driver.session() as session:
        try:
            results = session.run(cypher, session_id=session_id)
            records = [dict(record) for record in results]

            if not records:
                return f"No treatment plans found for session: {session_id}"

            # Format output
            output_parts = [f"=== TREATMENT PLANS FOR {session_id.upper()} ===\n"]
            output_parts.append(f"Total QA Pairs: {len(records)}\n")

            for record in records:
                output_parts.append(f"QA PAIR: {record['qa_id']}")
                output_parts.append(f"Question: {record['question']}\n")
                output_parts.append(f"Treatment Plan:")
                output_parts.append(f"{record['plan']}\n")
                output_parts.append("-" * 60 + "\n")

            return "\n".join(output_parts)

        except Exception as e:
            return f"Error retrieving treatment plans: {str(e)}"


# Tool list for import to chat_agents tools
PERSONA_FORGE_TOOLS = [
    search_psychological_insights,
    get_personality_summary,
    get_extreme_values,
    get_qa_pair_details,
    retrieve_diagnosis,
    get_subjective_analysis,
    get_objective_statistics,
    get_plan,
]


# Cleanup function
def cleanup_rag_connection():
    """Call this when shutting down your application"""
    global _rag_instance
    if _rag_instance:
        _rag_instance.close()
        _rag_instance = None
