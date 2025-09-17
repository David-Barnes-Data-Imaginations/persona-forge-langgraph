from __future__ import annotations
from typing import List
import os

_backend = os.getenv("EMBED_BACKEND", "local")
_model   = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")

def embed_texts(texts: List[str], model_name: str = None) -> List[List[float]]:
    model = model_name or _model
    if _backend == "local":
        from sentence_transformers import SentenceTransformer
        st = SentenceTransformer(model)
        return st.encode(texts, normalize_embeddings=True).tolist()
    elif _backend == "openai":
        from openai import OpenAI
        client = OpenAI()
        # replace with your preferred embedding model
        emb = client.embeddings.create(model="text-embedding-3-large", input=texts)
        return [d.embedding for d in emb.data]
    else:
        raise ValueError(f"Unknown EMBED_BACKEND: {_backend}")

def neo4j_vector_search(tx, query_vec, k=8):
    res = tx.run("""
      CALL db.index.vector.queryNodes('textchunk_embedding_index', $k, $q)
      YIELD node, score
      RETURN node.id AS chunk_id, node.text AS text, coalesce(node.source,'') AS source, score
    """, k=k, q=query_vec)
    return [r.data() for r in res]
