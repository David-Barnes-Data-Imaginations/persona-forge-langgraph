"""
Ollama-compatible embedding loader for Persona-Forge
Adapts existing Ollama setup for Neo4j loading
Will add it to automation at some point
"""

import json
import os
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
import requests
from datetime import datetime

# Import your existing embedding function
from src.utils.embeddings import embed_texts
neo4j_password = os.getenv("NEO4JP")

jsonl_filepath = '/home/david-barnes/Documents/Projects/sentiment_suite/output/chunks_for_embedding/20250917/embedding_params_230044.json'

class OllamaPersonaForgeRAG:
    """
    RAG system using your existing Ollama embedding setup
    """

    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        self.driver.close()

    def load_embeddings_from_json(self, json_filepath: str) -> Dict[str, Any]:
        """
        Load embeddings from your JSON format (embedding_params_230044.json)
        """
        print(f"Loading embeddings from JSON: {json_filepath}")

        if not os.path.exists(json_filepath):
            return {"error": f"File not found: {json_filepath}"}

        with open(json_filepath, 'r') as f:
            data = json.load(f)

        # Extract just chunk_id and embedding for Neo4j
        embedding_records = []
        for item in data.get('embeddings', []):
            embedding_records.append({
                'chunk_id': item['chunk_id'],
                'embedding': item['embedding']
            })

        return self._load_embeddings_to_neo4j(embedding_records)

    def _load_embeddings_to_neo4j(self, embedding_records: List[Dict]) -> Dict[str, Any]:
        """
        Internal method to load embeddings into Neo4j using your format
        """
        cypher = """
        UNWIND $embeddings AS e
        MATCH (t:TextChunk {id: e.chunk_id})
        CALL db.create.setNodeVectorProperty(t, 'embedding', e.embedding)
        RETURN t.id as chunk_id, LEFT(t.text, 50) + '...' as text_preview
        """

        try:
            with self.driver.session() as session:
                result = session.run(cypher, embeddings=embedding_records)
                updated_chunks = list(result)

                print(f"✅ Successfully loaded embeddings for {len(updated_chunks)} TextChunk nodes")
                return {
                    "status": "success",
                    "updated_count": len(updated_chunks),
                    "chunks": updated_chunks
                }

        except Exception as e:
            print(f"❌ Error loading embeddings: {e}")
            return {"status": "error", "error": str(e)}

    def generate_embeddings_for_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using your existing Ollama setup
        """
        print(f"Generating embeddings for {len(texts)} texts using Ollama...")
        return embed_texts(texts)

    def hybrid_search_with_ollama(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Perform hybrid search using Ollama for query embedding
        """
        print(f"\n🔎 Hybrid search for: '{query}'")

        # Use your existing Ollama embedding function
        query_embedding = embed_texts([query])[0]  # Get embedding for single query

        cypher = """
        CALL db.index.vector.queryNodes('textchunk_embedding_index', $k, $query_embedding)
        YIELD node, score

        // Get rich psychological context
        MATCH (node:TextChunk)
        OPTIONAL MATCH (node)-[:REVEALS_EMOTION]->(e:Emotion)
        OPTIONAL MATCH (node)-[:EXHIBITS_DISTORTION]->(d:Cognitive_Distortion)
        OPTIONAL MATCH (node)-[:REVEALS_ATTACHMENT_STYLE]->(a:Attachment_Style)
        OPTIONAL MATCH (node)-[:REVEALS_SCHEMA]->(s:Schema)
        OPTIONAL MATCH (node)-[:USES_DEFENSE_MECHANISM]->(m:Defense_Mechanism)
        OPTIONAL MATCH (node)-[:EXHIBITS_STAGE]->(es:Erikson_Stage)

        // Get parent context from your main psychological graph
        OPTIONAL MATCH (qa:QA_Pair)-[:HAS_CHUNK]->(node)
        OPTIONAL MATCH (session:Session)-[:INCLUDES_CHUNK]->(node)

        // Get the full QA_Pair psychological analysis too
        OPTIONAL MATCH (qa)-[:REVEALS_EMOTION]->(qa_emotion:Emotion)
        OPTIONAL MATCH (qa)-[:EXHIBITS_DISTORTION]->(qa_distortion:Cognitive_Distortion)
        OPTIONAL MATCH (qa)-[:SHOWS_BIG_FIVE]->(big5:Big_Five)

        RETURN
            node.id as chunk_id,
            LEFT(node.text, 150) + '...' as text_preview,
            node.text as full_text,
            score,
            node.valence as chunk_valence,
            node.arousal as chunk_arousal,
            node.confidence as chunk_confidence,

            // Chunk-level psychological tags
            collect(DISTINCT e.name) as chunk_emotions,
            collect(DISTINCT d.type) as chunk_distortions,
            collect(DISTINCT a.name) as chunk_attachment_styles,
            collect(DISTINCT s.name) as chunk_schemas,
            collect(DISTINCT m.name) as chunk_defense_mechanisms,
            collect(DISTINCT es.name) as chunk_erikson_stages,

            // Parent QA context
            qa.id as qa_pair_id,
            session.session_id as session,

            // QA-level psychological analysis
            collect(DISTINCT qa_emotion.name) as qa_emotions,
            collect(DISTINCT qa_distortion.type) as qa_distortions,
            big5.openness as openness,
            big5.neuroticism as neuroticism,
            big5.extraversion as extraversion

        ORDER BY score DESC
        """

        with self.driver.session() as session:
            try:
                results = session.run(cypher, k=k, query_embedding=query_embedding)
                search_results = [dict(record) for record in results]

                print(f"Found {len(search_results)} relevant chunks:")
                for i, result in enumerate(search_results, 1):
                    print(f"\n{i}. Chunk: {result['chunk_id']} (Score: {result['score']:.3f})")
                    print(f"   Text: {result['text_preview']}")
                    print(f"   Chunk Psychology: {result['chunk_emotions']} | {result['chunk_distortions']}")
                    if result['qa_pair_id']:
                        print(f"   QA Context: {result['qa_pair_id']} | Big5: O={result['openness']}, N={result['neuroticism']}")

                return search_results

            except Exception as e:
                print(f"❌ Search error: {e}")
                return []

    def create_rag_context_with_psychology(self, search_results: List[Dict]) -> str:
        """
        Create rich context for LLM including both chunk-level and QA-level psychology
        """
        if not search_results:
            return "No relevant psychological context found."

        context_parts = ["=== PERSONA-FORGE PSYCHOLOGICAL CONTEXT ===\n"]

        for i, result in enumerate(search_results, 1):
            # Combine chunk-level and QA-level psychological insights
            chunk_psych = []
            if result['chunk_emotions']:
                chunk_psych.append(f"Emotions: {', '.join(result['chunk_emotions'])}")
            if result['chunk_distortions']:
                chunk_psych.append(f"Distortions: {', '.join(result['chunk_distortions'])}")
            if result['chunk_attachment_styles']:
                chunk_psych.append(f"Attachment: {', '.join(result['chunk_attachment_styles'])}")

            qa_psych = []
            if result['qa_emotions']:
                qa_psych.append(f"QA Emotions: {', '.join(result['qa_emotions'])}")
            if result['qa_distortions']:
                qa_psych.append(f"QA Distortions: {', '.join(result['qa_distortions'])}")
            if result['openness']:
                qa_psych.append(f"Big5: O={result['openness']:.1f}, N={result['neuroticism']:.1f}, E={result['extraversion']:.1f}")

            context = f"""
Context {i} (Similarity: {result['score']:.3f}):
"{result['full_text']}"

Chunk-Level Psychology: {' | '.join(chunk_psych) if chunk_psych else 'None detected'}
QA-Level Psychology: {' | '.join(qa_psych) if qa_psych else 'None detected'}
Emotional State: Valence={result['chunk_valence']}, Arousal={result['chunk_arousal']}
Source: {result['session']} → {result['qa_pair_id']}

{'-' * 70}"""
            context_parts.append(context)

        return "\n".join(context_parts)


def test_ollama_embedding_system():
    """Test the Ollama-based embedding system"""

    # Configuration
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = input("Enter your Neo4j password: ")

    # Initialize
    rag = OllamaPersonaForgeRAG(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Option 1: Load from your existing JSONL files
        jsonl_files = []
        for root, dirs, files in os.walk("output/chunks_for_embedding"):
            for file in files:
                if file.startswith("embeddings_") and file.endswith(".jsonl"):
                    jsonl_files.append(os.path.join(root, file))

        if jsonl_files:
            latest_jsonl = max(jsonl_files, key=os.path.getctime)
            print(f"Found JSONL embedding file: {latest_jsonl}")

            load_choice = input("Load embeddings from JSONL? [y/N]: ").lower()
            if load_choice == 'y':
                result = rag.load_embeddings_from_your_jsonl(latest_jsonl)
                print(f"Load result: {result}")

        # Option 2: Load from your JSON params file
        json_file = "embedding_params_230044.json"
        if os.path.exists(json_file):
            print(f"Found JSON embedding file: {json_file}")

            load_choice = input("Load embeddings from JSON? [y/N]: ").lower()
            if load_choice == 'y':
                result = rag.load_embeddings_from_json(json_file)
                print(f"Load result: {result}")

        # Test hybrid search
        test_queries = [
            "emotional empathy with others",
            "visualization anger strength gym",
            "attachment style relationships",
            "cognitive distortions thinking patterns"
        ]

        for query in test_queries:
            print(f"\n{'='*60}")
            results = rag.hybrid_search_with_ollama(query, k=5)

            if results:
                print(f"\n📝 RAG Context for '{query}':")
                context = rag.create_rag_context_with_psychology(results)
                print(context)

        print("\n✅ Ollama-based RAG testing complete!")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        rag.close()


if __name__ == "__main__":
    # Quick embedding load without the full test
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "W00dpidge0n!"  # Using your password from the file

    # Initialize the RAG system
    rag = OllamaPersonaForgeRAG(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    try:
        # Load embeddings from your JSON file
        json_file_path = '/home/david-barnes/Documents/Projects/sentiment_suite/output/chunks_for_embedding/20250917/embedding_params_230044.json'

        print("🚀 Loading embeddings into Neo4j...")
        result = rag.load_embeddings_from_json(json_file_path)
        print(f"📊 Result: {result}")

        if result.get("status") == "success":
            print(f"✅ Successfully loaded {result['updated_count']} embeddings!")

            # Quick test search
            print("\n🔍 Testing hybrid search...")
            search_results = rag.hybrid_search_with_ollama("emotions", k=2)

            if search_results:
                print("\n📝 RAG Context Preview:")
                context = rag.create_rag_context_with_psychology(search_results)
                print(context[:500] + "..." if len(context) > 500 else context)
            else:
                print("❌ No search results - check if vector index is working")
        else:
            print(f"❌ Failed to load embeddings: {result}")

    finally:
        rag.close()
        print("🔌 Connection closed")