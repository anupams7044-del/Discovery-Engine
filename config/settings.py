"""
Application settings loaded from environment variables.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: str = "openai"  # "openai" or "google"
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"

    # Reddit API
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    reddit_user_agent: str = "GooglePhotosDiscoveryEngine/1.0"

    # YouTube API
    youtube_api_key: Optional[str] = None

    # Database
    database_url: str = "sqlite:///data/google_photos.db"
    chroma_persist_dir: str = "data/chroma"
    chroma_collection_name: str = "google_photos_search_feedback"

    # Scraping
    max_items_per_source: int = 500
    scraping_delay_seconds: float = 2.0

    # Analysis
    batch_size: int = 10  # Items per LLM batch call
    max_concurrent_requests: int = 5

    # App
    log_level: str = "INFO"
    app_title: str = "Google Photos Search — AI Discovery Engine"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
