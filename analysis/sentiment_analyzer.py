"""
Sentiment analyzer evaluating user sentiment, confidence, emotion, and intensity.
"""
from analysis.llm_client import LLMClient
from analysis.prompts import SENTIMENT_SYSTEM_PROMPT, SENTIMENT_USER_PROMPT
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def analyze(self, text: str) -> Dict:
        """Analyze sentiment for a single piece of text."""
        try:
            res = self.llm.chat(
                system_prompt=SENTIMENT_SYSTEM_PROMPT,
                user_prompt=f"Analyze this text:\n\n{text}",
                json_mode=True,
            )
            if isinstance(res, dict) and "label" in res:
                return res
            elif isinstance(res, dict) and "results" in res and res["results"]:
                return res["results"][0]
        except Exception as e:
            logger.warning(f"Sentiment analysis single text error: {e}")

        return {
            "label": "neutral",
            "score": 0.0,
            "confidence": 0.5,
            "emotion": "indifference",
            "intensity": "mild"
        }
