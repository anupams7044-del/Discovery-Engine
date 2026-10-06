"""
Main analysis pipeline: runs sentiment analysis, issue classification, and embedding into ChromaDB.
"""
from database.database import SessionLocal
from database.models import ScrapedItem, AnalysisResult
from analysis.llm_client import LLMClient
from analysis.sentiment_analyzer import SentimentAnalyzer
from analysis.issue_classifier import IssueClassifier
from analysis.embedder import DocumentEmbedder
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AnalysisPipeline:
    def __init__(self):
        self.llm = LLMClient()
        self.sentiment = SentimentAnalyzer(self.llm)
        self.classifier = IssueClassifier(self.llm)
        self.embedder = DocumentEmbedder()

    def run(self, scrape_run_id: Optional[int] = None, force_reanalyze: bool = False) -> Dict[str, Any]:
        """Run analysis on all search-relevant items and index to ChromaDB."""
        db = SessionLocal()
        try:
            query = db.query(ScrapedItem).filter(
                ScrapedItem.is_relevant == True,
                ScrapedItem.cleaned_text.isnot(None),
            )
            if scrape_run_id:
                query = query.filter(ScrapedItem.scrape_run_id == scrape_run_id)

            if not force_reanalyze:
                analyzed_ids = [r[0] for r in db.query(AnalysisResult.item_id).all()]
                items = query.filter(ScrapedItem.id.notin_(analyzed_ids)).all()
            else:
                items = query.all()

            total_items = len(items)
            print(f"[AI ENGINE] Starting NLP & LLM analysis on {total_items} relevant items...")

            analyzed_count = 0
            for idx, item in enumerate(items):
                text = item.cleaned_text or item.text

                # 1. Sentiment Analysis
                sent = self.sentiment.analyze(text)

                # 2. Issue Classification
                issue = self.classifier.classify(text)

                # 3. Upsert Analysis Result
                existing = db.query(AnalysisResult).filter_by(item_id=item.id).first()
                if not existing:
                    analysis = AnalysisResult(
                        item_id=item.id,
                        sentiment_label=sent.get("label", "neutral"),
                        sentiment_score=float(sent.get("score", 0.0)),
                        sentiment_confidence=float(sent.get("confidence", 0.8)),
                        emotion=sent.get("emotion", "indifference"),
                        emotion_intensity=sent.get("intensity", "mild"),
                        primary_issue=issue.get("primary_category", "other"),
                        issue_categories=issue.get("categories", ["other"]),
                        severity=issue.get("severity", "medium"),
                        retrieval_type=issue.get("retrieval_type", "Photos"),
                        user_memory_cues=issue.get("user_memory_cues", []),
                        search_failure_point=issue.get("search_failure_point", "retrieval"),
                        analyzed_at=datetime.utcnow(),
                    )
                    db.add(analysis)
                else:
                    existing.sentiment_label = sent.get("label", "neutral")
                    existing.sentiment_score = float(sent.get("score", 0.0))
                    existing.primary_issue = issue.get("primary_category", "other")
                    existing.issue_categories = issue.get("categories", ["other"])
                    existing.severity = issue.get("severity", "medium")
                    existing.search_failure_point = issue.get("search_failure_point", "retrieval")

                analyzed_count += 1

                # Commit every 50 items
                if (idx + 1) % 50 == 0:
                    db.commit()
                    print(f"[AI ENGINE] Analyzed {idx + 1}/{total_items} items...")

            db.commit()
            print(f"[AI ENGINE] Analysis completed for {analyzed_count} items. Starting ChromaDB embedding...")

            # 4. Embed into ChromaDB vector store
            indexed_count = self.embedder.embed_all(db)

            return {
                "analyzed_items": analyzed_count,
                "chromadb_indexed_documents": indexed_count,
            }
        except Exception as e:
            logger.error(f"[AI ENGINE] Analysis pipeline error: {e}")
            db.rollback()
            raise e
        finally:
            db.close()
