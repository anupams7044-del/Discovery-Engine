"""
ChromaDB vector store wrapper for RAG chatbot.
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from config.settings import settings

class VectorStoreManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(self, ids, documents, metadatas, embeddings=None):
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query(self, query_texts=None, query_embeddings=None, n_results=10, where=None):
        return self.collection.query(
            query_texts=query_texts,
            query_embeddings=query_embeddings,
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

    def count(self):
        return self.collection.count()

    def reset(self):
        try:
            self.client.delete_collection(settings.chroma_collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"},
        )
