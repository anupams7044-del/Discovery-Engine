"""
SQLAlchemy ORM models matching the schema in architecture.md.
"""
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean,
    DateTime, JSON, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class ScrapeRun(Base):
    __tablename__ = "scrape_runs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="running")
    total_items = Column(Integer, default=0)
    relevant_items = Column(Integer, default=0)
    sources_summary = Column(JSON, nullable=True)
    config = Column(JSON, nullable=True)
    items = relationship("ScrapedItem", back_populates="scrape_run")

class ScrapedItem(Base):
    __tablename__ = "scraped_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    scrape_run_id = Column(Integer, ForeignKey("scrape_runs.id"))
    source = Column(String(50), nullable=False)
    platform = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    cleaned_text = Column(Text, nullable=True)
    title = Column(Text, nullable=True)
    author_hash = Column(String(64), nullable=True)
    date = Column(DateTime, nullable=True)
    rating = Column(Float, nullable=True)
    url = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0)
    is_relevant = Column(Boolean, default=True)
    relevance_score = Column(Float, nullable=True)
    metadata_json = Column("metadata", JSON, nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    scrape_run = relationship("ScrapeRun", back_populates="items")
    analysis = relationship("AnalysisResult", back_populates="item", uselist=False)
    __table_args__ = (UniqueConstraint("url", "text", name="uq_url_text"),)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("scraped_items.id", ondelete="CASCADE"), unique=True)
    sentiment_label = Column(String(20))
    sentiment_score = Column(Float)
    sentiment_confidence = Column(Float)
    emotion = Column(String(30))
    emotion_intensity = Column(String(20))
    primary_issue = Column(String(50))
    issue_categories = Column(JSON)
    severity = Column(String(20))
    retrieval_type = Column(Text)
    user_memory_cues = Column(JSON)
    search_failure_point = Column(String(30))
    themes = Column(JSON)
    key_phrases = Column(JSON)
    analyzed_at = Column(DateTime, default=datetime.utcnow)
    item = relationship("ScrapedItem", back_populates="analysis")

class IssueCategory(Base):
    __tablename__ = "issue_categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text)
    item_count = Column(Integer, default=0)
    avg_severity = Column(Float, nullable=True)
    avg_sentiment = Column(Float, nullable=True)
    is_top_issue = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"))
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    sources = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    session = relationship("ChatSession", back_populates="messages")
