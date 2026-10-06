"""
Context retriever querying ChromaDB vector store for relevant feedback chunks.
"""
from database.vector_store import VectorStoreManager
import chromadb.utils.embedding_functions as ef
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ContextRetriever:
    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.embedding_fn = ef.DefaultEmbeddingFunction()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve top_k semantic matches for a query."""
        try:
            query_emb = self.embedding_fn([query])
            results = self.vector_store.query(
                query_embeddings=query_emb,
                n_results=top_k,
            )

            matches = []
            if results and results.get("documents") and results["documents"][0]:
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                dists = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

                for doc, meta, dist in zip(docs, metas, dists):
                    matches.append({
                        "content": doc,
                        "source": meta.get("source", "N/A"),
                        "platform": meta.get("platform", "N/A"),
                        "primary_issue": meta.get("primary_issue", "N/A"),
                        "severity": meta.get("severity", "N/A"),
                        "date": meta.get("date", "N/A"),
                        "distance": dist,
                    })

            return matches
        except Exception as e:
            logger.error(f"Retriever error: {e}")
            return []
