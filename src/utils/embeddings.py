from __future__ import annotations
from typing import List
import os
import requests
import json

_backend = os.getenv("EMBED_BACKEND", "ollama")
_model = os.getenv(
    "EMBED_MODEL", os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text:latest")
)


def embed_texts(texts: List[str], model_name: str = None) -> List[List[float]]:
    model = model_name or _model

    if _backend == "ollama":
        # Use Ollama for embeddings
        embeddings = []
        for text in texts:
            try:
                response = requests.post(
                    "http://localhost:11434/api/embeddings",
                    json={"model": model, "prompt": text},
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                embedding = response.json().get("embedding", [])
                embeddings.append(embedding)
            except Exception as e:
                print(f"Error getting embedding for text: {e}")
                # Return a zero vector as fallback
                embeddings.append([0.0] * 768)  # Common embedding dimension
        return embeddings

    elif _backend == "local":
        from sentence_transformers import SentenceTransformer

        st = SentenceTransformer(model)
        return st.encode(texts, normalize_embeddings=True).tolist()

    elif _backend == "openai":
        from openai import OpenAI

        client = OpenAI()
        # replace with your preferred embedding model
        emb = client.embeddings.create(model="text-embedding-3-large", input=texts)
        return [d.embedding for d in emb.data]

    elif _backend == "gemini":
        # Use langchain's GoogleGenerativeAIEmbeddings which properly handles credentials
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        # Force use of GOOGLE_APPLICATION_CREDENTIALS by unsetting API keys
        # This ensures embeddings use OAuth2 credentials like the voice service
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            # Temporarily unset API keys to force credential file usage
            os.environ.pop("GOOGLE_API_KEY", None)
            os.environ.pop("GEMINI_API_KEY", None)

        try:
            embeddings_model = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004", task_type="retrieval_document"
            )
            # Use langchain's embed_documents method which handles batching
            embeddings = embeddings_model.embed_documents(texts)
            return embeddings
        except Exception as e:
            print(f"Error getting Gemini embeddings: {e}")
            # Return zero vectors as fallback
            return [[0.0] * 768 for _ in texts]

    else:
        raise ValueError(f"Unknown EMBED_BACKEND: {_backend}")


def neo4j_vector_search(tx, query_vec, k=8):
    res = tx.run(
        """
      CALL db.index.vector.queryNodes('textchunk_embedding_index', $k, $q)
      YIELD node, score
      RETURN node.id AS chunk_id, node.text AS text, coalesce(node.source,'') AS source, score
    """,
        k=k,
        q=query_vec,
    )
    return [r.data() for r in res]
