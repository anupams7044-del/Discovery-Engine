"""
Document embedder indexing analyzed feedback into ChromaDB for RAG retrieval.
"""
from database.database import SessionLocal
from database.models import ScrapedItem, AnalysisResult
from database.vector_store import VectorStoreManager
import chromadb.utils.embedding_functions as ef
import logging

logger = logging.getLogger(__name__)

class DocumentEmbedder:
    def __init__(self):
        self.vector_store = VectorStoreManager()
        self.embedding_fn = ef.DefaultEmbeddingFunction()

    def embed_all(self, db_session=None) -> int:
        """Embed all analyzed items into ChromaDB."""
        close_db = False
        if db_session is None:
            db_session = SessionLocal()
            close_db = True

        try:
            # Query items that have analysis results
            items = db_session.query(ScrapedItem).join(AnalysisResult).filter(
                ScrapedItem.cleaned_text.isnot(None)
            ).all()

            if not items:
                logger.warning("No analyzed items to embed.")
                return 0

            print(f"[EMBEDDER] Indexing {len(items)} items into ChromaDB...")

            ids = []
            documents = []
            metadatas = []

            for item in items:
                analysis = item.analysis
                doc_text = f"Title: {item.title or 'N/A'}\nFeedback: {item.cleaned_text}"
                
                ids.append(f"item_{item.id}")
                documents.append(doc_text)
                metadatas.append({
                    "item_id": item.id,
                    "source": str(item.source),
                    "platform": str(item.platform),
                    "primary_issue": str(analysis.primary_issue if analysis else "other"),
                    "sentiment_label": str(analysis.sentiment_label if analysis else "neutral"),
                    "severity": str(analysis.severity if analysis else "medium"),
                    "date": str(item.date)[:10] if item.date else "N/A",
                })

            # Process in batches of 100 for memory efficiency
            batch_size = 100
            for i in range(0, len(ids), batch_size):
                b_ids = ids[i:i + batch_size]
                b_docs = documents[i:i + batch_size]
                b_meta = metadatas[i:i + batch_size]
                
                # Compute embeddings via local ONNX model
                b_embs = self.embedding_fn(b_docs)
                self.vector_store.add_documents(
                    ids=b_ids,
                    documents=b_docs,
                    metadatas=b_meta,
                    embeddings=b_embs
                )

            total_count = self.vector_store.count()
            print(f"[EMBEDDER] Success! ChromaDB now contains {total_count} indexed documents.")
            return total_count
        except Exception as e:
            logger.error(f"[EMBEDDER] Error embedding items: {e}")
            raise e
        finally:
            if close_db:
                db_session.close()
